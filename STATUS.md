# STATUS · public edition ledger

Last updated: 2026-11-25.

Every row is either a fact someone can re-check, or a gap we have not closed. No aspirational rows.

## What exists

| Item | Where | Re-checkable how |
|---|---|---|
| Draft 00 of the spec | `spec/draft-zhao-uibc-evidence-chain-00.md` (17,114 B) | read it |
| Reference verifier | `zhaoxinghua09-cell/uibc-core`, PyPI `uibc-core` 0.5.0 | `pip install uibc-core` then `uibc verify <pkg>` |
| Online entry | `https://zhaoxinghua09-cell.github.io/uibc-core/` | open it |
| Organisation identity | `https://github.com/UIBC` | open it |

## Gaps, in the order they hurt

| Gap | Measured value | Why it matters |
|---|---|---|
| External verification nodes | **0** | Independence rests on two implementations by the same author |
| Third-party run receipts | **0** | No `RUNS.md` row is a real run yet |
| Published normative spec | **none** (draft-00 only) | Readers have nothing to conform *to* |
| Check count consistency | closed 2026-11-25: abstract and Section 5 both say 19; S19 added to the table | S19 had no sentence anywhere in the draft, so a reader could not have implemented it |
| S19 baseline | a package whose outcome is `FAIL` still writes the high-water mark (0.5.0) | The rejection is recorded as "last accepted observation"; Section 7.6 forbids it, the code does it |
| Root algorithm | provisional | Cannot be ratified while flagged provisional |
| Transparent log / witness | none | Timestamps prove time, not that a log accepted the bytes |

## Why this repository exists separately

The core repository carries implementation, tests and history. This one carries only what a reader needs in order to judge the format: the text, the status, the gaps. Small enough to read in one sitting, small enough to review line by line.

## Change log

- 2026-11-23: repository created; draft 00 published as-is, with the check-count drift recorded rather than silently fixed.
