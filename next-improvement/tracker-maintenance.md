# Tracker maintenance (rare edge cases)

Read this file only when one of its specific triggers actually fires — not on a normal run. Each
section below names its own trigger. This exists to keep this rare, occasional-event content out
of `SKILL.md`'s always-loaded core read (see `DESIGN_PHILOSOPHY.md`'s "Progressive disclosure") —
none of it is needed to run the normal Step 0-6 loop.

## Id collision when minting

**Trigger: about to mint a new id** (lazy-backfill or a fresh Step 2 append).

Check it isn't already in use anywhere in the tracker first — a hand-typed `id: I5` can exist on
some entry while `Next id:` is still sitting at `I5` or lower, e.g. from manual editing. If the
value about to be minted collides, skip forward past every id already in use (checking the live
tracker, and `IMPROVEMENT_TRACKER_DONE.md`/`RISK_REGISTER.md` if either exists) and mint the first
free one instead, then set `Next id:` to one past whatever got minted — this is the same
mechanical, no-confirmation bookkeeping as the rest of id assignment (`SKILL.md`'s tracker-format
section), not a new judgement call.

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
already had one — an outstanding idea can be referenced from elsewhere (a risk entry's `at-risk:`
list) purely by id, and dropping it to Rejected doesn't retract that reference; if
`Risk register: on`, also remove the id from any `at-risk:` list it appears on, same as any other
idea leaving the outstanding pool (see `SKILL.md` Step 6's clean-ship handling for the parallel
case). This applies to any outstanding idea dropped to Rejected, not just a category-retirement
drop — including one tagged `mitigated-by: ... (outcome: planned)` on a risk entry
(`risk-register.md`): if the idea it names is dropped instead of shipped, remove that
`mitigated-by:` tag too rather than leaving a dangling reference to a fix that will never ship.
