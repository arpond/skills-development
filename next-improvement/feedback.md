# Outcome feedback (optional)

Read this file only when the tracker's `Feedback:` line is `on`, or when the user is setting it
up or asking to change it. If a project has `Feedback: off` (or the line is simply absent),
none of this applies and you never need to read it.

The idea: shipped work can look great as a plan and still not deliver. This loop asks, lazily
and cheaply, how past ships actually landed, and feeds that back into future ranking/top-up
judgement — without turning into a nagging, ever-growing chore.

## Tracker format

In the Goals block:

```markdown
Feedback: on(wait=7, bulk=5, batch=5) (bulk-offer last: <N>)
```

`on`/`off`, default `on`. `off` disables the whole feedback check in `session-start.md`'s Step 0.5
— no prompts, no pending count shown (but see `session-start.md`'s Step 0.6, which still surfaces
standalone `reassess:` flags even with `Feedback: off`, since those aren't part of this
subsystem). `wait`, `bulk`, and `batch` are optional and independently settable (unset means the
defaults shown — 7, 5, and 5 respectively) — plain `Feedback: on` with no parens is equivalent to
`Feedback: on(wait=7, bulk=5, batch=5)` and is the normal way to write it when none need changing;
only spell out the parens when overriding one. `wait` is the eligibility window in days (see
Checking in), `bulk` is the bulk-offer threshold, `batch` is the chunk size for the batched-offer
mode (same section) — three unrelated numbers, set independently (`batch` defaults to whatever
`bulk` is set to, but doesn't silently ride on it — set it separately if the two should differ,
e.g. offering in chunks smaller than the threshold that triggers the offer), same independent-knob
treatment as the `Selection strategy:` counts. The `(bulk-offer last: N)` note records the
eligible-count at which the most recent bulk-style offer (all-at-once or batched) was made or
declined (0 if never) — this is what lets Step 0.5 know not to re-offer until the count has grown a
full `bulk`-step past that point (see below); it's a real stored field, not something inferred from
the eligible count alone, since that count fluctuates as items get answered or new ones ship.

Done entries extend the base format (see `SKILL.md`, which also covers the `id:`, `fixes:`,
`reworked:`, and `reassess:` fields — those aren't specific to this subsystem) with a ship date and
an `outcome:` value:

```markdown
- **Idea name** (Category, id: I7, shipped YYYY-MM-DD, outcome: pending) — one-line note...
```

`outcome:` is one of `pending`, `delivered`, `mixed`, `missed`, `reverted`, or `skipped`.
`reverted` is distinct from `missed`: `missed` means it shipped but didn't deliver the intended
value; `reverted` means it was actually undone — a stronger, costlier signal worth its own tag
rather than folding into `missed`.

## Setup (from `setup.md`)

Ask one short yes/no: want the skill to check back on how shipped work actually landed (delivered
/ mixed / missed) — at most once per session, starting 7 days after an item ships, and offered
(once 5 are eligible at once) as a choice of all-at-once, in smaller batches, continuously one at a
time, or the default single question, rather than always asked one at a time? Default
`Feedback: on(wait=7, bulk=5, batch=5)` if they don't care — all three numbers are changeable later
without re-running setup, and it's capped and skippable per the mechanics below, so opting in is
low-risk.

## Recording a ship (from `SKILL.md` Step 6)

When moving an item to Done, extend the base `(Category, id: I<N>)` parenthetical (see `SKILL.md`
for the id itself, which applies regardless of `Feedback:`) with a ship date and `outcome:
pending`, e.g. `(Category, id: I7, shipped YYYY-MM-DD, outcome: pending)`. The date and the
outcome tag are specific to `Feedback: on` — if it's off, use the plain base format with just the
category and id.

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
`outcome: pending` — enough time has passed to actually judge it. Count eligible entries from the
live tracker's Done section for free, since Step 0.5 already reads it. Then also check whether
`IMPROVEMENT_TRACKER_DONE.md` exists (`SKILL.md` Step 6 archives entries regardless of `outcome`,
so a `pending` entry can end up there if the feedback loop hasn't caught up to it yet) — if it
exists, open it and fold any `pending` entries in as eligible too. Treat the two files as one
combined pool: eligible count is the sum, and "oldest eligible" (drip mode, below) is the oldest
across both, not just whichever file it happens to live in. This is the one place in the normal
Step 0-6 loop that reads the archive, and only when `Feedback: on` — see `SKILL.md`'s "Reading the
archive" note.

- **`reassess: pending` entries take priority over routine eligible items.** A `reassess` flag
  (`SKILL.md` Step 6: a later ship fixed or reworked this one) means the item's original outcome
  judgement may no longer hold — surfacing that is more valuable than a routine newly-eligible ask,
  so reassess-flagged entries always go first, oldest first, ahead of plain eligible items in every
  mode below. Wording is distinct from a routine ask, and depends on what the origin's outcome
  already was: if it's still `pending` (never answered), fold the fix/rework into the normal
  outcome question as one clause instead of asking twice — "Last shipped '<idea>' (<date>) —
  deliver as expected, mixed, miss, or was it reverted? (Note: this was later fixed by '<fixing
  idea>'.)" If the origin already had a real answer (`delivered`/`mixed`/`missed`/`reverted`),
  reopen it explicitly: "'<idea>' was marked <old outcome>, but was later fixed by '<fixing idea>'
  — still <old outcome>, or downgrade to mixed/missed/reverted?" Clear `reassess: pending` the
  moment it's answered, same as any other eligible item — see "Answered items" below.
- **Always surface the count** when it's nonzero, even if nothing else here triggers — e.g. a
  trailing "(3 ships pending feedback, 1 needs reassessment)" note, calling out the reassess subset
  separately since it's a different kind of pending. This is what stops the backlog from silently
  growing unnoticed; a visible number is enough on its own even between prompts. This still only
  fires once per session, per the throttle above — it's about not going silent forever across
  separate sessions, not about repeating every round within one.
- **Every item shown in any mode below gets a why-and-what line, not just name + date** — the
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
- **At or above `bulk`, and the eligible count exceeds `bulk-offer last:` by at least `bulk`**:
  offer a choice instead of the single drip question — "N ships pending feedback (M need
  reassessment) — clear them all now, N at a time, one-by-one until you say stop, or just the
  oldest for now?" Whichever is chosen (or declined outright), update `bulk-offer last:` to the
  current eligible count immediately — the offer itself only needs re-triggering once the pool
  grows another full `bulk`-step, regardless of which mode was picked last time.
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
of `missed` outcomes is worth naming as a reason for caution when a similar-shaped candidate
comes up, not a hidden scoring penalty. A `reverted` outcome carries more weight than a `missed` or
`mixed` one when judging this — it's not "didn't land great," it's "actively undone," so it's
worth naming even on its own, not just as part of a pattern.

If `Risk register: on`, a `missed` or `mixed` outcome is also one of `risk-register.md`'s
creation/update triggers — even without an explicit `fixes:`/`reworked:` link, a plain bad outcome
in a category is earlier, softer evidence of the same kind of pattern. See `risk-register.md`'s
triggers list. A single `reverted` outcome is strong enough evidence to trigger a risk-area
proposal by itself, unlike `missed`/`mixed`, which need a repeat pattern first — see
`risk-register.md`'s trigger 2.
