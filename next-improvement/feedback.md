# Outcome feedback (optional)

Read this file unless the tracker's `Feedback:` line explicitly says `off`, or whenever the user is
setting it up or asking to change it. **An absent line means `on`** (see `SKILL.md`'s
read-condition note).

The idea: shipped work can look great as a plan and still not deliver. This loop asks, lazily
and cheaply, how past ships actually landed, and feeds that back into future ranking/top-up
judgement — without turning into a nagging, ever-growing chore.

## Tracker format

In the Goals block:

```markdown
Feedback: on(wait=7, bulk=5, batch=5, reoffer=30) (bulk-offer last: <N>, <YYYY-MM-DD>, growth-streak: <N>)
```

`on`/`off`, default `on`. An absent line means `on`, and only a spelled-out `off` disables this.
`off` disables the whole feedback check in `session-start.md`'s Step 0.5: no prompts, no pending
count shown (but see `session-start.md`'s Step 0.6, which still surfaces standalone `reassess:`
flags in that case, since those aren't part of this subsystem).

The four numbers are optional and independently settable. Plain `Feedback: on` with no parens is
equivalent to `Feedback: on(wait=7, bulk=5, batch=5, reoffer=30)` and is the normal way to write
it when none need changing; only spell out the parens when overriding one.
- `wait` (default 7): the eligibility window in days (see Checking in).
- `bulk` (default 5): the bulk-offer threshold.
- `batch` (default: whatever `bulk` is set to, so 5): the chunk size for the batched-offer mode
  (same section). It doesn't silently ride on `bulk`; set it separately if the two should differ,
  e.g. offering in chunks smaller than the threshold that triggers the offer.
- `reoffer` (default 30): the days-based re-offer trigger (see below).

Four unrelated numbers, set independently, same independent-knob treatment as the
`Selection strategy:` counts.

The `(bulk-offer last: N, <date>, growth-streak: <N>)` note records
the eligible-count and date at which the most recent bulk-style offer (all-at-once or batched) was
made or declined — this is what lets Step 0.5 know when to re-offer (see
below); it's a real stored field, not something inferred from the eligible count alone, since that
count fluctuates as items get answered or new ones ship. **"Never offered" is its own state, not a
count of zero.** Write it as `(bulk-offer last: never, growth-streak: 0)`. A first-ever offer has
no previous offer to have grown from, so it's neither growth nor a reset; treating the sentinel as
a real prior measurement of 0 would score every first offer as growth. `growth-streak` counts consecutive offers
where the eligible count was higher than at the previous offer — see "Backlog not shrinking" below.

**If the `Feedback:` line isn't present, write it out before annotating it.** That's the normal
case, since an absent line already means `on`. Write `Feedback: on` with the note attached, the
same way Step 6 writes out an absent `Done archive:` line before annotating its own counter. Both
fields here need it: the counter, and `bulk-offer last:`, which the re-offer trigger reads back.
There's no other line either belongs on, so without this they silently stop being recorded at all.

Done entries extend the base format (see `SKILL.md`, which also covers the `id:`, `fixes:`,
`reworked:`, and `reassess:` fields — those aren't specific to this subsystem) with a ship date and
an `outcome:` value:

```markdown
- I7: **Idea name** (Category, shipped YYYY-MM-DD, outcome: pending) — one-line note...
```

`outcome:` is one of `pending`, `effective`, `partial`, `ineffective`, `reverted`, or `skipped` —
these match `risk-register.md`'s own `mitigated-by:` vocabulary rather than duplicating it under
different words. `effective` = worked as intended; `partial` = landed but with real rough edges or
partial value; `ineffective` = shipped but didn't deliver the intended value at all; `reverted` =
actually undone, a stronger, costlier signal than `ineffective` worth its own tag rather than
folding in; `skipped` = user declined to judge this one. **These definitions are for me, not
something the user is assumed to already know.** See "Checking in" below for where they actually
get told this, not just the Setup question.

## Setup (from `setup.md`)

Ask one short yes/no: want the skill to check back on how shipped work actually landed — effective
(worked as intended), partial (landed but with real rough edges), ineffective (didn't deliver the
intended value), or reverted (actually undone) — at most once per session, starting 7 days after an item
ships, and offered (once 5 are eligible at once) as a choice of all-at-once, in smaller batches,
continuously one at a time, or the default single question, rather than always asked one at a time?
Default `Feedback: on(wait=7, bulk=5, batch=5, reoffer=30)` if they don't care — all four numbers
are changeable later without re-running setup, and it's capped and skippable per the mechanics
below, so opting in is low-risk.

## Recording a ship (from `SKILL.md` Step 6)

When moving an item to Done, extend the base `I<N>: **Idea name** (Category)` line (see `SKILL.md`
for the id itself, which applies regardless of `Feedback:`) with a ship date and `outcome:
pending` inside the parenthetical, e.g. `I7: **Idea name** (Category, shipped YYYY-MM-DD,
outcome: pending)`. The date and the outcome tag are specific to `Feedback: on` — if it's off, use
the plain base format with just the category.

## Checking in (from `session-start.md` Step 0.5)

**Once per session, not once per invocation.** Doing several rounds of this skill back to back in
one sitting re-runs Step 0.5 every round, but the eligible set can't meaningfully change within
that sitting — a Done entry only becomes eligible after `wait` days, so nothing new becomes
eligible mid-session, and anything already answered has already dropped out. Track (in
conversation context only, never written to the tracker — this is exactly the kind of signal that
shouldn't be persisted, since it's only ever useful within the current sitting) whether this
check-in has already surfaced once this session. If it has, skip the rest of this section
entirely on later rounds — no drip question, no bulk offer, no "N ships pending" note, no "nothing
eligible" note either. Silence by default beats a repeat announcement of the same fact. Re-check
normally the next time the skill starts a new session.

A Done entry is **eligible** once it's shipped ≥`wait` days ago (default 7) and still has
`outcome: pending` — enough time has passed to actually judge it. Count them across both Done
files, per the combined-pool rule (`SKILL.md` Step 6's "Reading the archive"): Step 6 archives
entries regardless of `outcome`, so a `pending` entry can be sitting in
`IMPROVEMENT_TRACKER_DONE.md` if this loop hasn't caught up to it yet, and missing it would let the
backlog quietly shrink on paper without anyone answering anything.

- **`reassess: pending` entries take priority over routine eligible items.** A `reassess` flag
  (`SKILL.md` Step 6: a later ship fixed or reworked this one) means the item's original outcome
  judgement may no longer hold. Surfacing that is more valuable than a routine newly-eligible ask,
  so reassess-flagged entries always go first, oldest first, ahead of plain eligible items in every
  mode below. Wording is distinct from a routine ask, and depends on what the origin's outcome
  already was:
  - Still `pending` (never answered): fold the fix/rework into the normal outcome question as one
    clause instead of asking twice. "Last shipped '<idea>' (<date>) — worked as intended, partial,
    ineffective, or was it reverted? (Note: this was later fixed by '<fixing idea>'.)"
  - Already a real answer (`effective`/`partial`/`ineffective`/`reverted`): reopen it explicitly,
    allowing either direction. "'<idea>' was marked <old outcome>, but was later fixed by
    '<fixing idea>' — still <old outcome>, upgrade to effective, or adjust to
    partial/ineffective/reverted?"

  Clear `reassess: pending` the moment it's answered, same as any other eligible item — see
  "Answered items" below.
  - **What the tag measures.** `outcome:` answers one question only: given everything known now,
    did this idea deliver its intended value? It is not a defect record — whether a bug was found
    and fixed later is already preserved permanently and independently via the `fixes:`/`reworked:`
    link on the fixing entry (`SKILL.md` Step 6), regardless of what outcome gets chosen here.
    Don't fold "there was a bug" into the outcome value itself; that fact isn't lost by leaving
    outcome at `effective`, and doesn't need re-litigating by downgrading on principle.
  - **What reassessment is actually for, then.** Not scoring the bug — the fix is evidence the
    *original judgement* might have been made on incomplete information, and reassessment exists to
    check that, not to penalize the idea for having needed a fix. For a `pending` origin, this means
    giving the first-time judgement full context (e.g. did the bug mean the feature genuinely didn't
    deliver value for users during the gap before it was fixed?). For an already-answered origin, it
    means asking whether the original call was actually correct now that more is known (e.g. marked
    `effective`, but did the bug mean it wasn't, even at the time?) — not whether the fix itself
    should move the tag. A same-day, narrow patch (tightening a regex, a one-line guard) rarely
    implies the original judgement was wrong and is rarely reason to move the tag at all.
- **Always surface the count** when it's nonzero, even if nothing else here triggers — e.g. a
  trailing "(3 ships pending feedback, 1 needs reassessment)" note, calling out the reassess subset
  separately since it's a different kind of pending. This is what stops the backlog from silently
  growing unnoticed; a visible number is enough on its own even between prompts. This still only
  fires once per session, per the throttle above — it's about not going silent forever across
  separate sessions, not about repeating every round within one.
- **The first outcome question ever asked for a project includes the tag definitions; later ones
  don't repeat them.** Setup's yes/no already stated them once, but that can be weeks before the
  first Done entry actually becomes eligible — long enough to forget. **The test for "first ever":
  no Done entry anywhere (live tracker or the archive) yet carries a non-`pending` outcome.**
  Detect it cheaply, without a new stored field; it can be computed fresh at no real cost, so
  don't write it down just because it'd be convenient to have. When it's the first real question,
  append the gloss inline — "(effective = worked as intended, partial = landed with real rough
  edges, ineffective = didn't deliver the value, reverted = actually undone)" — to whatever wording
  the mode below would otherwise use. Every later question,
  in any mode, drops it; the tags are self-evident once they've been used once.
- **Every item shown in any mode below gets a why-and-what line, not just name + date.** The
  longer it's been, the harder those two things are to tell apart from memory. Pull both from text
  already stored, nothing new to record: the idea's original one-line rationale (from when it was
  added to its category) and the Done entry's "what actually shipped" note. Format: `"<Idea name>
  (shipped <date>) — proposed: <original rationale>; shipped as: <Done note>."` This applies to the
  drip question, the batched list, the continuous-drip list, and the all-at-once list alike.
- **Below the `bulk` threshold (default 5 eligible)**: single drip. Ask about the one oldest
  eligible item across both files (reassess-flagged first, per above), one short question with the
  why-and-what line above. Any answer, including "skip," gets written back as its `outcome:` value
  immediately (skip -> `outcome: skipped`) in whichever file the item actually lives in (live
  tracker or `IMPROVEMENT_TRACKER_DONE.md`), so that item is never asked about again. At most one
  such question per session, per the throttle above.
- **At or above `bulk`, and either of:**
  - the eligible count exceeds `bulk-offer last:`'s stored count by at least `bulk`, or
  - it's been ≥`reoffer` days since `bulk-offer last:`'s stored date.

  A `never` sentinel satisfies this outright; reaching `bulk` for the first time is itself the
  trigger. Then:
  1. Offer a choice instead of the single drip question: "N ships pending feedback (M need
     reassessment) — clear them all now, N at a time, one-by-one until you say stop, or just the
     oldest for now?"
  2. Whichever is chosen (or declined outright), update `bulk-offer last:`'s count and date to the
     current eligible count and today, immediately.

  The count-based trigger exists so a fast-growing backlog doesn't wait a full month to be
  re-offered; the date-based trigger exists so a stalled backlog that isn't growing (declined once,
  then just sits there) still gets re-surfaced instead of silently waiting for growth that may
  never come.
  - **Backlog not shrinking** — a self-correcting counter, same shape as `SKILL.md` Step 2's
    dry-run tracking. Trigger/increment: before updating the stored count, compare it against
    the current eligible count — if this offer's count is higher than the *previous* offer's,
    increment `growth-streak`. Corrected signal/reset: otherwise, back to 0. **If `bulk-offer last:`
    is `never`, do neither.** Leave the streak at 0 and just record this offer, since there's no
    previous count to compare against. Threshold: `growth-streak: 2` (two consecutive offers where
    the backlog grew instead of shrinking). At the threshold:
    1. Say so plainly as part of the offer: "this backlog's grown across the last two check-ins
       instead of shrinking; want to shorten `reoffer`, shrink `bulk` so it asks more often in
       smaller pieces, or leave it as-is?"
    2. Surface the pattern and ask rather than picking a fix. Whether the right cause is cadence,
       batch size, or the user just not being engaged isn't something to guess at.
    3. Force-reset `growth-streak` to 0 once surfaced, regardless of the answer, same as Step 2's
       dry-run counter.
  - **All at once** — list every eligible item as a numbered list (oldest first across both files,
    reassess-flagged first within that, no cap — see `SKILL.md` Step 4's numbering rule, which
    applies to this list too), each with its why-and-what line, and let the user answer all of them
    in one pass by number (terse per-item tags are fine); write each tag back into whichever file
    that item is actually in — this may mean one edit to the live tracker and one to the archive if
    eligible items span both.
  - **Batched (`batch` at a time, default same as `bulk`)** — same numbered-list treatment, but
    capped to the oldest `batch` items this round. Write back answers for that chunk immediately.
    The remaining eligible items stay pending; the next time this offer fires (this session's
    continuous-drip variant below, or a future session), present the next oldest `batch`-sized
    chunk — don't re-show already-answered items and don't require the user to ask for "the next
    batch" by name, just continue oldest-first from what's left.
  - **Continuous drip** — same single-question format as the below-threshold drip mode, but asked
    back-to-back in this same turn, oldest first, until either the eligible pool (including any
    newly-reassess-flagged items surfaced mid-run) is exhausted or the user says stop. This
    explicitly **suspends** the once-per-session throttle for this run only — that throttle exists
    to stop unsolicited re-asking, not to cap a mode the user just opted into. Whatever's answered
    before they stop is written back same as any other answer; anything left unanswered stays
    pending for next time.
  - **Declined, or threshold condition not yet met** — fall back to single drip mode for this run.
- Answered items (any outcome, including `skipped`) drop out of the eligible count permanently —
  the backlog can only shrink or hold steady between offers, never balloon unnoticed.

## Using the results

Use recorded outcomes qualitatively in `SKILL.md` Step 2 (top-up) and Step 3 (ranking), the same
way existing signals like "what's fragile/rough-edged" are used — e.g. a category with a couple
of `ineffective` outcomes is worth naming as a reason for caution when a similar-shaped candidate
comes up, not a hidden scoring penalty. A `reverted` outcome carries more weight than an
`ineffective` or `partial` one when judging this — it's not "didn't land great," it's "actively
undone," so it's worth naming even on its own, not just as part of a pattern.

If `Risk register: on`, an `ineffective` or `partial` outcome is also one of `risk-register.md`'s
creation/update triggers — even without an explicit `fixes:`/`reworked:` link, a plain bad outcome
in the same part of the project is earlier, softer evidence of the same pattern. See
`risk-register.md`'s
triggers list. A single `reverted` outcome is strong enough evidence to trigger a risk-area
proposal by itself, unlike `ineffective`/`partial`, which need a repeat pattern first — see
`risk-register.md`'s trigger 2.
