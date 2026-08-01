# Risk register (optional)

Read this file only when the tracker's `Risk register:` line is `on`, or when the user is setting
it up or asking to change it. If a project has `Risk register: off` (or the line is simply
absent), none of this applies and you never need to read it.

The idea: some ideas ship clean, some come back — a bug fix, a rework, a repeat `missed`/`mixed`
outcome in the same category. That recurrence is a signal about *where this project needs more
rigor*, not just a fact about one idea. This loop names that pattern once, persists it, and feeds
it back into future proposals so the same kind of risk gets flagged before it repeats a third time,
not just noticed after the fact.

This is a genuinely separate concern from the rest of the skill's steady-state loop — different
question ("where's the risk" vs. "what's next"), different write target, multiple independent
entry points — so it lives in its own sibling file, `RISK_REGISTER.md`, rather than growing
`IMPROVEMENT_TRACKER.md`'s own sections. It still only exists to serve next-improvement's Step 2-4
proposals, so it stays a companion file of this skill rather than a separate skill.

## File format

`RISK_REGISTER.md`, same directory as `IMPROVEMENT_TRACKER.md`, created the first time it's
actually needed (setup, or the first trigger below if the project turns this on mid-stream):

```markdown
# <Project> — Risk Register
Next id: R<N>

## Active
- **Theme** (Category, id: R1, status: active) — at-risk: I7, I12; mitigated-by: I23 (outcome:
  pending) — one-line note on the pattern and what it actually is.
- **Theme B** (Category, id: R3, status: active) — at-risk: (none); mitigated-by: I31 (outcome:
  planned) — a fix is already proposed (I31) but not yet built.

## Archived
- **Theme** (Category, id: R2, status: archived) — at-risk: (none); mitigated-by: I19 (outcome:
  effective) — archived <YYYY-MM-DD>: mitigation held, no new evidence since.
```

- **Own id space (`R<N>`)**, own counter (`Next id:` at the top of this file), never reused —
  distinct from ideas' `I<N>` ids (`SKILL.md`) because a risk area is a different kind of thing
  (a persisted pattern, not a buildable candidate), not a case of inventing a parallel scheme for
  the same concept.
- **`status: active` | `archived`** — archived entries are preserved, not deleted, and excluded
  from the routine cross-reference checks below; see Archival.
- **`at-risk:`** — ids of currently *outstanding* ideas judged to share this risk (same
  category/theme/cause). References ideas by id, not name, for the same reason `fixes:`/
  `reworked:` do (`SKILL.md`) — a name can get reworded, an id can't drift.
- **`mitigated-by:`** — id(s) of idea(s) built, or *intended*, *specifically to address* this
  risk, each with its own `outcome:` value: `planned`/`pending`/`effective`/`partial`/
  `ineffective`. `planned` is this field's own first state, for an idea that's still outstanding —
  proposed at Step 2 specifically as the fix for this risk, not yet built. The remaining four reuse
  `feedback.md`'s exact ship-outcome vocabulary and check-in mechanics once it ships — see Recording
  a planned mitigation and Checking on mitigations below. Distinct meaning from `at-risk:`: `at-risk`
  is "exposed to this," `mitigated-by` is "meant to fix this, whether or not it's shipped yet" —
  don't conflate the two in reasoning text (`SKILL.md` Step 3/4 already calls this out).
- **No `cause:`/`fixes:` list is stored on the entry.** Which specific `fixes:`/`reworked:` links
  originally evidenced the pattern is cheap to recompute on demand — scan Done for links whose
  origin's category matches this entry's category — so it isn't persisted here; storing it would
  just be a second copy to keep in sync every time a new link lands. **Scan both the live
  tracker's Done section and `IMPROVEMENT_TRACKER_DONE.md` if it exists** — same combined-pool
  treatment `feedback.md` already applies to its own outcome checks (`SKILL.md`'s "Reading the
  archive" note): evidence for an old, slow-moving risk pattern is exactly the kind of thing that's
  likely to have aged into the archive by the time it matters, and missing it there would silently
  undercount evidence or, worse, wrongly clear an active entry for archival on a false "nothing new"
  read. When reasoning about an entry (Step 2/3/4, or deciding whether to archive), pull that
  evidence live from both files rather than trusting a stored snapshot or only checking the live
  one.

## Malformed file

`RISK_REGISTER.md` can exist but not parse (a missing `Next id:`, an entry outside `## Active`/
`## Archived`, an unrecognised `status:` value) — same "unreachable isn't resolved" treatment as
`IMPROVEMENT_TRACKER.md`'s own malformed-tracker case (`session-start.md` Step 0): don't silently
reinterpret or rewrite it, and don't refuse to proceed either. Name the specific thing that doesn't
parse and ask directly, same as the tracker's own handling. `Next id:` missing specifically isn't
this case — see `SKILL.md`'s lazy-initialization rule, which applies here too.

## Setup (from `setup.md`)

Ask one short yes/no alongside the `Selection strategy:`/`Feedback:` questions: want the skill to
track recurring risk patterns (repeat fixes, reworks, or bad outcomes in the same area) as a named,
persisted risk register that future proposals get checked against? Default `Risk register: off` —
unlike `Feedback:`, this one defaults off, since it only pays for itself once a project has enough
shipped history to show a repeat pattern; a brand-new project has nothing to register yet. Offer to
turn it on any time later once that's no longer true, same lightweight edit-in-place as
`Selection strategy:`/`Feedback:` (`session-start.md` Step 0.5).

## Creating or updating an entry

**Always a proposal, never a silent write** — this is one of the skill's hard rules (see the table
in `SKILL.md`): show the proposed theme, category, and evidence, and wait for confirmation before
writing to `RISK_REGISTER.md`, same gate as Step 2's new-idea proposals. Five independent triggers
can start this, all funneling through the same proposal format and the same gate — a repeat pattern
doesn't care which trigger noticed it first:

