# Tracker maintenance (rare edge cases)

Read this file only when one of its specific triggers actually fires — not on a normal run. Each
section below names its own trigger. This exists to keep this rare, occasional-event content out of
the core file `SKILL.md` — none of it is needed to run the normal Step 0-6 loop.

## Minting and migrating ids

**Trigger: an id is actually needed** — a fresh Step 2 append, or an existing id-less entry that
something now wants to reference (a `fixes:` link, a risk entry's `mitigated-by:` tag, a reassess
flag) — **or `session-start.md` Step 0 discovering a tracker with zero ids and no `Next id:` line at
all**, which runs the first-adoption case below immediately rather than waiting for this section's
usual lazy trigger to eventually fire.

All of it is mechanical bookkeeping, same as Step 6's Done-trimming — never a
judgement call, and never a reason to stop and ask.

**The bulk-backfill ordering rule**, used both by first-time adoption below and by the one-time
retroactive backfill further down, stated once here rather than twice. Assign ids in one pass,
oldest-first:
1. Done entries in `shipped`-date order, including the archive (`IMPROVEMENT_TRACKER_DONE.md`) if
   it exists, treating live Done and the archive as the one combined pool, same rule as everywhere
   else that reads Done history.
2. Then each outstanding category top-to-bottom in file order.
3. Skip Rejected. An entry there already carrying a hand-typed `id: I<N>` stays as it is; nothing
   else in Rejected gets one.
4. Before assigning each id, apply the same hand-typed-id collision check as any other minting
   (see below). Skip past anything already in use rather than assuming the run of numbers is
   clear.

- **A missing `Next id:`** splits into two cases, not one:
  - **No entries have an id yet** (a tracker predating the id system entirely — `Created: 0.0.0` from
    `session-start.md`'s backfill, or otherwise never having written the field): this is a one-time
    full adoption, not routine lazy minting. Apply the bulk-backfill ordering rule above, starting the
    count at 1, then set `Next id:` to one past the highest id assigned. Doing this in one pass, rather
    than lazily per-entry as each is first referenced, is what keeps ids roughly tracking age/position
    instead of tracking "whenever something happened to reference it" — see the bulk-backfill section
    below for the same fix applied retroactively to a tracker that already went through the old lazy
    behavior before this existed.
  - **Some entries already have ids** (the field itself just wasn't written down, or this is the
    steady state after the bulk pass above has already run): initialize `Next id:` from the highest
    existing id + 1, and mint the rest lazily per-entry as covered next.
- **An id-less entry that now needs referencing** (steady state *after* initial adoption, not the
  bulk-adoption case above): mint the next counter value for *that one entry* in place. Don't rewrite
  every other id-less entry while you're there — being id-less is the expected steady state for
  anything that hasn't needed a reference yet, not an error, and not a malformed-tracker case either
  (contrast `session-start.md` Step 0's malformed handling).
- **Older entries in the trailing `(id: I<N>)` style**, from before the leading-`I<N>:`-prefix
  convention: a styling change, not a breaking one — read both, write the new style. Those entries
  stay exactly as they are, don't get bulk-rewritten, and remain valid to read and reference. Only
  newly-minted entries use the leading prefix.
- **A collision with a hand-typed id**: before minting, check the value isn't already in use — a
  hand-typed `id: I5` can exist on some entry while `Next id:` still sits at `I5` or lower. If it
  collides, skip forward past every id already in use (checking the live tracker, and
  `IMPROVEMENT_TRACKER_DONE.md`/`RISK_REGISTER.md` if either exists), mint the first free one, then
  set `Next id:` to one past whatever got minted.

## One-time bulk id backfill for a tracker migrated before this fix (changelog 2.2.0)

**Trigger: `changelog.md`'s 2.2.0 entry, disclosed via `session-start.md` Step 0.5's version-gap
walk, and the user accepts it.** Only relevant for a tracker whose `Next id:` already existed before
this fix — one that's never had `Next id:` gets the same result automatically via the bulk-adoption
case above, so nothing further applies to it here.

Apply the bulk-backfill ordering rule above to every entry that's still id-less, starting the count
from the current `Next id:` value rather than from 1 — this tracker already has ids in circulation
(including any stray hand-typed ones in Rejected), and the collision check folded into that rule is
what keeps this pass from handing out a number already spoken for. Set `Next id:` to one past the
highest id assigned by this pass.

This is a one-time sweep, not an ongoing state: once it's run (or declined), `Feature check:`
advances past 2.2.0 and it isn't offered again — any id-less entry appearing after this point is
ordinary steady state, handled by lazy per-entry minting like any other.

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
the only place a risk entry references an idea by id, and it's a promise that a fix is coming.
**If the idea is dropped instead of shipped, remove the tag.** Otherwise a risk entry points at a
fix that will never arrive. Nothing else needs cleaning up; exposure to a risk area is computed
from the entry's `areas:`, never stored against an idea, so a dropped idea simply stops matching.
