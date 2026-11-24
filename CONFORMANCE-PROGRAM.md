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
| second implementation | yes | `uibc-core/tools/verify-js` (18 of 19, CI-enforced, 36 packages) and `UIBC/vectors/second-impl` (10 of 19, public corpus) | exists, same maintainer twice |
| implementation manifest | yes | `implementations.json`: 4 entries, 0 independent | exists |
| gate that refuses overclaims | implicit | `tools/check_implementations.py` (R1–R5) | exists |
| independent implementation | yes | none | **absent** |
| submitted run record | yes | `UIBC/vectors/submissions/` now holds one submission judged by `tools/check_submission.py` (twelve rules, thirteen-way self-test plus one honestly signed witness that must pass, covering competence basis, witness statement and scope); `uibc-core/benchmarks/submissions/` holds one verifier benchmark | exists, **both by this maintainer, zero external, competence basis `none`, witness `null`** |
| legal entity / signed terms | yes | none | **absent** |
| validity period and revocation | yes | not defined | **absent** |
| reviewer other than the author | yes | none | **absent** |

Five of the eight ingredients exist and one is half-built: the submission
record exists but has never been filled in by anyone outside this organisation.
The three that do not exist — another maintainer, a legal entity to sign terms,
a reviewer who is not the author — are all *social*, which is exactly why
writing more code cannot close them. A note on the order of work: two
implementations and a 36-package cross-check existed in `uibc-core` for six
days while the public repositories still described cross-implementation as
missing. Publication lag, not capability, was the gap; that is also social.

## 3. The smallest submission, defined

A submission reuses the schema that already exists rather than a new one:
`uibc-core/benchmarks/submissions/uibc-<impl>@<commit>.json` (`uibc-bench/1`),
which already carries implementation name, submitter, commit, machine, the
verifier command, per-case outcomes with the raw exit codes, and a
`claim.not_claimed` list the submitter has to write themselves. Two additions
are proposed, both because the existing record cannot answer a question a reader
will ask:

1. `legal_entity` and `contact` — who is accountable for the run. Without it
   a submission is an anonymous claim with a commit hash.
2. `corpus_digest` — the `FIXTURES.sha256` digest the run was produced
   against, so a listing can be tied to a corpus version instead of a date.
3. `competence_basis` — who ran it and on what standing: a laboratory with an
   accreditation number, a named person with a qualification, or the literal
   `none`. A reviewer of a verification record asks this before asking whether
   anything passed; a record that omits it reads as adequate when it is merely
   silent.
4. `witness` — `null` or an object naming who watched, with an
   `independent_of_submitter` flag. The key must be present even when the value
   is `null`, because "no witness" and "we did not think about it" are different
   statements and only one of them is reviewable. A named witness must also ship
   `witness/statement.json` and `witness/witness.key.pub`: an Ed25519-signed
   statement over its own canonical bytes, naming the same person as the product
   record, attesting to the **same** `corpus_digest` as the results it
   accompanies, and signed by a key that neither this repository publishes nor
   the submitter declares. Identity is checked before the signature, because the
   attack this rule exists for is a submitter signing for their own witness.
   What a signed statement proves is that it came from a key the submitter does
   not hold. It does not prove the witness exists, watched anything, or is
   accredited — a signature is an identity, not a credibility.
5. `scope.not_covered` — the checks the submitter does not claim. Every check
   id in `S1`-`S19` must be either claimed or disclaimed, exactly once.
   Silence about a check reads as coverage.

The run log stays unedited and attached; a tidied log is refused, because the
noise is part of the evidence.

This is no longer a description of what a submission should look like. It is
enforced: `UIBC/vectors/tools/check_submission.py` refuses a missing product
record, a self-declared `independent` from this organisation's own entity, a
corpus digest that is not the one committed here, a missing, re-scored,
duplicated or invented case, a log under 200 bytes, a check id outside
`S1`-`S19`, a missing or empty competence basis, a submission that does not
mention its witness at all, a check silently left out of both lists, a named
witness with no signed statement behind it, a witness signature that does not
verify, a statement signed by a key this repository publishes or by the
submitter's own key. `--selftest` breaks the format thirteen ways and requires
all thirteen to be caught — and requires one honestly signed witness to be
accepted, so that the rule is a check and not a wall.

Three of those rules refuse silence rather than a bad answer, and that is
deliberate: writing `none` is accepted, writing nothing is not. An honest
absence can be checked by a reader who asks why; an omission cannot be checked
at all. Our own first row therefore states `competence_basis: none` and
`witness: null` in the record itself rather than leaving a reader to infer it
from the prose.

The first row in that table is a submission by this corpus's own author,
labelled `same-maintainer`. External submissions remain zero.

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


