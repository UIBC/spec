# A conformance programme for UIBC packages — what exists, what does not

This document is written for two readers: someone who wants their verifier
listed, and someone deciding whether to trust a listing. It describes the
smallest programme that is honest at today's scale: one maintainer, two
implementations, zero independent runs.

**Status: proposal. Nothing here certifies a product, and UIBC is not a
standards body.** No submission has been received, because the programme
described below is being designed before it is opened — not after a logo is
printed on a certificate.

## 1. What the programmes we are copying actually do

The mechanics below are quoted because they are the parts that make a
programme survive contact with vendors, not the parts that make a website look
serious.

- **NIST CAVP / ACVP.** The lab does not run your implementation. The server
  generates test vectors matched to the capabilities you declare, your
  implementation produces the outputs, and the server judges them:
  "The CAVP is not responsible for running those test vectors through the
  implementation" — testing is entirely black-box, and the implementation is
  never handed to NIST. Source: <http://www.shturl.cc/48eb12aca982f9c35815c8881d0c174e>,
  protocol: <https://pages.nist.gov/ACVP/draft-fussell-acvp-spec.html>.
- **CNCF Certified Kubernetes.** Self-testing with a published suite, then a
  pull request to `cncf/k8s-conformance` carrying machine output plus a
  `PRODUCT.yaml` manifest (vendor name as a legal entity, platform name and
  version, repo URL, docs URL); a bot pre-checks the PR, a reviewer approves,
  and certification is time-limited — valid up to 12 months, with
  recertification each year. Over 90 offerings listed.
  Sources: <https://www.cncf.io/training/certification/software-conformance/>,
  <http://www.shturl.cc/5916385412faa7332fc8c603687ded11>.
- **W3C DID Core.** 137 normative features, 47 DID methods submitting results,
  per-feature pass/fail recorded rather than a single badge:
  <https://w3c.github.io/did-wg/faqs/2021-formal-objections/>.

Three properties recur: results are **machine-readable and submitted**, the
manifest identifies a **legal entity**, and the listing **expires**.

## 2. What UIBC has today, measured

| programme ingredient | CNCF / ACVP / DID | UIBC today | verdict |
|---|---|---|---|
| published test corpus | yes | 6 fixtures + 12 adversarial packages, frozen by `FIXTURES.sha256` | exists |
| runner a stranger can execute | yes | `tools/run_crossimpl.py`, `run_vectors.py`, `run_adversarial.py` | exists |
| second implementation | yes | `second-impl/verify.mjs`, Node 22, 10 of 19 checks | exists, same maintainer |
| implementation manifest | yes | `implementations.json` | exists |
| gate that refuses overclaims | implicit | `tools/check_implementations.py` (R1–R5) | exists |
| independent implementation | yes | none | **absent** |
| submitted external run | yes | `EXTERNAL-RUNS.json`-style ledger, empty on purpose | **absent** |
| legal entity / signed terms | yes | none | **absent** |
| validity period and revocation | yes | not defined | **absent** |
| reviewer other than the author | yes | none | **absent** |

Four of the eight ingredients exist. The four that do not are all *social*
(another maintainer, another organisation, a clock, a reviewer) — which is
exactly why writing more code cannot close them.

## 3. The smallest submission, defined

A submission is a pull request to `UIBC/vectors` adding one directory under
`submissions/<entity>-<impl>/` containing:

1. `PRODUCT.yaml` — legal entity, implementation name and version, language,
   repository URL, the checks it claims (`S1`…`S19`), and a contact address.
2. `results.json` — one row per corpus case: case id, verdict, exit code,
   timestamp, and the digest of the case tree it was produced against.
3. `run.log` — the unedited stdout of the runner. A log that has been tidied is
   refused; the noise is part of the evidence.

Three rules apply to all of it:

- **Verdicts must match the frozen corpus.** A submission that disagrees with
  `EXPECTED.md` on any frozen row is refused, not negotiated. Discussion of
  whether the corpus is right belongs in an issue, before the submission.
- **Independence is a fact about people, not about languages.** `independent`
  requires a maintainer who did not write the reference verifier. A second
  language from the same person is `same-maintainer`, and `check_implementations.py`
  refuses the other word from our own address.
- **Coverage is a set, never a percentage.** "80% conformant" is meaningless
  when checks differ in weight; the listing shows which check ids were run and
  which returned PASS.

## 4. What a listing would and would not say

A listing would say: *on `<date>`, implementation `<x>` produced verdicts
matching the frozen corpus on rows `<set>`, as recorded in `results.json`.*

It would not say: that the implementation is secure, that a package it accepts
is trustworthy, that the entity is competent, or that UIBC approves of the
product. No certificate, no badge, no mark. That sentence is already in the
organisation profile, and it survives every future version of this programme:
`Not a standards body; issues no certificates.`

## 5. Time limits, because a listing that never expires is a rumour

- A listing is valid for **12 months** from the recorded run date, mirroring the
  Kubernetes recertification cycle.
- The corpus changes; when a frozen row changes, listings citing the old
  `FIXTURES.sha256` digest are marked `superseded`, not deleted, and remain
  readable with their original digest.
- Revocation for cause: a submission later found to have been produced against a
  modified corpus is marked `revoked` and the entry must name the digest it
  actually ran (`registry/check_registry.py` already enforces that a revoked
  entry binds a target root).

## 6. What we will not build

- No paid certification, no logo licence, no "UIBC Approved" mark.
- No percentage scores.
- No reviewer who is also the only maintainer: while the corpus has one
  maintainer, a self-review is labelled `self-review` in the listing rather than
  presented as independent review. That label disappears the day a second
  reviewer exists — and not before.

## 7. Open questions we are not pretending to have answered

1. Which legal entity would hold submissions, given there is no incorporated
   body yet.
2. Whether a 12-month validity is meaningful for a corpus that currently changes
   weekly.
3. How a submission proves it ran the frozen corpus rather than a locally
   adjusted copy — the digest in `results.json` covers the case tree, not the
   runner's code, and the runner is ours.
4. What a medical-device manufacturer would actually need to see before citing a
   UIBC listing in a 510(k) cybersecurity submission, if anything. That question
   belongs to `MEDICAL-MAPPING.md` and is currently unanswered by evidence.
