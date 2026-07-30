# Internet Computer node-provider self-declarations

This repository is the public home of the **self-declarations** and supporting
documents of Internet Computer node providers.

A prospective node provider publishes their self-declaration and supporting
artefacts here, and then references those files and their SHA-256 hashes in their
NNS node-provider registration proposal. Anyone can re-compute the hashes from
this repository and compare them with the hashes in the proposal.

This replaces the retired `internetcomputer.mywikis.net` wiki, which previously
hosted these documents. The declarations that were on the wiki have been
backfilled here.

> **Note:** Reviewers of this repository check that a submission is complete,
> correctly named and free of harmful content. They do **not** verify or vouch
> for the truthfulness of the statements a node provider makes in their
> declaration. There is no audit.

## Repository layout

```
├── README.md                       # this file: intro, index, how to submit
├── CONTRIBUTING.md                 # step-by-step submission guide
├── CODEOWNERS                      # who must approve a pull request
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md    # the submission checklist
│   └── workflows/validate.yml      # blocking PR checks
├── scripts/validate.py             # the checks, runnable locally
├── templates/                      # copy these into your own directory
└── node-providers/                 # one directory per node provider
    └── <provider-slug>/
        ├── README.md               # identity, principal, document manifest
        ├── <provider-slug>-self-declaration.pdf
        └── <provider-slug>-proof-of-identity.pdf
```

## What every node provider must submit

| Document | Required | Doc-type in file name |
| --- | --- | --- |
| Per-provider README with the document manifest | yes | — (`README.md`) |
| Self-declaration | yes | `self-declaration` |
| Proof of identity (e.g. commercial-register extract) | yes | `proof-of-identity` |
| Excess-node handover statement | optional | `excess-node-handover` |
| Proof of hardware order | optional | `proof-of-hardware-order` |
| Auditor confirmation letter | optional | `auditor-confirmation` |
| Addendum to a declaration | optional | `addendum` |

### Naming convention

Every document is named:

```
<provider-slug>-<doc-type>.<ext>
```

- `<provider-slug>` — lowercase kebab-case, identical to the directory name;
- `<doc-type>` — one of `self-declaration`, `proof-of-identity`,
  `excess-node-handover`, `proof-of-hardware-order`, `addendum`,
  `auditor-confirmation`;
- `<ext>` — `pdf` is preferred for signed documents (`md`, `png`, `jpg` are also
  accepted).

## How to submit

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full walk-through. In short:

1. Fork this repository and create `node-providers/<your-slug>/`.
2. Copy the files from [templates/](templates/) into it and fill them in.
3. Add your signed documents, named per the convention above.
4. List every file with its SHA-256 hash in your `README.md` manifest.
5. Run `python3 scripts/validate.py --all` and open a pull request.

## Verifying a declaration

To check that the documents in a provider directory are the ones referenced in
the NNS proposal:

```sh
cd node-providers/<provider-slug>
shasum -a 256 *          # macOS
sha256sum *              # Linux
```

Compare the output with the manifest in that directory's `README.md` and with
the hashes in the NNS registration proposal linked from it.

## Index of node providers

| Node provider | Directory | Principal | NNS proposal |
| --- | --- | --- | --- |
| Example Provider LLC (example, not a real provider) | [example-provider-llc](node-providers/example-provider-llc/) | `k4n2l-dljbu-gkrav-vgpnm-v4xbe-fmdpg-5s4ts-ixlw5-65ggf-n5oxu-2ae` | — |
