#!/usr/bin/env python3
"""Validate node-provider self-declaration submissions.

This is the single source of truth for the checks that run in CI
(.github/workflows/validate.yml). Contributors can run it locally before
opening a pull request:

    python3 scripts/validate.py --all                 # check every provider
    python3 scripts/validate.py node-providers/foo    # check one provider
    python3 scripts/validate.py --changed-from origin/main

Checks performed (all blocking):

  structure   changed files sit under node-providers/<slug>/, slug is kebab-case
  naming      every document is named <slug>-<doc-type>.<ext>
  required    README.md, self-declaration and proof-of-identity are present
  readme      required README fields are present and well formed
  checksums   recomputed SHA-256 matches the manifest, no unlisted or
              listed-but-missing files
  hygiene     allowed file types only, no oversized binaries, contents match
              the extension
  shared      the same file does not appear in two provider directories, which
              is an error for a declaration or an identity proof
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import re
import subprocess
import sys
import zlib
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROVIDERS_DIR = "node-providers"

# Accepted <doc-type> values, per the naming convention.
DOC_TYPES = (
    "self-declaration",
    "proof-of-identity",
    "excess-node-handover",
    "proof-of-hardware-order",
    "addendum",
    "auditor-confirmation",
)
REQUIRED_DOC_TYPES = ("self-declaration", "proof-of-identity")

ALLOWED_EXTENSIONS = ("pdf", "md", "png", "jpg", "jpeg")
MAX_FILE_BYTES = 20 * 1024 * 1024  # 20 MiB per file
MAX_DIR_BYTES = 100 * 1024 * 1024  # 100 MiB per provider directory

# Content sniffing, so a .pdf really is a PDF.
MAGIC_BYTES = {
    "pdf": (b"%PDF-",),
    "png": (b"\x89PNG\r\n\x1a\n",),
    "jpg": (b"\xff\xd8\xff",),
    "jpeg": (b"\xff\xd8\xff",),
}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Backfilled documents do not always carry a reliable date.
DATE_UNKNOWN = "unknown"
PROPOSAL_ID_RE = re.compile(r"^\d+$")
# A provider may not have an NNS proposal yet when the declaration is filed.
PROPOSAL_ID_PENDING = "pending"
# The earliest node providers were registered before node-provider onboarding
# moved to NNS proposals, so no registration proposal exists for them.
PROPOSAL_ID_NONE = "none"
PROPOSAL_ID_WORDS = (PROPOSAL_ID_PENDING, PROPOSAL_ID_NONE)

# Documents backfilled from the retired wiki are sometimes incomplete: the wiki
# page linked to a public company register instead of hosting a document, or
# hosted no document at all. Those gaps are recorded here so that the required
# document check can be waived for exactly those providers, while every new
# submission stays strict. See the file for its format.
EXCEPTIONS_FILE = "backfill-exceptions.txt"

# README field labels -> internal key.
FIELD_LABELS = {
    "node provider name": "name",
    "node-provider name": "name",
    "node provider principal": "principal",
    "node-provider principal": "principal",
    "nns registration proposal id": "proposal_id",
    "nns registration proposal": "proposal_id",
}
REQUIRED_FIELDS = ("name", "principal", "proposal_id")

PLACEHOLDER_RE = re.compile(r"<[^>]+>|\bTODO\b|\bFIXME\b|\bXXX\b", re.IGNORECASE)


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------


@dataclass
class Report:
    errors: list[tuple[str, str, str]] = field(default_factory=list)
    warnings: list[tuple[str, str, str]] = field(default_factory=list)

    def error(self, check: str, path: str, message: str) -> None:
        self.errors.append((check, path, message))

    def warn(self, check: str, path: str, message: str) -> None:
        self.warnings.append((check, path, message))

    def emit(self) -> int:
        in_actions = bool(os.environ.get("GITHUB_ACTIONS"))
        for kind, items in (("error", self.errors), ("warning", self.warnings)):
            for check, path, message in items:
                if in_actions:
                    loc = f" file={path}" if path else ""
                    print(f"::{kind}{loc},title={check}::{message}")
                marker = "FAIL" if kind == "error" else "WARN"
                where = f"{path}: " if path else ""
                print(f"{marker} [{check}] {where}{message}")
        if self.errors:
            print(
                f"\n{len(self.errors)} check(s) failed, "
                f"{len(self.warnings)} warning(s)."
            )
            return 1
        print(f"\nAll checks passed ({len(self.warnings)} warning(s)).")
        return 0


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def load_exceptions() -> dict[str, set[str]]:
    """Read the backfill exception list: '<slug> <doc-type> # reason' per line."""
    path = REPO_ROOT / EXCEPTIONS_FILE
    waived: dict[str, set[str]] = {}
    if not path.is_file():
        return waived
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        slug, doc_type = parts[0], parts[1]
        waived.setdefault(slug, set()).add(doc_type)
    return waived


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_valid_principal(text: str) -> bool:
    """Check an IC principal in its canonical textual form.

    Text form is base32(crc32be(blob) || blob), lowercased, without padding,
    in dash-separated groups of five characters.
    """
    if not re.fullmatch(r"[a-z0-9]{1,5}(?:-[a-z0-9]{1,5})*", text):
        return False
    raw = text.replace("-", "").upper()
    try:
        decoded = base64.b32decode(raw + "=" * (-len(raw) % 8))
    except Exception:
        return False
    if len(decoded) < 5:
        return False
    checksum, blob = decoded[:4], decoded[4:]
    if zlib.crc32(blob).to_bytes(4, "big") != checksum:
        return False
    canonical = base64.b32encode(decoded).decode("ascii").lower().rstrip("=")
    grouped = "-".join(canonical[i : i + 5] for i in range(0, len(canonical), 5))
    return grouped == text


def split_table_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [cell.strip() for cell in cells]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


def parse_tables(text: str) -> list[list[list[str]]]:
    """Return every markdown table as a list of rows of cells."""
    tables: list[list[list[str]]] = []
    current: list[list[str]] = []
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            cells = split_table_row(line)
            if not is_separator_row(cells):
                current.append(cells)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def normalise_label(cell: str) -> str:
    return re.sub(r"[*`_:]", "", cell).strip().lower()


def clean_cell(cell: str) -> str:
    return cell.strip().strip("`").strip()


@dataclass
class ManifestRow:
    filename: str
    doc_type: str
    date: str
    sha256: str


@dataclass
class ProviderReadme:
    fields: dict[str, str] = field(default_factory=dict)
    manifest: list[ManifestRow] = field(default_factory=list)
    has_manifest_table: bool = False


def parse_provider_readme(text: str) -> ProviderReadme:
    parsed = ProviderReadme()
    for table in parse_tables(text):
        header = [normalise_label(c) for c in table[0]]
        is_manifest = (
            len(header) >= 4
            and any("file" in c for c in header)
            and any(c.replace("-", "") in ("sha256", "sha256hash") for c in header)
        )
        if is_manifest:
            parsed.has_manifest_table = True
            for row in table[1:]:
                if len(row) < 4 or not clean_cell(row[0]):
                    continue
                parsed.manifest.append(
                    ManifestRow(
                        filename=clean_cell(row[0]),
                        doc_type=clean_cell(row[1]).lower(),
                        date=clean_cell(row[2]),
                        sha256=clean_cell(row[3]).lower(),
                    )
                )
            continue
        for row in table:
            if len(row) < 2:
                continue
            key = FIELD_LABELS.get(normalise_label(row[0]))
            if key and key not in parsed.fields:
                parsed.fields[key] = clean_cell(row[1])
    return parsed


# --------------------------------------------------------------------------
# per-provider validation
# --------------------------------------------------------------------------


def validate_provider(slug: str, report: Report, waived: dict[str, set[str]] | None = None) -> None:
    directory = REPO_ROOT / PROVIDERS_DIR / slug
    rel_dir = f"{PROVIDERS_DIR}/{slug}"

    if not SLUG_RE.fullmatch(slug):
        report.error(
            "structure",
            rel_dir,
            f"provider directory name '{slug}' is not lowercase kebab-case",
        )

    if not directory.is_dir():
        report.error("structure", rel_dir, "provider directory does not exist")
        return

    # -- structure: flat directory, no nested paths -------------------------
    entries = sorted(directory.iterdir(), key=lambda p: p.name)
    files: list[Path] = []
    for entry in entries:
        rel = f"{rel_dir}/{entry.name}"
        if entry.is_dir():
            report.error(
                "structure", rel, "subdirectories are not allowed in a provider directory"
            )
        elif entry.is_symlink():
            report.error("structure", rel, "symlinks are not allowed")
        elif entry.name.startswith("."):
            report.error("hygiene", rel, "dotfiles are not allowed")
        else:
            files.append(entry)

    documents = [f for f in files if f.name != "README.md"]

    # -- naming ------------------------------------------------------------
    # <slug>-<doc-type>.<ext>, with an optional -<n> suffix for the second and
    # further documents of the same doc-type.
    name_re = re.compile(
        rf"^{re.escape(slug)}-({'|'.join(DOC_TYPES)})(-[2-9]\d*)?"
        rf"\.({'|'.join(ALLOWED_EXTENSIONS)})$"
    )
    doc_types_present: dict[str, list[str]] = {}
    for document in documents:
        rel = f"{rel_dir}/{document.name}"
        match = name_re.fullmatch(document.name)
        if not match:
            report.error(
                "naming",
                rel,
                "filename must be <provider-slug>-<doc-type>.<ext> (optionally "
                "<provider-slug>-<doc-type>-<n>.<ext> for further documents of the "
                f"same type) with slug '{slug}', doc-type one of "
                f"{', '.join(DOC_TYPES)} and extension one of "
                f"{', '.join(ALLOWED_EXTENSIONS)}",
            )
            continue
        doc_types_present.setdefault(match.group(1), []).append(document.name)

    # -- required documents ------------------------------------------------
    if not (directory / "README.md").is_file():
        report.error("required", f"{rel_dir}/README.md", "README.md is missing")
    exempt = (waived or {}).get(slug, set())
    for doc_type in REQUIRED_DOC_TYPES:
        if doc_type in doc_types_present:
            continue
        if doc_type in exempt:
            report.warn(
                "required",
                rel_dir,
                f"required document '{doc_type}' is missing, waived by "
                f"{EXCEPTIONS_FILE}",
            )
            continue
        report.error("required", rel_dir, f"required document '{doc_type}' is missing")

    # -- hygiene -----------------------------------------------------------
    total_bytes = 0
    for document in files:
        rel = f"{rel_dir}/{document.name}"
        size = document.stat().st_size
        total_bytes += size
        if size == 0:
            report.error("hygiene", rel, "file is empty")
            continue
        if size > MAX_FILE_BYTES:
            report.error(
                "hygiene",
                rel,
                f"file is {size / 1024 / 1024:.1f} MiB, the limit is "
                f"{MAX_FILE_BYTES // 1024 // 1024} MiB",
            )
        extension = document.suffix.lower().lstrip(".")
        if extension not in ALLOWED_EXTENSIONS:
            report.error(
                "hygiene",
                rel,
                f"file type '.{extension}' is not allowed "
                f"(allowed: {', '.join('.' + e for e in ALLOWED_EXTENSIONS)})",
            )
            continue
        expected_magic = MAGIC_BYTES.get(extension)
        if expected_magic:
            with document.open("rb") as handle:
                head = handle.read(16)
            if not any(head.startswith(m) for m in expected_magic):
                report.error(
                    "hygiene",
                    rel,
                    f"contents do not look like a {extension.upper()} file",
                )
    if total_bytes > MAX_DIR_BYTES:
        report.error(
            "hygiene",
            rel_dir,
            f"directory is {total_bytes / 1024 / 1024:.1f} MiB, the limit is "
            f"{MAX_DIR_BYTES // 1024 // 1024} MiB",
        )

    # -- README completeness ----------------------------------------------
    readme_path = directory / "README.md"
    if not readme_path.is_file():
        return
    rel_readme = f"{rel_dir}/README.md"
    parsed = parse_provider_readme(readme_path.read_text(encoding="utf-8"))

    for key in REQUIRED_FIELDS:
        value = parsed.fields.get(key, "")
        if not value:
            report.error(
                "readme",
                rel_readme,
                f"required field '{key}' is missing or empty "
                "(see templates/node-provider-README.md)",
            )
            continue
        if PLACEHOLDER_RE.search(value):
            report.error(
                "readme", rel_readme, f"field '{key}' still contains a placeholder: {value}"
            )

    principal = parsed.fields.get("principal", "")
    if principal and not PLACEHOLDER_RE.search(principal):
        if not is_valid_principal(principal):
            report.error(
                "readme", rel_readme, f"'{principal}' is not a valid IC principal"
            )

    proposal_id = parsed.fields.get("proposal_id", "")
    if proposal_id and not PLACEHOLDER_RE.search(proposal_id):
        # accept a bare number, a markdown link whose text is the number, or one
        # of the two words
        bare = re.sub(r"^\[([^\]]*)\]\([^\)]*\)$", r"\1", proposal_id).strip()
        if bare.lower() not in PROPOSAL_ID_WORDS and not PROPOSAL_ID_RE.fullmatch(bare):
            report.error(
                "readme",
                rel_readme,
                "NNS registration proposal ID must be a number, "
                f"'{PROPOSAL_ID_PENDING}' or '{PROPOSAL_ID_NONE}', got '{proposal_id}'",
            )

    if not parsed.has_manifest_table:
        report.error(
            "readme",
            rel_readme,
            "the document manifest table is missing (columns: file, doc-type, "
            "date, SHA-256)",
        )
        return
    if not parsed.manifest:
        report.error("readme", rel_readme, "the document manifest table has no entries")

    # -- checksums ---------------------------------------------------------
    listed: dict[str, ManifestRow] = {}
    for row in parsed.manifest:
        if row.filename in listed:
            report.error(
                "checksums", rel_readme, f"'{row.filename}' is listed twice in the manifest"
            )
            continue
        listed[row.filename] = row

        if row.doc_type not in DOC_TYPES:
            report.error(
                "readme",
                rel_readme,
                f"'{row.filename}': doc-type '{row.doc_type}' is not one of "
                f"{', '.join(DOC_TYPES)}",
            )
        if not DATE_RE.fullmatch(row.date) and row.date.lower() != DATE_UNKNOWN:
            report.error(
                "readme",
                rel_readme,
                f"'{row.filename}': date '{row.date}' must be ISO 8601 (YYYY-MM-DD) "
                f"or '{DATE_UNKNOWN}'",
            )
        if not SHA256_RE.fullmatch(row.sha256):
            report.error(
                "checksums",
                rel_readme,
                f"'{row.filename}': '{row.sha256}' is not a lowercase hex SHA-256 digest",
            )
            continue

        document = directory / row.filename
        if not document.is_file():
            report.error(
                "checksums",
                rel_readme,
                f"'{row.filename}' is listed in the manifest but does not exist",
            )
            continue
        actual = sha256_file(document)
        if actual != row.sha256:
            report.error(
                "checksums",
                f"{rel_dir}/{row.filename}",
                f"SHA-256 mismatch: manifest says {row.sha256}, file is {actual}",
            )

    for document in documents:
        if document.name not in listed:
            report.error(
                "checksums",
                f"{rel_dir}/{document.name}",
                "file is not listed in the README manifest",
            )


# --------------------------------------------------------------------------
# cross-provider checks
# --------------------------------------------------------------------------

# Two providers legitimately publish the same document when it is a statement
# they both signed — an excess-node handover between the two of them. Nobody
# legitimately shares a declaration or an identity proof.
UNIQUE_DOC_TYPES = ("self-declaration", "proof-of-identity")


def check_no_shared_documents(report: Report, slugs: list[str]) -> None:
    """Flag one document appearing in more than one provider directory.

    A backfill mistake put one provider's identity proof into another provider's
    directory; identical bytes under two providers is the signature of that class
    of error, so it is checked repository-wide.
    """
    root = REPO_ROOT / PROVIDERS_DIR
    if not root.is_dir():
        return
    by_digest: dict[str, list[tuple[str, str]]] = {}
    for provider in sorted(p for p in root.iterdir() if p.is_dir()):
        for document in sorted(provider.iterdir()):
            if not document.is_file() or document.name == "README.md":
                continue
            by_digest.setdefault(sha256_file(document), []).append(
                (provider.name, document.name)
            )

    touched = set(slugs)
    for digest, owners in sorted(by_digest.items()):
        if len(owners) < 2:
            continue
        # only report where the pull request is involved, so unrelated
        # pre-existing pairs do not fail someone else's submission
        if touched and not any(slug in touched for slug, _ in owners):
            continue
        where = ", ".join(f"{PROVIDERS_DIR}/{s}/{n}" for s, n in owners)
        doc_types = {
            re.sub(rf"^{re.escape(s)}-|(-\d+)?\.\w+$", "", n) for s, n in owners
        }
        unique_required = doc_types & set(UNIQUE_DOC_TYPES)
        message = (
            f"the same file ({digest[:12]}...) appears in several provider "
            f"directories: {where}"
        )
        if unique_required:
            report.error(
                "shared-document",
                f"{PROVIDERS_DIR}/{owners[0][0]}/{owners[0][1]}",
                f"{message}. A {'/'.join(sorted(unique_required))} belongs to one "
                "provider only — check that each directory holds its own document",
            )
        else:
            report.warn(
                "shared-document",
                f"{PROVIDERS_DIR}/{owners[0][0]}/{owners[0][1]}",
                f"{message}. This is expected for a statement both parties signed, "
                "such as an excess-node handover; confirm that is the case here",
            )


# --------------------------------------------------------------------------
# target selection
# --------------------------------------------------------------------------


def all_slugs() -> list[str]:
    root = REPO_ROOT / PROVIDERS_DIR
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def changed_paths(base_ref: str) -> list[str]:
    merge_base = subprocess.run(
        ["git", "merge-base", base_ref, "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    diff_base = merge_base.stdout.strip() if merge_base.returncode == 0 else base_ref
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=d", diff_base, "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def slugs_from_paths(paths: list[str], report: Report) -> list[str]:
    slugs: list[str] = []
    for raw in paths:
        rel = os.path.relpath(os.path.abspath(raw), REPO_ROOT)
        parts = Path(rel).parts
        if not parts or parts[0] != PROVIDERS_DIR:
            report.warn(
                "structure", rel, "path is outside node-providers/, not validated here"
            )
            continue
        if len(parts) == 1:
            continue
        if len(parts) > 3:
            report.error(
                "structure",
                rel,
                "files must sit directly in node-providers/<slug>/, "
                "nested directories are not allowed",
            )
        if len(parts) == 2 and (REPO_ROOT / rel).is_file():
            report.error(
                "structure",
                rel,
                "stray file in node-providers/, every document belongs to a "
                "provider directory",
            )
            continue
        if parts[1] not in slugs:
            slugs.append(parts[1])
    return sorted(slugs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        help="provider directories or files to validate",
    )
    parser.add_argument("--all", action="store_true", help="validate every provider")
    parser.add_argument(
        "--changed-from",
        metavar="REF",
        help="validate the providers touched since REF (e.g. origin/main)",
    )
    args = parser.parse_args()

    report = Report()

    if args.all:
        slugs = all_slugs()
    elif args.changed_from:
        slugs = slugs_from_paths(changed_paths(args.changed_from), report)
    elif args.paths:
        slugs = slugs_from_paths(args.paths, report)
    else:
        parser.error("give one of: paths, --all, --changed-from REF")

    if not slugs:
        print("No provider directories to validate.")
        return report.emit()

    print(f"Validating {len(slugs)} provider directory/directories:")
    for slug in slugs:
        print(f"  - {PROVIDERS_DIR}/{slug}")
    print()

    waived = load_exceptions()
    for slug in slugs:
        validate_provider(slug, report, waived)
    check_no_shared_documents(report, slugs if not args.all else [])

    return report.emit()


if __name__ == "__main__":
    sys.exit(main())
