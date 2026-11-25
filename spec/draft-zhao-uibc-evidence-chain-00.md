# Agent Lifecycle Evidence Chain (UIBC)

## Package Structure, Verification, and External Anchoring

**Local draft — NOT submitted.** This document is written in Internet-Draft
shape so that reviewers can read it the way they read a draft and so that it
can be submitted unchanged if a decision is ever made to do so. It has **not**
been posted to the IETF datatracker, it carries no IETF copyright notice, and
it claims no standards status. Do not cite it as an Internet-Draft.

```
Document name : draft-zhao-uibc-evidence-chain-00
Intended status: Informational (proposed only)
Author        : X. Zhao
Version       : 00 (local, 2026-11-18)
Reference impl: https://github.com/zhaoxinghua09-cell/uibc-core
```

---

## Abstract

An autonomous agent leaves a trail of actions, but that trail is normally
produced, stored and verified by the same party it is supposed to convince.
This document specifies a portable package that binds an agent's identity,
lifecycle, and action evidence into one hash-committed structure, gives an
nineteen-check verification procedure with three-valued outcomes, and
specifies how to commit the resulting root to backends the operator cannot
rewrite. The specification is deliberately narrow: it defines what can be
checked from bytes alone, and it names what it does **not** check.

## 1. Introduction

Three problems recur when an agent's behaviour must be shown to a third party:

1. **Evidence is not citable.** Logs live in a vendor's database, in a format
   that cannot be handed over, with no way to prove that later retrieval
   returned the same bytes.
2. **Truncation is invisible.** A hash chain detects modification and
   reordering; it cannot detect deletion of a tail. A dropped tail verifies
   exactly like a shorter run.
3. **Verification is self-attested.** The party that produced the record also
   judges it, so a passing verdict carries no information.

This document answers each: a byte-level package (Section 3, 4), an
out-of-band head commitment (Section 8), and a verification procedure whose
outcomes include *inconclusive* rather than only pass/fail (Section 5).

Design rule throughout: **a verifier must never invent a fact.** Anything not
derivable from the bytes under test is reported as not-checked, not assumed.

## 2. Conventions and Terminology

The key words MUST, MUST NOT, SHOULD, and MAY are to be interpreted as
described in [RFC2119] and [RFC8174].

- **Package**: a directory of five required JSON files plus an evidence tree.
- **Evidence Root**: SHA-256 over the sorted content hashes (Section 4).
- **Seal**: a signature or MAC over the package's committed state.
- **Outcome**: `PASS`, `FAIL`, or `INCONCLUSIVE`, per check.
- **Anchored**: the root has been committed to an external backend and that
  commitment has been *confirmed* by that backend (see Section 8.2).

## 3. Package Structure

A package contains exactly:

| File | Content |
|---|---|
| `manifest.json` | `agent_id`, `agent_version`, `evidence_count`, `evidence_root`, `status` |
| `identity.json` | `agent_id`, `agent_type`, `owner`, `created_at`, `status`, `version` |
| `lifecycle.json` | ordered events, each with `event_id`, `sequence_number`, `event_type`, `timestamp`, `actor`, `previous_event` |
| `evidence/index.json` | entries: `path`, `media_type`, `content_hash`, `recorded_at`, `action_type` |
| `evidence/files/…` | the evidence bytes themselves |

Undeclared files at the package root are a structural failure (S1). Evidence
files MUST be reachable through an index entry; an unreferenced file is not
evidence.

## 4. Evidence Root

```
root = SHA-256( canonical_json( sorted( entry.content_hash for entry in index ) ) )
```

Canonical form: UTF-8, keys sorted, no insignificant whitespace, no
normalization of string values. The root is stored in `manifest.json` and is
the object that gets anchored, signed, and compared.

Because the root covers content hashes rather than paths, moving a file
without changing its content does not change the root; changing one byte does.

## 5. Verification Procedure

