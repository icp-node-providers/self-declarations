<!--
Copy this file to node-providers/<your-slug>/README.md and fill it in.

Replace every <placeholder>. CI rejects a README that still contains
placeholders, that is missing a required field, or whose manifest does not match
the files in the directory exactly.
-->

# <Node provider legal name>

| Field | Value |
| --- | --- |
| **Node provider name** | <Node provider legal name, as registered> |
| **Node provider principal** | `<node-provider-principal>` |
| **NNS registration proposal ID** | [<proposal-id>](https://dashboard.internetcomputer.org/proposal/<proposal-id>) |

<!--
If the NNS registration proposal has not been submitted yet, put `pending` in the
proposal ID field and open a follow-up pull request with the ID once the proposal
has been submitted.
-->

## Document manifest

<!--
Every file in this directory except README.md must appear here exactly once, and
every entry must point at a file that exists.

  file      the file name, as in this directory
  doc-type  self-declaration | proof-of-identity | excess-node-handover |
            proof-of-hardware-order | addendum | auditor-confirmation
  date      the date of the document itself (signature date), ISO 8601
  SHA-256   shasum -a 256 <file>   (macOS)
            sha256sum <file>       (Linux)
-->

| File | Doc type | Date | SHA-256 |
| --- | --- | --- | --- |
| `<slug>-self-declaration.pdf` | self-declaration | <YYYY-MM-DD> | `<sha256>` |
| `<slug>-proof-of-identity.pdf` | proof-of-identity | <YYYY-MM-DD> | `<sha256>` |

## Notes

<!-- Optional. Anything a reader should know, e.g. what the proof of identity is,
     which entity signed, or why an addendum was added. Remove if unused. -->
