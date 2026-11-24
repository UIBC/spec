# STATUS · public edition ledger

Last updated: 2026-11-24.

Every row is either a fact someone can re-check, or a gap we have not closed. No aspirational rows.

## What exists

| Item | Where | Re-checkable how |
|---|---|---|
| Draft 00 of the spec | `spec/draft-zhao-uibc-evidence-chain-00.md` (11,581 B) | read it |
| Reference verifier | `zhaoxinghua09-cell/uibc-core`, PyPI `uibc-core` 0.5.0 | `pip install uibc-core` then `uibc verify <pkg>` |
| Online entry | `https://zhaoxinghua09-cell.github.io/uibc-core/` | open it |
| Organisation identity | `https://github.com/UIBC` | open it |
| Eight-row conformance matrix | `UIBC/vectors` | `python tools/run_vectors.py` → 8/8 |
| Adversarial supplement (12 cases) | `UIBC/vectors` | `python tools/run_adversarial.py` → 9 rejected, 3 documented defects |
| Frozen fixture digests | `UIBC/vectors/FIXTURES.sha256` | `python tools/check_frozen.py` → 45 files match |
| Claim checker (anti-overclaim) | `UIBC/vectors/tools/check_report.py` | `--selftest` → 4/4 doctored reports rejected |
| Medical mapping (proposal) | `MEDICAL-MAPPING.md` | read it; not a regulatory opinion |
| Registry (six states) | `UIBC/.github/registry` | `python registry/check_registry.py` |

## Gaps, in the order they hurt

| Gap | Measured value | Why it matters |
|---|---|---|
| External verification nodes | **0** | Independence rests on two implementations by the same author |
| Third-party run receipts | **0** | No `RUNS.md` row is a real run yet |
| Published normative spec | **none** (draft-00 only) | Readers have nothing to conform *to* |
| Check count consistency | abstract says 18, verifier runs S1–S19 | A reader counting will find the mismatch |
| Root algorithm | provisional | Cannot be ratified while flagged provisional |
| Transparent log / witness | none | Timestamps prove time, not that a log accepted the bytes |
| **D-002: index metadata partly mutable** | `evidence_id`, `media_type`, `created_at` rewritable while verdict stays PASS | Evidence can be backdated or re-identified without detection. Found 2026-11-24 by our own adversarial set; reproduce with `run_adversarial.py`, gate with `--strict` |
| Medical mapping | proposal only | `MEDICAL-MAPPING.md` is unverified against a real submission; no regulatory endorsement |

## Why this repository exists separately

The core repository carries implementation, tests and history. This one carries only what a reader needs in order to judge the format: the text, the status, the gaps. Small enough to read in one sitting, small enough to review line by line.

## Change log

- 2026-11-23: repository created; draft 00 published as-is, with the check-count drift recorded rather than silently fixed.
- 2026-11-24: the matrix it points at is now eight rows (`unsigned`, `unknown-upgrade`); twelve-case adversarial supplement added; fixture digests frozen; D-002 found and recorded; `MEDICAL-MAPPING.md` added as a proposal.
