# Contributing

This guide walks you through publishing your node-provider self-declaration.
Everything happens through a pull request, so the history of every declaration is
public and reviewable.

## Before you start

You need:

- a GitHub account;
- your **self-declaration**, signed (PDF);
- a **proof of identity** for your legal entity, e.g. an extract from the
  commercial register of the jurisdiction where the entity is incorporated (PDF);
- your **node-provider principal** (the principal you will register, or have
  registered, with the NNS);
- optionally: an excess-node handover statement, a proof of hardware order, an
  auditor confirmation letter.

Only the self-declaration and the proof of identity are required.

## 1. Pick your slug

Your slug is the directory name and the prefix of every file you add. It is
lowercase kebab-case, derived from your legal entity name:

```
Example Provider LLC   ->  example-provider-llc
Another Provider GmbH  ->  another-provider-gmbh
```

Use only `a-z`, `0-9` and single dashes. If a directory for your entity already
exists, add to it instead of creating a second one.

## 2. Create your directory

Fork this repository, create a branch, and create
`node-providers/<your-slug>/`. Copy the templates into it:

```sh
mkdir -p node-providers/<your-slug>
cp templates/node-provider-README.md node-providers/<your-slug>/README.md
```

`templates/node-provider-self-declaration.md` is the outline of what a
self-declaration is expected to cover. Use it as the basis for the document you
sign, and add the signed PDF to your directory.

## 3. Name your documents

Every file follows:

```
<provider-slug>-<doc-type>.<ext>
```

- `<provider-slug>` is identical to your directory name;
- `<doc-type>` is one of `self-declaration`, `proof-of-identity`,
  `excess-node-handover`, `proof-of-hardware-order`, `addendum`,
  `auditor-confirmation`;
- `<ext>` is `pdf` for signed documents (`md`, `png`, `jpg`, `jpeg` are also
  accepted).

File names carry no date. The date of each document goes into the manifest in
your `README.md`.

If you have more than one document of the same doc-type — say two addenda — the
second and further ones get a numeric suffix:

```
example-provider-llc-addendum.pdf
example-provider-llc-addendum-2.pdf
```

Example:

```
node-providers/example-provider-llc/
├── README.md
├── example-provider-llc-self-declaration.pdf
├── example-provider-llc-proof-of-identity.pdf
└── example-provider-llc-proof-of-hardware-order.pdf
```

## 4. Fill in your README

Your `README.md` must contain:

- **Node provider name** — the legal name of the entity;
- **Node provider principal** — your node-provider principal;
- **NNS registration proposal ID** — the proposal that registers you as a node
  provider. If you have not submitted it yet, write `pending` and open a
  follow-up pull request with the ID once the proposal exists;
- **Document manifest** — a table listing every file in your directory (except
  `README.md`) with its doc-type, date and SHA-256 hash.

Compute the hashes:

```sh
cd node-providers/<your-slug>
shasum -a 256 *          # macOS
sha256sum *              # Linux
```

These are the same hashes you reference in your NNS registration proposal, so
that anyone can confirm the proposal and this repository describe the same
documents.

See [node-providers/example-provider-llc/README.md](node-providers/example-provider-llc/README.md)
for a filled-in example.

## 5. Check your submission locally

```sh
python3 scripts/validate.py --all
```

This runs exactly the checks that run in CI:

| Check | What it enforces |
| --- | --- |
| structure | changes sit in `node-providers/<slug>/`, slug is kebab-case, no subdirectories |
| naming | every file is `<slug>-<doc-type>.<ext>` |
| required | `README.md`, self-declaration and proof-of-identity are present |
| readme | provider name, principal and proposal ID are present and well formed |
| checksums | recomputed SHA-256 matches the manifest; no unlisted and no missing files |
| hygiene | allowed file types only, max 20 MiB per file, contents match the extension |

## 6. Open the pull request

Push your branch and open a pull request. Fill in the pull-request template and
tick the checklist. Then:

1. CI runs the checks above. A red run must be fixed before review.
2. A reviewer listed in [CODEOWNERS](CODEOWNERS) reviews and merges.

Reviewers check that your submission is complete, correctly named, internally
consistent, and that nothing harmful is being merged. **They do not verify or
vouch for the truthfulness of your declaration.** The declaration is yours; the
repository only makes it public and tamper-evident.

## Updating an existing declaration

- **Correcting metadata** (a typo in the README, filling in the proposal ID):
  edit `README.md` and open a pull request.
- **Replacing a document** with a new version: replace the file, update its hash
  and date in the manifest. The previous version stays in the Git history.
- **Adding information** to a signed declaration: add a signed `addendum`
  document rather than changing the original declaration.

If your NNS proposal references a document by hash, do not silently change that
document: a hash change makes the proposal reference stale, so say in the pull
request why the document changed.
