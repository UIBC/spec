# UIBC specification · draft 00

The specification of **UIBC** — a portable package that binds an agent's identity, lifecycle and action evidence into one hash-committed structure, plus a verification procedure with three-valued outcomes.

**Status: draft-00, non-normative.** Written in Internet-Draft shape so reviewers can read it the way they read a draft. It has **not** been submitted to any standards body, carries no IETF copyright notice, and claims no standards status. Do not cite it as an Internet-Draft.

## Read the draft

- [`spec/draft-zhao-uibc-evidence-chain-00.md`](spec/draft-zhao-uibc-evidence-chain-00.md) (2026-11-18, 11.5 KB)

## What this draft does and does not do

It defines what can be checked **from bytes alone**, and it names what it does not check. A UIBC judgement is evidence a reader can re-run; it is not an authorisation, a certificate, or a statement about whether the agent behaved well.

## Reference implementation

- Repository: `zhaoxinghua09-cell/uibc-core` (Apache-2.0)
- Package: `uibc-core` 0.5.0 on PyPI
- Online page: `https://zhaoxinghua09-cell.github.io/uibc-core/`

## Known open defects in this draft

| Defect | Detail | State |
|---|---|---|
| Check count drift | Abstract says "eighteen-check"; the reference verifier runs S1–S19 | open |
| Root algorithm provisional | `sha256(canonical-json(sorted(content_hashes)) v0.1-provisional)` is not ratified | open |
| No external review | No third party has read this draft under a recorded name | open |
| Not submitted | No datatracker entry exists | by design, for now |

Full ledger: [`STATUS.md`](STATUS.md).

## Licence

Apache-2.0 — see [`LICENSE`](LICENSE).
