## What this changes

Four edits to the draft, one ledger row.

**1. S19 is now in Section 5.** The table listed S1–S18 while the reference verifier runs S19. The new row says what it applies to: only when the verifier was given a state record.

**2. New Section 7.5 says what S19 actually does**, written after measuring, not before.

**3. New Section 7.6 bounds the baseline.** The high-water mark has to start somewhere; these two rules decide where, and both are testable.

**4. New Appendix D reserves error codes**, plus the abstract and STATUS edits.

## What was measured first (`uibc-core` 0.5.0, `vectors/full`)

| input | overall | S19 | detail | state written |
|---|---|---|---|---|
| no file | `INCONCLUSIVE` | `INCONCLUSIVE` | first observation, no high-water mark | **yes** |
| `{}` | `FAIL` | `FAIL` | state file unreadable | no |
| `{"subjects":{}}` | `INCONCLUSIVE` | `INCONCLUSIVE` | first observation | yes |
| same head again | `PASS` | `PASS` | same head as the last accepted observation | — |
| different head | `INCONCLUSIVE` | `INCONCLUSIVE` | cannot be placed before or after | **no** |
| **rejected package, fresh state** | `FAIL` | `INCONCLUSIVE` | "first observation" | **yes** |

Two facts come out of this that the draft did not say anywhere:

- The marker is **durable**: a different head does not replace it, so re-presenting the original head still returns `PASS`. That is the property that makes "replay marker" a fair description rather than a euphemism.
- The marker can be **set by a package that failed**. `vectors/tampered` returns `FAIL` overall, yet writes the baseline; a later presentation of that same rejected head is then `PASS` with the detail "last accepted observation". Section 7.6 forbids this, and the code does it anyway — recorded in STATUS as a gap, not papered over.

## Section 7.5, in one line each

- S19 answers *"has this exact head been accepted before by this verifier?"* — and a report MUST NOT call it rollback protection.
- Rollback is S9's out-of-band head; a hash carries no order, so a new head is `INCONCLUSIVE` rather than "newer" or "older".
- `head_sequence` is named as what would make rollback decidable, with the three questions any such revision must answer, so the ambiguity does not simply move down a level.
- Freeze is out of scope, stated as such.

## Section 7.6, in one line each

- Only an accepted package may set the baseline.
- A marker, once written, MUST NOT be replaced by a head that cannot be placed.

Both come with the corpus fixtures they imply, described but not yet added: one package a rejected head, then check the next verdict is not `PASS`; one present a second head, then re-present the first.

## Appendix D

Namespace `E-<DOMAIN>-<N>`, nine codes reserved (`E-FRESH-1..4`, `E-B64-1`, `E-LC-1..4`). The appendix states plainly that **none of them is emitted by 0.5.0**: today the fourth freshness case is `INCONCLUSIVE` with prose in `detail`. A code becomes normative when an implementation emits it and the corpus pins the mapping. This is a reservation, not a description of current output.

## Measurement

`tools/spec_parity.py` in `UIBC/vectors`, run against this file:

```
named in the specification:        19/19   (was 18/19)
normatively governed (MUST/SHOULD): 2/19   (was 1/19)
error codes reserved in the spec:     9   (was 0)
error codes emitted by uibc-core:     0
checks with undefined terminology:    9   (unchanged)
```

A sentence counts as naming a check only if it names the check ID or uses a term unique to that check (≤5 occurrences in the whole draft); generic words such as `package` and `root` do not count. That rule is why the first version of the measurement said 2/19 before it said 1/19: §7's sentence about revocation was matching S5 through the word `root`.

## What this does not do

- No `head_sequence`. Structural change with its own corpus work (a reversed-sequence fixture that must fail), tracked separately.
- No change to `uibc-core`. Eighteen checks still carry no stable code; Appendix D reserves the names only.
- No claim of conformance to anything. Draft stays non-normative and unsubmitted.

## Why now

A check that exists in code and nowhere in the text is worse than a check that does not exist: the implementation becomes the only definition, and the only reader who can learn it is one reading Python. The nine checks with single-use terminology are the same defect in smaller pieces — S3's `contiguous`, S14's `pad-bit`, S7's `agreement` — and Sections 7.5/7.6 are the template for fixing them.