1. **`SKILL.md` Step 6, a `fixes:`/`reworked:` link lands.** If this is the 2nd+ link into the same
   category (or the same specific earlier idea), propose creating a new entry (first pattern) or
   extending an existing one (add the new fix's evidence isn't stored, but do re-open `status:
   archived → active` if the matching entry was archived — see Reactivation).
2. **`feedback.md`, a `missed`/`mixed`/`reverted` outcome is recorded.** For `missed`/`mixed`: same
   category showing a *repeat* of bad outcomes, even with no explicit fix link yet, is earlier/
   softer evidence of the same shape — propose the same way as trigger 1. For `reverted`: propose
   on the **first** occurrence, no repeat needed — an idea getting actively undone is strong enough
   evidence on its own, unlike a merely-disappointing outcome.
3. **`SKILL.md` Step 2's fragile-scan** turns up a *structural* pattern (not one isolated rough
   spot) while brainstorming — propose directly, don't wait for it to actually break first.
4. **`SKILL.md` Step 4.5**, planning a confirmed pick exposes a risk that wasn't visible before
   (fragile coupling, an untested assumption) — propose right there rather than waiting for a
   future fix to retroactively prove it.
5. **Ad hoc, any time** — the user names a risk directly ("flag X as a risk area"), same as Goals'
   "reprioritise" jump (`session-start.md` Step 0.5) — no need to wait for a mechanical trigger.

### A mitigation needing its own fix

Distinct from trigger 1's ordinary same-category evidence: if the id getting a `fixes:`/
`reworked:` link (`SKILL.md` Step 6) is itself tagged `mitigated-by:` on some risk entry — the
thing that was supposed to fix that risk just needed fixing itself — that's not just another data
point toward a *new* pattern, it's direct evidence the *existing* mitigation didn't hold. Handle it
as its own case, not folded into trigger 1's generic "2nd+ link" counting:

- If that `mitigated-by:` was `effective` or `partial`, propose downgrading it — to `partial` or
  `ineffective` respectively — rather than leaving the old rating standing next to contradicting
  evidence. This is a reassessment, same confirm-before-write gate as any other risk-register
  change, not a silent overwrite.
- If the risk entry had already been archived on the strength of that mitigation, this is also a
  **reactivation** trigger (see Archival and reactivation below) — the evidence that justified
  archiving it just got contradicted.
- If it was still `pending`, this is simply strong early signal for however that check-in eventually
  resolves — mention it when the outcome check finally happens rather than pre-deciding the answer.

## Cross-referencing new ideas (from `SKILL.md` Step 2)

Before presenting a newly-proposed idea, check it against every **active** entry's category/theme.
On a match, say so as part of presenting the idea (not a separate confirmation step) — e.g. "this
also touches R1 — <theme> — past ships here needed 2 follow-up fixes, worth extra care on scope/
tests upfront." Then, **for each matching entry separately** (a candidate can match more than one —
it may be the intended fix for one and merely exposed to another; don't ask one global question
covering all matches at once), ask the exposed-vs-fix follow-up: is this candidate merely *exposed*
to that risk, or *meant to fix it*? The answer decides which field it goes in, per entry:

- **Exposed, not a fix** (the normal case): if the user accepts the idea, add its id to that
  entry's `at-risk:` list in the same write as appending the idea itself.
- **Meant to fix it**: if the user accepts the idea, tag it `mitigated-by: I<N> (outcome: planned)`
  on that entry instead — this is the idea's status *before* it's built, distinct from the
  `pending` it gets once shipped (see Recording a planned mitigation below). Don't also add it to
  the same entry's `at-risk:` — for *that entry* it's either the fix or exposed, not both (it can
  still be `at-risk:` on a *different* matching entry).

Archived entries are skipped for this check — that's the point of archiving; a new match against an
archived theme is instead a **reactivation** trigger (see below), not a routine at-risk tag or a new
planned mitigation.

## Recording a planned mitigation (from `SKILL.md` Step 6)

