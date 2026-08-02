# Risk register (optional)

Read this file only when the tracker's `Risk register:` line is `on`, or when the user is setting
it up or asking to change it. If a project has `Risk register: off` (or the line is simply
absent), none of this applies and you never need to read it.

The idea: some ideas ship clean, some come back — a bug fix, a rework, a repeat
`ineffective`/`partial` outcome in the same part of the project. That recurrence is a signal about *where this project
needs more rigor*, not just a fact about one idea. This loop names that pattern once, persists it,
and feeds it back into future proposals so the same kind of risk gets flagged before it repeats a
third time, not just noticed after the fact.

This is a genuinely separate concern from the rest of the skill's steady-state loop — different
question ("where's the risk" vs. "what's next"), different write target, multiple independent
entry points — so it lives in its own sibling file, `RISK_REGISTER.md`, rather than growing
`IMPROVEMENT_TRACKER.md`'s own sections.

**It stays a companion file of this skill, but is deliberately built not to depend on being one.**
A risk area is a property of the project, not of anyone's backlog, and shipped ideas are only one
of the things that could evidence one — a debugging session, a review, a flaky test would all do.
So entries key on `areas:` (see below) rather than on idea ids: what a risk *is* and what it covers
stay readable with no tracker present.

**One field is still tracker-coupled: `mitigated-by:`, which carries an idea id.** Without an
`IMPROVEMENT_TRACKER.md` that id resolves to nothing, so name the intended fix in the entry's own
note as well when there's any doubt a reader could look it up. That's the honest limit of the
standalone claim — everything else in an entry stands on its own.

What keeps this a companion file for now is that every trigger below is still a next-improvement
event, and mitigation outcomes ride on `feedback.md`'s check-in machinery rather than any of their
own. **The tripwire for splitting it out into its own skill: a reason to run that doesn't start
with "what should we build next" — auditing risk areas directly, or evidence arriving from outside
this loop.** Size alone isn't the signal.

## File format

`RISK_REGISTER.md`, in whatever directory `IMPROVEMENT_TRACKER.md` was resolved to — it follows
the tracker rather than being looked up on its own — created the first time it's actually needed
(setup, or the first trigger below if the project turns this on mid-stream):

```markdown
# <Project> — Risk Register
Next id: R<N>

## Active
- **Theme** (id: R1, status: active) — areas: src/sync/, retry logic anywhere —
  mitigated-by: I23 (outcome: pending) — one-line note on the pattern and what it actually is.
- **Theme B** (id: R3, status: active) — areas: the CSV export path —
  mitigated-by: I31 (outcome: planned) — a fix is already proposed but not yet built.

## Archived
- **Theme** (id: R2, status: archived) — areas: db/migrations/ —
  mitigated-by: I19 (outcome: effective) — archived <YYYY-MM-DD>: mitigation held, no new
  evidence since.
```

- **Own id space (`R<N>`)**, own counter (`Next id:` at the top of this file), never reused —
  distinct from ideas' `I<N>` ids (`SKILL.md`) because a risk area is a different kind of thing
  (a persisted pattern, not a buildable candidate), not a case of inventing a parallel scheme for
  the same concept.
- **`status: active` | `archived`** — archived entries are preserved, not deleted, and excluded
  from the routine cross-reference checks below; see Archival.
- **`areas:`** — **the join key: what part of the project this risk is actually about**, named
  concretely enough to match against — file paths, directories, a module, or a named subsystem
  where no path fits ("the CSV export path", "anything touching retry logic"). Everything that
  consumes this file matches on areas, so a vague area ("the codebase", "quality") makes the entry
  unusable; push for something a candidate can be checked against.
  - **Deliberately not idea ids.** An area is a durable property of the project; an idea id is a
    row in one particular tracker. Keying on areas means an entry stays meaningful when the idea
    that evidenced it is reworded, archived, or dropped, when the tracker is hand-edited, and when
    there's no `IMPROVEMENT_TRACKER.md` at all — evidence can come from a debugging session or a
    review just as legitimately as from a shipped idea.
  - **Which ideas are currently exposed is computed, never stored.** Exposure is recomputed
    wherever it's needed, the same way the evidence scan below is. There's no `at-risk:` list to
    add to, drop from, or repopulate, and so no way for one to go stale — which is why nothing in
    this file ever writes one; the flag at the point of use is the whole output. A register written
    before this change may still carry an `at-risk:` field — ignore it on read, drop it the next
    time that entry is rewritten for another reason; don't do a bulk pass.

