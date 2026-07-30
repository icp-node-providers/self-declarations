<!--
Thanks for submitting your node-provider self-declaration.

Please fill in the summary below and tick every box. A reviewer will merge the
pull request once CI is green. Reviewers check that the submission is complete
and well formed; they do not vouch for the truthfulness of the declaration.
-->

## Summary

- **Node provider name:**
- **Provider slug (directory name):** `node-providers/<provider-slug>/`
- **Node provider principal:**
- **NNS registration proposal ID:** <!-- number, or "pending" if not submitted yet -->
- **Type of change:** <!-- new provider / additional document / correction / update -->

## Checklist

- [ ] All my changes are inside a single `node-providers/<provider-slug>/` directory.
- [ ] The slug is lowercase kebab-case and matches the prefix of every file name.
- [ ] Every file is named `<provider-slug>-<doc-type>.<ext>`, with `<doc-type>` one of
      `self-declaration`, `proof-of-identity`, `excess-node-handover`,
      `proof-of-hardware-order`, `addendum`, `auditor-confirmation` — and a numeric
      suffix (`-2`, `-3`, …) for further documents of the same doc-type.
- [ ] The required documents are present: `README.md`, the self-declaration and a
      proof of identity (e.g. a commercial-register extract).
- [ ] `README.md` lists the provider name, the principal and the NNS registration
      proposal ID.
- [ ] The `README.md` document manifest lists **every** file in the directory with its
      doc-type, date and SHA-256 hash — no missing and no extra entries.
- [ ] The hashes in the manifest are the hashes of the files in this pull request
      (`shasum -a 256 <file>`), and match the hashes referenced in the NNS proposal
      (if the proposal has already been submitted).
- [ ] Documents are signed PDFs where a signature is expected.
- [ ] I ran `python3 scripts/validate.py --all` locally and it passed.
