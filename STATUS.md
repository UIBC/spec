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
| Second implementation (18 of 19 checks, CI-enforced) | `zhaoxinghua09-cell/uibc-core` `tools/verify-js` | `python tools/assert_second_impl.py`; measured `strict 36/36` over 36 packages |
| Third verifier (Node 22, 10 of 19 checks, public corpus) | `UIBC/vectors/second-impl` | `node second-impl/verify.mjs vectors/clean` - exists so the public corpus replays without Python, not as an improvement |
| Cross-implementation replay | `UIBC/vectors/tools/run_crossimpl.py` | 20/20 verdicts, 182/182 per-check agree; writes `interop-results.json` |
| Implementations manifest + anti-overclaim gate | `UIBC/vectors/implementations.json` | `python tools/check_implementations.py` → refuses 'independent' from our own address |
| Conformance programme (proposal) | `CONFORMANCE-PROGRAM.md` | read it; no submission has been received |

## Gaps, in the order they hurt

| Gap | Measured value | Why it matters |
|---|---|---|
| External verification nodes | **0** | Three implementations, one author. `implementations.json` labels all four entries `same-maintainer` and `check_implementations.py` refuses the word 'independent' from this organisation's address. Two implementations agreeing with each other is convergence, not corroboration |
| Third-party run receipts | **0** | No `RUNS.md` row is a real run yet |
| Published normative spec | **none** (draft-00 only) | Readers have nothing to conform *to* |
| Check count consistency | abstract says 18, verifier runs S1–S19 | A reader counting will find the mismatch |
| Root algorithm | provisional | Cannot be ratified while flagged provisional |
| Transparent log witness | anchor tooling exists (`anchor_rekor.py`, `anchor_ots.py`, `anchor_tsa.py`, `nostr_anchor.py`); two Bitcoin block attestations published (heights 976684 and 976735); **no transparency-log inclusion entry a reader can open** | Time is proven to a block; equivocation by a log is not what a block proves, and one is not claimed |
| **D-002: index metadata partly mutable** | `evidence_id`, `media_type`, `created_at` rewritable while verdict stays PASS | Evidence can be backdated or re-identified without detection. Found 2026-11-24 by our own adversarial set; reproduce with `run_adversarial.py`, gate with `--strict` |
| Medical mapping | proposal only | `MEDICAL-MAPPING.md` is unverified against a real submission; no regulatory endorsement |

## Why this repository exists separately

The core repository carries implementation, tests and history. This one carries only what a reader needs in order to judge the format: the text, the status, the gaps. Small enough to read in one sitting, small enough to review line by line.

## Change log

- 2026-11-23: repository created; draft 00 published as-is, with the check-count drift recorded rather than silently fixed.
- 2026-11-24 (later): second implementation added (Node 22, zero deps, S1-S8/S11/S12). Its first cross-run caught a real ambiguity - whether the evidence root is computed over bytes on disk or over hashes the index claims - which the spec text had left unsaid; the rule is now stated in the implementation and recorded in `implementations.json`. `CONFORMANCE-PROGRAM.md` added as a proposal, with the four missing ingredients named.
- 2026-11-24: the matrix it points at is now eight rows (`unsigned`, `unknown-upgrade`); twelve-case adversarial supplement added; fixture digests frozen; D-002 found and recorded; `MEDICAL-MAPPING.md` added as a proposal.




## 关于这张表的有效期

这张表历史上的若干行是凭快照写的，2026-11-24 一天内查出三行已过期：第二实现（`verify-js` 18/19 项、CI 强制）被写成缺失；验证器基准记录被写成没有；比特币区块时间证明（高度 976735 / 976684）被写成 Pending。

修复方向不是再改一遍句子，而是让句子有摘要：`UIBC/.github` 的 `registry/evidence-index.json` 把这类说法变成可抓取、可比对的行，`check_evidence_index.py` 每天重抓一次；"absent"的行必须带一个可能反驳它的账本。

在那张索引覆盖每一行之前，**本表应被读作一份有有效期的摘要，而不是证据本身**。