- **`mitigated-by:`** — id(s) of idea(s) built, or *intended*, *specifically to address* this
  risk, each with its own `outcome:` value: `planned`/`pending`/`effective`/`partial`/
  `ineffective`. `planned` is this field's own first state, for an idea that's still outstanding —
  proposed at Step 2 specifically as the fix for this risk, not yet built. The remaining three
  (`effective`/`partial`/`ineffective`) share `feedback.md`'s ship-outcome wording and reuse its
  check-in mechanics once it ships — see Recording a planned mitigation and Checking on mitigations
  below. **This one *is* stored, unlike exposure**
  — "meant to fix this" is a judgement someone made, not something recomputable from what a
  candidate touches, and it's the only field carrying an idea id. Keep the distinction sharp in
  reasoning text: merely touching an area is "exposed to this," a `mitigated-by:` tag is "meant to
  fix this, whether or not it's shipped yet" (`SKILL.md` Step 3/4 already calls this out).
- **No `cause:`/`fixes:` list is stored on the entry.** Which specific `fixes:`/`reworked:` links
  originally evidenced the pattern is cheap to recompute on demand — scan Done for links whose
  origin touches this entry's areas — so it isn't persisted here; storing it would
  just be a second copy to keep in sync every time a new link lands. Scan Done per the combined-pool
  rule (`SKILL.md` Step 6's "Reading the archive") — evidence for an old, slow-moving risk pattern
  is exactly the kind of thing likely to have aged into the archive by the time it matters, and
  missing it there would undercount evidence or, worse, wrongly clear an active entry for archival
  on a false "nothing new" read. When reasoning about an entry (Step 2/3/4, or deciding whether to
  archive), pull that evidence live rather than trusting a stored snapshot.

## The area match

**One test, used everywhere.** Every check in this file and in `SKILL.md` Steps 2/3/4/6 that asks
"does this touch the risk" means exactly this test — don't improvise a second version per call
site. It's a judgement, not a string comparison: `src/sync/` matches any file under it, and a named
subsystem ("the CSV export path") matches by meaning, not by wording.

What gets matched depends on what the thing *is*:

- **An outstanding idea** hasn't been built, so there are no files to compare. Match on what its
  own rationale names — files, functions, modules it says it will touch — plus what the idea
  plainly implies even when unstated ("add retry to the sync job" is in `src/sync/` whether or not
  the rationale spells that out).
- **A shipped idea** (evidence scans, archival judgements) matches on what it actually changed,
  which is better evidence than what it originally proposed to change.

Two outcomes that are neither "matched" nor "didn't match", and neither collapses into one:

- **The idea is too vague to place.** If a rationale names nothing concrete and implies nothing
  specific, don't guess in either direction — say so when presenting it. An idea too vague to
  locate is usually too vague to rank, which is worth surfacing at Step 2 regardless of any risk.
- **The area no longer resolves** — see Re-grounding areas below.

When a match is genuinely borderline, present it as borderline rather than resolving it silently
in either direction.

## Re-grounding areas

An `areas:` value is a claim about how the project is laid out, recorded once and true at the time.
Refactors move things. **A stale area fails silently — it just stops matching anything, forever** —
which is worse than a reference that breaks loudly, because the entry goes on looking healthy while
protecting nothing.

So whenever an entry is actually in hand for something (a Step 2 cross-reference, an archival
judgement) and its areas name concrete paths, check those paths still exist. It's cheap at that
point, and it only ever runs on entries already in play — never as a sweep. A path that no longer
resolves is a third state, not a no-match: say so and ask, since it means either the code moved
(update `areas:`) or the risk is obsolete (propose archiving), and those need different answers.

## Malformed file

`RISK_REGISTER.md` can exist but not parse (a missing `Next id:`, an entry outside `## Active`/
`## Archived`, an unrecognised `status:` value, or **any** entry with no `areas:` at all — nothing
can be matched against it). Archived entries count here too, not just active ones: an archived
entry with no areas can never be reactivated, since reactivation is itself an area match, so it's
silently dead rather than dormant — and archived entries are the likeliest to predate the field.
Same "unreachable isn't resolved" treatment as
`IMPROVEMENT_TRACKER.md`'s own malformed-tracker case (`session-start.md` Step 0): don't silently
reinterpret or rewrite it, and don't refuse to proceed either. Name the specific thing that doesn't
parse and ask directly, same as the tracker's own handling. `Next id:` missing specifically isn't
this case — see `tracker-maintenance.md`'s "Minting and migrating ids", which applies here too.

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
in `SKILL.md`): show the proposed theme, **the concrete areas it covers**, and the evidence, then
wait for confirmation before writing to `RISK_REGISTER.md`, same gate as Step 2's new-idea
proposals. The areas are the part worth actually negotiating rather than assuming — they're what
every later check matches against, so "which files/modules is this really about?" is the question
to ask if the evidence doesn't already make it obvious. Five independent triggers can start this,
all funneling through the same proposal format and the same gate — a repeat pattern doesn't care
which trigger noticed it first:

