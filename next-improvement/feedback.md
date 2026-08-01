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
Feedback: on(wait=7, bulk=5) (bulk-offer last: <N>)
```

`on`/`off`, default `on`. `off` disables the whole feedback check in `session-start.md`'s Step 0.5
— no prompts, no pending count shown. `wait` and `bulk` are optional and independently settable (unset means the
defaults shown, 7 and 5 respectively) — plain `Feedback: on` with no parens is equivalent to
`Feedback: on(wait=7, bulk=5)` and is the normal way to write it when neither needs changing; only
spell out the parens when overriding one. `wait` is the eligibility window in days (see Checking
in), `bulk` is the bulk-offer threshold (same section) — two unrelated numbers, set independently,
same as the `Selection strategy:` counts. The `(bulk-offer last: N)` note records the
eligible-count at which the most recent bulk offer was made or declined (0 if never) — this is
what lets Step 0.5 know not to re-offer until the count has grown a full `bulk`-step past that
point (see below); it's a real stored field, not something inferred from the eligible count alone,
since that count fluctuates as items get answered or new ones ship.

Done entries extend the base format (see `SKILL.md`) with a ship date and an `outcome:` value:

```markdown
- **Idea name** (Category, shipped YYYY-MM-DD, outcome: pending) — one-line note...
```

`outcome:` is one of `pending`, `delivered`, `mixed`, `missed`, or `skipped`.

## Setup (from `setup.md`)

Ask one short yes/no: want the skill to check back on how shipped work actually landed (delivered
/ mixed / missed) — at most once per session, starting 7 days after an item ships, and offered as
a single bulk prompt once 5 are eligible at once rather than asked one at a time? Default
`Feedback: on(wait=7, bulk=5)` if they don't care — both numbers are changeable later without
re-running setup, and it's capped and skippable per the mechanics below, so opting in is low-risk.

## Recording a ship (from `SKILL.md` Step 6)

When moving an item to Done, extend the base `(Category)` parenthetical with a ship date and
`outcome: pending`, e.g. `(Category, shipped YYYY-MM-DD, outcome: pending)`. Both the date and
the outcome tag are specific to `Feedback: on` — if it's off, use the plain base format with
just the category.

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

- **Always surface the count** when it's nonzero, even if nothing else here triggers — e.g. a
  trailing "(3 ships pending feedback)" note. This is what stops the backlog from silently
  growing unnoticed; a visible number is enough on its own even between prompts. This still only
  fires once per session, per the throttle above — it's about not going silent forever across
  separate sessions, not about repeating every round within one.
- **Below the `bulk` threshold (default 5 eligible)**: drip mode. Ask about the single oldest
  eligible item across both files, one short question — "Last shipped '<idea>' (<date>) — deliver
  as expected, mixed, or miss?" Any answer, including "skip," gets written back as its `outcome:`
  value immediately (skip -> `outcome: skipped`) in whichever file the item actually lives in
  (live tracker or `IMPROVEMENT_TRACKER_DONE.md`), so that item is never asked about again. At
  most one such question per session, per the throttle above.
- **At or above `bulk`, and the eligible count exceeds `bulk-offer last:` by at least `bulk`**:
  make a single bulk offer instead of the drip question — "N ships pending feedback — want to
  clear them now, or keep going one at a time?" Either way (accepted or declined), update
  `bulk-offer last:` to the current eligible count immediately. If accepted, list every eligible
  item as a numbered list (idea name + ship date, oldest first across both files, no cap — see
  `SKILL.md` Step 4's numbering rule, which applies to this list too) and let the user answer all
  of them in one pass by number (terse per-item tags are fine); write each tag back into whichever
  file that item is actually in — this may mean one edit to the live tracker and one to the
  archive if eligible items span both. If declined, or if the threshold condition isn't yet met,
  fall back to drip mode for this run.
- Answered items (any outcome, including `skipped`) drop out of the eligible count permanently —
  the backlog can only shrink or hold steady between offers, never balloon unnoticed.

## Using the results

Use recorded outcomes qualitatively in `SKILL.md` Step 2 (top-up) and Step 3 (ranking), the same
way existing signals like "what's fragile/rough-edged" are used — e.g. a category with a couple
of `missed` outcomes is worth naming as a reason for caution when a similar-shaped candidate
comes up, not a hidden scoring penalty.