A verifier performs the checks below and reports one outcome per check. A
single `FAIL` makes the verdict `FAIL`; otherwise any `INCONCLUSIVE` makes it
`INCONCLUSIVE`; only all-`PASS` yields `PASS`.

| ID | Check | Notes |
|---|---|---|
| S11 | strict serialization | runs **before** any parse: UTF-8, no duplicate member names, no raw control characters |
| S1 | package structure | required files present, no undeclared root entries |
| S2 | identity consistency | `agent_id` agrees across files; enum fields valid |
| S3 | lifecycle state machine | chain valid, sequence contiguous, timestamps monotonic, actors authorised |
| S4 | evidence integrity | recompute each `content_hash` from the file bytes |
| S12 | timestamp and identifier strictness | values, not hashes: real calendar dates, lowercase UUIDs |
| S13 | merkle inclusion proofs | where the package carries them |
| S14 | strict base64 | canonical spelling, no pad-bit slack |
| S15 | anchor event resolution | where an anchor is claimed |
| S16 | external timestamp (RFC 3161) | where a token is present |
| S17 | linear receipt chain | `prev_digest` continuity, `seq` from 1, closing entry |
| S18 | policy artefact resolution | where a policy reference is present |
| S7 | evidence index metadata | index metadata digest agreement |
| S8 | package checkpoint head | recomputed checkpoint equals stored |
| S9 | head pinned out-of-band | only when the verifier was given an external head |
| S19 | freshness state | only when the verifier was given a state record; answers replay, not rollback (Section 7.5) |
| S10 | attestation closure declared | declarations are recorded, **not** verified |
| S5 | evidence root | recomputed root equals `manifest.evidence_root` |
| S6 | seal signature | Ed25519 verified publicly; HMAC only with the owner key |

S6 is the reason the outcome set has three values: an unsigned package is
internally consistent but its provenance is unattested. Reporting that as
`PASS` would be the single most damaging mistake this document could make, so
the specification forbids it.

## 6. Seal and Key Custody

Two seal types are defined: Ed25519 over canonical package state (publicly
verifiable), and HMAC-SHA256 (verifiable only with the owner key). A verifier
reading a public key out of the package under test proves internal
consistency only — the key could have been swapped with the content. Only an
out-of-band key (or the owner key) lifts that limitation, and even then the
result is *unanchored* until Section 8 applies.

## 7. Gate Outcomes

When a package is presented for a decision rather than a verification, the
outcome set is: `REVOKED`, `DISPUTED`, `MISMATCH`, `MALFORMED`,
`UNVERIFIABLE`. A revocation or dispute MUST name the `target_root` it
applies to and MUST be rejected if that root differs from the package's
current root — otherwise a stale revocation silently applies to new content.

### 7.5 Freshness, and what S19 does not do

A verifier checks `freshness state` (S19) when the caller supplies a state
record, and reports one of three outcomes. This section states what the check
answers, because the answer is narrower than "did this package roll back":

- **no record for the subject** — the freshness check reports `INCONCLUSIVE`.
  The absence of a comparison MUST NOT be reported as `PASS`.
- **record present, `checkpoint_head` equal to the recorded head** — `PASS`.
  The verifier has accepted these exact bytes for this subject before.
- **record present, `checkpoint_head` differs from the recorded head** — the
  check reports `INCONCLUSIVE`, and the report MUST say that the head cannot be
  placed before or after the recorded one. A `checkpoint_head` is a hash, and
  hashes carry no order.

Therefore, in this version of the format:

- S19 answers "has this exact head been accepted before by this verifier?". It
  is a **replay marker**, and a report MUST NOT describe it as rollback
  protection.
- **Rollback is detected by an out-of-band head**, not by S19: see S9
  (`--expect-head`), and Section 5's rule that a check whose comparison is
  impossible reports `INCONCLUSIVE` rather than `PASS`.
- Making rollback decidable requires a monotonic counter in the package
  (a `head_sequence`), which this version does not define. A future revision
  that adds one MUST specify where it lives, how it advances, and what a verifier
  with a lower recorded sequence reports — otherwise the same ambiguity returns
  one level down.
