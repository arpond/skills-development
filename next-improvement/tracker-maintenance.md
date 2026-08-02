# Tracker maintenance (rare edge cases)

Read this file only when one of its specific triggers actually fires — not on a normal run. Each
section below names its own trigger. This exists to keep this rare, occasional-event content out of
`SKILL.md`'s always-loaded core read — none of it is needed to run the normal Step 0-6 loop.

## Minting and migrating ids

**Trigger: an id is actually needed** — a fresh Step 2 append, or an existing id-less entry that
something now wants to reference (a `fixes:` link, a risk entry's `mitigated-by:` tag, a reassess
flag).

All of it is mechanical, no-confirmation bookkeeping, same as Step 6's Done-trimming — never a
judgement call, and never a reason to stop and ask.

- **A missing `Next id:`** (a tracker predating the field): initialize it the first time something
  actually needs it — from 1, or from the highest existing id + 1 if some entries already have one.
- **An id-less entry that now needs referencing**: mint the next counter value for *that one entry*
  in place. Don't rewrite every other id-less entry while you're there — being id-less is the
  expected steady state for anything that hasn't needed a reference yet, not an error, and not a
  malformed-tracker case either (contrast `session-start.md` Step 0's malformed handling).
- **Older entries in the trailing `(id: I<N>)` style**, from before the leading-`I<N>:`-prefix
  convention: a styling change, not a breaking one — read both, write the new style. Those entries
  stay exactly as they are, don't get bulk-rewritten, and remain valid to read and reference. Only
  newly-minted entries use the leading prefix.
- **A collision with a hand-typed id**: before minting, check the value isn't already in use — a
  hand-typed `id: I5` can exist on some entry while `Next id:` still sits at `I5` or lower. If it
  collides, skip forward past every id already in use (checking the live tracker, and
  `IMPROVEMENT_TRACKER_DONE.md`/`RISK_REGISTER.md` if either exists), mint the first free one, then
  set `Next id:` to one past whatever got minted.

## One-time heads-up on a tracker that predates the fixes/reworks question

**Trigger: `SKILL.md` Step 6 is about to ask whether this ship fixes or reworks an earlier one, and
`Next id:` was missing before this recording** — meaning this project has never seen that question.

Say so in one clause before asking it, e.g. "(this tracker's picking up a new feature: every ship
now gets asked if it fixes/reworks an earlier one, used to flag the origin for a second look)" —
the same disclosure `setup.md` gives a brand-new tracker at bootstrap, given once here since an
existing tracker never goes through `setup.md` again. Don't repeat it on later ships once
`Next id:` exists.

## Retiring, merging, or narrowing a category

**Trigger: offered at `dry runs: 2+`** (see `SKILL.md` Step 2), and the user picks one of these
instead of "keep polling."

- **Retire**: delete that category's `##` header and its (by then empty, or otherwise moved) item
  list from the active section — but never touch **Done**/**Rejected** entries already tagged with
  that category name; they're history, not live state, and stay exactly as written.
- **Merge into an existing category**: move any remaining outstanding items under the surviving
  category's header (dropping the retired one), and don't rewrite old Done/Rejected tags to the new
  name — a mismatched historical tag is expected and fine, not a bug to fix.
- **Narrow scope instead**: rename the category's `##` header to a more specific name (the tracker
  format has no separate scope/description field — the name *is* the scope) and treat that
  narrower name as the brief for future brainstorming in Step 2; existing outstanding items stay
  under it unless they no longer fit, in which case handle them like any other Step 2 judgement
  call (re-propose to a different category, or drop with a Rejected note) rather than silently
  discarding them.

All three are still a write to the tracker and need confirmation first, same as any other Step 2
change (see `SKILL.md`'s hard-rules table).

**Preserve the id on a dropped item's Rejected note** (`(Category, YYYY-MM-DD, id: I<N>)`) if it
already had one — an outstanding idea can still be referenced by id from elsewhere, and dropping it
to Rejected doesn't retract that reference. This applies to any outstanding idea dropped to
Rejected, not just a category-retirement drop.

**If `Risk register: on`, check for a `mitigated-by:` tag naming it** (`risk-register.md`). That's
the only place a risk entry references an idea by id, and it's a promise that a fix is coming: if
the idea is dropped instead of shipped, remove the tag rather than leaving a risk entry pointing at
a fix that will never arrive. Nothing else needs cleaning up — exposure to a risk area is computed
from the entry's `areas:`, never stored against an idea, so a dropped idea simply stops matching.
