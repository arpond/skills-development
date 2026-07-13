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
Feedback: on (bulk-offer last: <N>)
```

`on`/`off`, default `on`. `off` disables the whole feedback check in Step 0.5 — no prompts, no
pending count shown. The `(bulk-offer last: N)` note records the eligible-count at which the
most recent bulk offer was made or declined (0 if never) — this is what lets Step 0.5 know not
to re-offer until the count has grown a full threshold-step past that point (see below); it's a
real stored field, not something inferred from the eligible count alone, since that count
fluctuates as items get answered or new ones ship.

Done entries extend the base format (see `SKILL.md`) with a ship date and an `outcome:` value:

```markdown
- **Idea name** (Category, shipped YYYY-MM-DD, outcome: pending) — one-line note...
```

`outcome:` is one of `pending`, `delivered`, `mixed`, `missed`, or `skipped`.

## Setup (from `setup.md`)

Ask one short yes/no: want the skill to occasionally check back on how shipped work actually
landed (delivered / mixed / missed)? Default `Feedback: on` if they don't care — it's capped and
skippable per the mechanics below, so opting in is low-risk.

## Recording a ship (from `SKILL.md` Step 6)

When moving an item to Done, extend the base `(Category)` parenthetical with a ship date and
`outcome: pending`, e.g. `(Category, shipped YYYY-MM-DD, outcome: pending)`. Both the date and
the outcome tag are specific to `Feedback: on` — if it's off, use the plain base format with
just the category.

## Checking in (from `SKILL.md` Step 0.5)

A Done entry is **eligible** once it's shipped ≥7 days ago and still has `outcome: pending` —
enough time has passed to actually judge it. Count eligible entries; this costs nothing extra
since Step 0.5 already reads the tracker.

- **Always surface the count** when it's nonzero, even if nothing else here triggers — e.g. a
  trailing "(3 ships pending feedback)" note. This is what stops the backlog from silently
  growing unnoticed; a visible number is enough on its own even between prompts.
- **Below the bulk threshold (default 5 eligible)**: drip mode. Ask about the single oldest
  eligible item, one short question — "Last shipped '<idea>' (<date>) — deliver as expected,
  mixed, or miss?" Any answer, including "skip," gets written back as its `outcome:` value
  immediately (skip -> `outcome: skipped`), so that item is never asked about again. At most one
  such question per invocation.
- **At or above the threshold, and the eligible count exceeds `bulk-offer last:` by at least the
  threshold**: make a single bulk offer instead of the drip question — "N ships pending
  feedback — want to clear them now, or keep going one at a time?" Either way (accepted or
  declined), update `bulk-offer last:` to the current eligible count immediately. If accepted,
  list every eligible item (idea name + ship date, oldest first, no cap) and let the user answer
  all of them in one pass (terse per-item tags are fine); write all tags back in one edit. If
  declined, or if the threshold condition isn't yet met, fall back to drip mode for this run.
- Answered items (any outcome, including `skipped`) drop out of the eligible count permanently —
  the backlog can only shrink or hold steady between offers, never balloon unnoticed.

## Using the results

Use recorded outcomes qualitatively in `SKILL.md` Step 2 (top-up) and Step 3 (ranking), the same
way existing signals like "what's fragile/rough-edged" are used — e.g. a category with a couple
of `missed` outcomes is worth naming as a reason for caution when a similar-shaped candidate
comes up, not a hidden scoring penalty.