A `mitigated-by:` entry tagged `outcome: planned` was proposed at Step 2 specifically to fix an
active risk, but hasn't shipped yet. When *that specific idea* is the one being recorded in Step 6,
flip `outcome: planned → pending` on the risk entry (not a new tag — the same `mitigated-by: I<N>`
reference, just its state advancing) — this is what starts the real wait/bulk outcome-check timing
from the actual ship date, same as any other mitigation reaching `pending`. If the idea shipped in a
substantially different shape than originally planned, or turned out not to actually address the
risk, say so rather than mechanically flipping the state — that's a judgement call worth a word, not
silent bookkeeping.

## Checking on mitigations

A `planned` mitigation isn't eligible for any check-in yet — it hasn't shipped, so there's nothing
to ask about (see Recording a planned mitigation above for how it becomes `pending`). Everything
below applies from `pending` onward only.

A `mitigated-by:` idea's `outcome:` follows the exact same eligibility/check-in machinery as
`feedback.md`'s ship outcomes (`wait`/`bulk`/`batch` windows, drip/batched/continuous-drip/
all-at-once offer, once-per-session throttle) — don't build a parallel mechanism, extend that one:
when `feedback.md`'s check-in reaches a Done entry that's also tagged as some risk entry's
`mitigated-by:`, ask about it using the *risk* vocabulary instead of the generic one ("did R1 stay
quiet since this shipped, or has it recurred?") and write the answer as that risk entry's
`mitigated-by: I23 (outcome: <answer>)`, not as the idea's own `outcome:` field (the idea already
has its own routine outcome from the ordinary feedback loop, if `Feedback:` is also on — the two
are separate judgements about the same ship: did it deliver, and did it actually fix the risk).

**This is a hard dependency on `Feedback: on`.** `feedback.md`'s check-in only runs from
`session-start.md` Step 0.5 when `Feedback:` is on — if `Risk register: on` and `Feedback: off`,
there is no periodic mechanism to ever ask about a `mitigated-by:` outcome, and it would sit at
`pending` indefinitely with nothing surfacing that fact. Don't silently let this happen: if a
project has `Risk register: on` while `Feedback:` is off, say so the first time a `mitigated-by:`
tag would be added ("mitigation outcomes need `Feedback: on` to ever get checked — turn it on too,
or this one will just stay `pending`?") and let the user decide, same as any other setup-time
disclosure rather than a silently-dead feature.

## Archival and reactivation

**Propose archiving** (confirm gate, same as creation) when a `mitigated-by:` entry is assessed
`effective` **and** no new evidence has landed against that category since (no new `fixes:`/
`reworked:` link, no new `missed`/`mixed`/`reverted` outcome, checked live per the "no stored cause list"
note above). On confirmation: flip `status: active → archived`, move the entry from `## Active` to
`## Archived`, clear its `at-risk:` list (outstanding ideas stop being flagged against a resolved
risk), and note the archival date and reason inline.

**Don't archive while any `mitigated-by:` on that entry is still `outcome: planned`.** A fix is
already in flight — archiving now would mean Step 6's flip-check (which only scans **active**
entries for a matching `planned` tag) could never find it once it ships, leaving that mitigation
permanently stuck. Wait for it to ship and reach a real outcome (or get dropped, see the note below)
before considering archival, even if a separate, earlier `mitigated-by:` on the same entry already
came back `effective`.

**A clean ship of an `at-risk:`-tagged idea is counter-evidence too** (`SKILL.md` Step 6): if an
idea on an active entry's `at-risk:` list ships with no `fixes:`/`reworked:` tag of its own, that's
one data point against the risk being live — worth factoring into the next archival judgement even
without a formal `mitigated-by:` entry, though it doesn't trigger archival by itself the way an
`effective` mitigation does.

**New evidence against an archived entry** (a `fixes:`/`reworked:` link or `missed`/`mixed`/
`reverted` outcome lands in that category again) is a **reactivation** proposal, not a silent flip — same
confirm gate: "R2 (<theme>) was archived on <date> — <new evidence> suggests it's back, reopen it?"
On confirmation, flip `status: archived → active`, move it back to `## Active`, and — **re-populate
`at-risk:` immediately**, not just going forward: scan the category's currently outstanding ideas
for a match, same check `SKILL.md` Step 2 runs for a newly-proposed idea, and add every match now.
Archival cleared the list, but ideas that were already sitting outstanding in that category the
whole time never went through Step 2's cross-reference (that only fires for *new* proposals), so
without this they'd stay silently untagged until each one happened to get re-touched. Then continue
from there as an ordinary active entry.

## Using active entries (from `SKILL.md` Step 3/4)

A candidate that's tagged `mitigated-by:` an active entry gets that named as a positive reason in
Step 3/4's reasoning, same weight class as a synergy signal but a distinct claim ("mitigates R1").
A candidate that's merely `at-risk:`-tagged gets named as a caution, not a point in its favour.
Neither promotes a candidate across Goals tiers — same rule as synergy (`SKILL.md` Step 3): it
breaks close calls within a tier, it doesn't re-tier anything.