- **Freeze is out of scope.** Nothing here detects a publisher that keeps
  serving the same, valid package. Bounding a freeze needs external publication
  or an anchor (Section 8); a report MUST NOT claim freeze protection.

The state record is local to the verifier and MUST NOT be written into the
package (Section 8.4). A record that cannot be read MUST NOT be treated as "no
prior observation": the two differ, and conflating them turns an unreadable
file into a silent `PASS`.

### 7.6 Recording the baseline

A verifier that keeps freshness state has to acquire a first marker somewhere.
The first presentation of a subject therefore establishes the baseline, and a
second presentation of the same head is `PASS` — trust-on-first-use, with no
claim that the first presentation was the right one. Two rules bound the damage
that a careless baseline can do:

- **Only an accepted package may set the baseline.** A verifier MUST NOT
  record a head for a package that failed any other check. If it does, the
  marker belongs to a package the verifier rejected, and the next legitimate
  package is then reported as `INCONCLUSIVE` while the rejected head can later
  come back as `PASS`, with the report claiming it was "the last accepted
  observation". The reference verifier at 0.5.0 records a baseline for
  packages whose overall outcome is `FAIL`; that is a defect against this
  paragraph, not a licence to rely on it.
- **A marker, once written, MUST NOT be replaced by a head that cannot be
  placed.** The recorded head is durable: presenting a different head, with or
  without a sequence number, leaves the stored baseline intact. A marker that
  the next caller can overwrite is not a marker.

Both rules are cheap to test and belong in a corpus: one fixture packages a
rejected head and then checks that the following verdict is not `PASS`; another
presents a second head and then re-presents the first.


## 8. External Anchoring

### 8.1 What crosses the wire

Only the root. No evidence, no inputs, no outputs, no tool names. A root is a
commitment, not a leak.

### 8.2 Two states, not one

- **pending**: a backend accepted the commitment but it is not yet confirmed
  (an OpenTimestamps calendar attestation before `ots upgrade` matures it
  into a Bitcoin commitment).
- **anchored**: the backend's confirmation has been verified.

A report MUST NOT use the word "anchored" for the pending state.

### 8.3 Backends

Two are specified because one is a single point of censorship:

- **OpenTimestamps calendars** (`POST /digests`, 32-byte body).
- **Nostr relays** (BIP-340 Schnorr signature over a NIP-01 event whose
  `content` carries the root).

Submitting to more than one backend is a SHOULD, not a MUST: availability
differs by jurisdiction.

### 8.4 The proof must not go inside the package

Recording an anchor proof as package evidence changes the package, hence
changes the root — and the root that was anchored is then no longer the root
the package has. Implementations MUST refuse to write proofs into the package
directory. This failure is silent and total; it is the single most likely
implementation error in this section.

## 9. Conformance and Interoperability

An implementation is conformant if it: (a) reproduces the committed test
vectors, (b) reports `INCONCLUSIVE` rather than `PASS` when a check cannot be
resolved, and (c) never accepts a foreign-format document as its own.

Interoperability with AER-1 receipts is defined by an explicit mapping
(Appendix A), not by similarity of intent. The reference implementation
demonstrates both directions: emitting AER-1 receipts that the AER-1
publisher's own runner accepts, and judging external AER-1 receipts
(21 valid accepted, 36 invalid rejected), with 28 documents from two unrelated
protocols rejected without exception.

## 10. Security Considerations

- **Truncation** is undetectable without Section 8; S8 catches truncation
  inside the package, S9 catches replacement by an older self-consistent
  package only when a head is supplied out of band.
- **Key substitution** is detectable only with an out-of-band or owner key.
- **Replay** of an older package is a Section 8.2 problem, not a hash problem.
- **Timestamps** are self-asserted until anchored; S12 checks that they are
  real calendar instants, not that they are true.
- **No behavioural evaluation.** This document says nothing about whether an
  agent acted well, only about whether its record is intact and attributable.
  Confusing the two is the usual overclaim.