1. **`SKILL.md` Step 6, a `fixes:`/`reworked:` link lands.** If this is the 2nd+ link touching the
   same area (or the same specific earlier idea), propose creating a new entry if no entry covers
   that pattern yet. If one already does, there's usually nothing to write — the new link is
   evidence, and evidence isn't stored on the entry (see the no-`cause:`-list note above), so it
   gets recomputed on demand rather than appended. Two exceptions: if the matching entry was
   archived, this is a reactivation proposal (see Archival and reactivation); and if the new
   evidence lands *near* an entry's areas without matching them, propose either widening `areas:`
   or opening a separate entry — don't silently count it against the existing one. **Which of the
   two turns on whether it's the same underlying cause**, not on how close the paths are: the same
   fragility reaching one module further is a widening; a different failure that happens to live
   next door is its own entry, and merging them produces a theme too broad to act on. Say which
   reading you're proposing and why, so the user can correct it.
2. **`feedback.md`, an `ineffective`/`partial`/`reverted` outcome is recorded.** For
   `ineffective`/`partial`: the same areas showing a *repeat* of bad outcomes, even with no
   explicit fix link yet, is earlier/softer evidence of the same shape — propose the same way as
   trigger 1. For `reverted`: propose
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

Distinct from trigger 1's ordinary same-area evidence: if the id getting a `fixes:`/
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

Before presenting a newly-proposed idea, check whether it touches any **active** entry's `areas:`.
On a match, say so as part of presenting the idea (not a separate confirmation step) — e.g. "this
also touches R1 — <theme> — past ships here needed 2 follow-up fixes, worth extra care on scope/
tests upfront." Then, **for each matching entry separately** (a candidate can match more than one —
it may be the intended fix for one and merely exposed to another; don't ask one global question
covering all matches at once), ask the exposed-vs-fix follow-up: is this candidate merely *exposed*
to that risk, or *meant to fix it*?

- **Exposed, not a fix** (the normal case): the flag is the whole output — whether spoken or kept
  as a short note in the idea's own rationale once appended, it names the theme alongside the id
  (`Touches R2 — settings-panel density`), never the bare id on its own.
- **Meant to fix it**: if the user accepts the idea, tag it `mitigated-by: I<N> (outcome: planned)`
  on that entry — this is the idea's status *before* it's built, distinct from the `pending` it
  gets once shipped (see Recording a planned mitigation below). This is a real write, so it goes
  through the confirm gate along with appending the idea itself.

Archived entries are skipped for this check — that's the point of archiving; a new match against an
archived theme is instead a **reactivation** trigger (see below), not a routine caution or a new
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
`effective` **and** no new evidence has landed in that entry's areas since (no new `fixes:`/
`reworked:` link, no new `ineffective`/`partial`/`reverted` outcome, checked live per the "no stored cause
list" note above). On confirmation: flip `status: active → archived`, move the entry from
`## Active` to `## Archived`, and note the archival date and reason inline. Outstanding ideas stop
being flagged against it automatically, since the cross-reference only looks at active entries.

**Don't archive while any `mitigated-by:` on that entry is still `outcome: planned`.** A fix is
already in flight — archiving now would mean Step 6's flip-check (which only scans **active**
entries for a matching `planned` tag) could never find it once it ships, leaving that mitigation
permanently stuck. Wait for it to ship and reach a real outcome (or get dropped, see the note below)
before considering archival, even if a separate, earlier `mitigated-by:` on the same entry already
came back `effective`.

**A clean ship in an entry's areas is counter-evidence too** (`SKILL.md` Step 6): if an idea
touching an active entry's areas ships with no `fixes:`/`reworked:` tag of its own, that's one data
point against the risk being live — worth factoring into the next archival judgement even without a
formal `mitigated-by:` entry, though it doesn't trigger archival by itself the way an `effective`
mitigation does. It's read out of Done at archival time, per the area match.

**New evidence against an archived entry** (a `fixes:`/`reworked:` link or `ineffective`/`partial`/
`reverted` outcome lands in its areas again) is a **reactivation** proposal, not a silent flip —
same confirm gate: "R2 (<theme>) was archived on <date> — <new evidence> suggests it's back, reopen
it?" On confirmation, flip `status: archived → active` and move it back to `## Active`; it's an
ordinary active entry from there, and every already-outstanding idea in those areas starts matching
again immediately.

## Using active entries (from `SKILL.md` Step 3/4)

A candidate that's tagged `mitigated-by:` an active entry gets that named as a positive reason in
Step 3/4's reasoning ("mitigates R1 — <theme>"); one that merely touches an active entry's areas
gets named as a caution the same way ("touches R1 — <theme>"), not a point in its favour. Always
name the theme alongside the id, never the bare id — see the id-labeling rule in `SKILL.md`'s
tracker-format notes. For how either weighs against the other tie-break signals, see `SKILL.md`
Step 3's precedence ladder — that's the canonical ordering, not restated here.