- **Threat model boundary**: an adversary who controls the package *and* the
  backend *and* the key has won; nothing here applies.

## 11. IANA Considerations

This document requests no IANA action. No media type registration is
requested at this version.

## 12. References

Normative: [RFC2119], [RFC8174], [RFC3339], [RFC8032], [RFC2104].

Informative: [RFC3161] (external timestamp tokens, S16), [AER1] (`draft-zambo-aer1-26`,
the receipt format this mapping targets), [BIP340] (Schnorr signatures used by
the Nostr backend), [NIP01] (Nostr event serialization).

## Appendix A. Relationship to AER-1

| Aspect | AER-1 | This document |
|---|---|---|
| Unit | one receipt per execution | package: identity + lifecycle + many evidence items |
| Root | Merkle root over step receipt ids | SHA-256 over sorted evidence content hashes |
| Outcome set | accept / reject | PASS / FAIL / INCONCLUSIVE |
| Missing metadata binding | MUST fail (Section 6), not implemented by the publisher's runner | n/a |
| Anchoring | section defined, SDK ships Nostr + OTS | two backends specified, both implemented |

Three claimed spec-versus-corpus divergences were re-audited against the
specification text; two hold (mandatory `metadata_hash` for 0.4 receipts;
integer-valued floats accepted for `seq` but rejected for `entry_count`), and
one was withdrawn as an error of ours. See `docs/AER1-SPEC-AUDIT.md`.

## Appendix B. Test Vectors and Re-running

Reproduction commands live in the reference implementation: `tools/aer1_spec_audit.py`
(corpus audit), `tools/aer1_interop_demo.py` (end-to-end interop),
`tools/anchor_chain_head.py` (OTS), `tools/nostr_anchor.py` (Nostr, checked
against the official BIP-340 vectors committed at `tests/data/bip340-vectors.csv`).

## Appendix C. If This Is Ever Submitted

Nothing in this repository submits it. Doing so would require: an author
email registered with the datatracker, `xml2rfc`-valid source, a chosen
working group or an AD sponsor, and an IPR declaration. Until all four exist,
this file stays a local draft, and any claim that it is "an I-D" is false.

## Appendix D. Error Codes (reserved namespace)

Check results are currently reported as free text in `detail`, which a machine
cannot consume stably and which changes whenever the wording is improved. A
stable code removes that coupling: the code is the contract, the sentence is
courtesy.

The namespace is `E-<DOMAIN>-<N>`, where `DOMAIN` is a short upper-case token
for the area and `N` counts from 1 within it. Two domains are visible in this
draft today:

| code | domain | meaning |
|---|---|---|
| `E-FRESH-1` | freshness | a recorded sequence is lower than the presented one |
| `E-FRESH-2` | freshness | head presented again, unchanged |
| `E-FRESH-3` | freshness | the state record exists but cannot be read |
| `E-FRESH-4` | freshness | a different head arrived with nothing to order it against |
| `E-B64-1` | base64 | padding, alphabet or pad-bit condition violated |
| `E-LC-1` | lifecycle | sequence gap or repeat |
| `E-LC-2` | lifecycle | timestamp regression along the chain |
| `E-LC-3` | lifecycle | actor is not an authorised principal |
| `E-LC-4` | lifecycle | `previous_event` does not name the preceding event |

**None of these codes is emitted by the reference verifier at version 0.5.0.**
This appendix reserves the names so that they can be emitted without a
second rename, and it must not be read as a description of current output:
today `uibc-core` reports S19's fourth case as an `INCONCLUSIVE` result whose
`detail` says the head cannot be placed. A code becomes normative for an
implementation when that implementation emits it, and the corpus pins the
mapping with a fixture — the same rule this document applies to every other
claim.

Codes are also the cheapest way to make the specification checkable: once each
check names the codes it can emit, a table of `check → code` is a conformance
artefact that a third party can implement against without reading anyone's
source.

