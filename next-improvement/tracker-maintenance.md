# Tracker maintenance (events outside the normal loop)

Read this file only when one of its specific triggers actually fires — not on a normal run. Each
section below names its own trigger. This exists to keep occasional-event content out of the core
file `SKILL.md` — none of it is needed to run the normal Step 0-6 loop.

## Minting and migrating ids

**Trigger: an id is actually needed** — a fresh Step 2 append, or an existing id-less entry that
something now wants to reference (a `fixes:` link, a risk entry's `mitigated-by:` tag, a reassess
flag) — **or `session-start.md` Step 0 discovering a tracker with zero ids and no `Next id:` line at
all**, which runs the first-adoption case below immediately rather than waiting for this section's
usual lazy trigger to eventually fire.

All of it is mechanical bookkeeping, same as the Done archive sweep — never a
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
  - **No entries have an id yet** (a tracker predating the id system entirely — `Created: 0.0.0`
    from the catch-up section below, or otherwise never having written the field): this is a one-time
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

**Trigger: `build-and-record.md` Step 6 is about to ask whether this ship fixes or reworks an earlier one, and
`Next id:` was missing before this recording** — meaning this project has never seen that
question. `setup.md` writes `Next id:` into every tracker it creates, so a missing field means a
tracker older than that rule, never a fresh one.

Say so in one clause before asking it, e.g. "(this tracker's picking up a new feature: every ship
now gets asked if it fixes/reworks an earlier one, used to flag the origin for a second look)" —
the same disclosure `setup.md` gives a brand-new tracker at bootstrap, given once here since an
existing tracker never goes through `setup.md` again. Don't repeat it on later ships once
`Next id:` exists.

## Catching up a tracker that predates the version stamps

**Trigger: `session-start.md` Step 0 finds `Created:` or `Feature check:` missing.** That means a
tracker older than those fields, or one written by hand. It fires once in such a tracker's life
and never for one `setup.md` created, which is why it lives here rather than in the every-run read.

Don't treat a missing stamp as already caught up. A missing stamp is stronger evidence of being
behind than a stale one, and never proof of being current.

**These two fields split into a mechanical part and a check-in part. Don't let the first blur
into skipping the second.**
- Backfill `Created:` to `0.0.0` as mechanical bookkeeping. The tracker's real creation version is
  unknown, and stamping it to the *current* skill version would falsely claim it started life
  knowing about everything up to today, which is exactly backwards for a tracker old enough to
  predate the field. `0.0.0` says the true thing instead.
- Backfill `Feature check:` to `0.0.0` as that same mechanical first step.
- **Stamping `Feature check:` to the current version is never mechanical.** It can only happen
  *after* actually running `session-start.md` Step 0.5's full behind-version disclosure walk (open
  `changelog.md`, walk every entry, oldest first) and folding the result into the combined
  check-in, exactly as if this tracker had really been sitting at `0.0.0` all along.

This tracker is owed disclosure for every feature shipped since baseline, not just future ones. A
missing stamp confirms nothing about what it already knows, so treating the whole section as
mechanical bookkeeping and jumping straight to the current-version stamp is exactly the failure mode
it exists to block.

**This backfilled tracker also never went through `setup.md`'s own bootstrap interrogation.** It
predates this skill's full feature set, or was created by hand. Two different things follow, and
they must not be conflated:

- **The id system, `Done archive:` mechanics, and the closed-section rule are core and mandatory,
  never dependent on presence.** Contrast `Selection strategy:`/`Feedback:`/`Risk register:`, which
  genuinely are optional and read by *value*, not presence (see `SKILL.md`'s tracker-format note).
  If this tracker has zero ids anywhere and no `Next id:` line at all, that's exactly this file's
  "Minting and migrating ids" first-adoption case:
  - Run its one-time bulk backfill right here, as the same mechanical bookkeeping
    as the version-stamp backfill above. Waiting for that section's ordinary "an id is actually
    needed" trigger might never fire this session, leaving the tracker looking id-less
    indefinitely.
  - Never frame this as "want to start using ids?" It isn't a choice; it's baseline mechanics this
    tracker was always going to have.
  - Mention it in one clause if it actually ran ("also backfilled ids for the N entries that
    didn't have one yet"); silent otherwise, same as any other automatic action that didn't
    change what's visible this run.
- **`Selection strategy:`, `Feedback:`, and `Risk register:` are genuinely optional, and this
  tracker never got `setup.md` Step 4's one-time offer of them.** Offer each of the three that has
  no line at all. An existing line already answers the question, even if it just spells out the
  default. Fold whatever's still due into this run's combined check-in: the same brief questions
  `setup.md` Step 4 asks a brand-new tracker (the full option set for `Selection strategy:`, per
  `strategies.md`'s own Setup section; a single short yes/no each for `Feedback:` and
  `Risk register:`). This is distinct
  from the changelog walk above: that walk discloses *changes* since baseline; this discloses
  baseline features the tracker never had a chance to decline or accept at all, since it skipped
  `setup.md` entirely.

## Trimming an oversized entry

**Trigger: the user accepts `session-start.md` Step 0.5's entry-size offer, or asks for a trim of
an idea-category entry.** Done and Rejected stay append-only history. Content in a category that
is not an entry gets the same treatment as an entry's excess.

**Work in batches, largest first.** A tracker can hold a hundred oversized entries, and one message
cannot carry a hundred proposals.
- Propose the five largest in the first message, so the yes that led here is not asked again.
- Put the full over-limit list under them, numbered, with word counts, so the user can pick others
  instead.
- Continue five at a time, and stop when the user says so.

**Before you propose a trim, find what cites the entry.** Other files point into a tracker by id,
and a trim can remove the detail they point at.
1. Search the project for the id as a whole word, outside this skill's own files.
2. For each hit, say which file cites the entry and what detail it relies on.
3. Where that detail would go, either keep it in the entry or include an update to the citing file
   in the proposal.
4. Say that the search covered this project only. A citation from another repository is invisible
   to it.

A `fixes:`, `reworked:`, or `mitigated-by:` tag cites by id alone, so a trim that keeps the id keeps
it working.

**Sort what comes out by kind. Each kind has one destination.**
1. **Stale content**: superseded counts, lists of line numbers, notes that something no longer
   holds. Delete it. A move keeps an error alive.
2. **Change history and dated measurements.** Delete it, and name the commit that holds the full
   text: the last one to touch the tracker. That commit holds it only if the tracker has no
   uncommitted changes. If the tracker is untracked, modified, or not in a git repository, say the
   deleted text would be lost. Then ask, as a numbered choice, whether to keep it, move it, or
   delete it anyway.
3. **Durable findings and gotchas.** Offer a handoff to a skill in the session that records repo
   knowledge, such as `repo-knowledge`. It applies its own test for what to keep, so never write to
   its file directly. With no such skill, ask, as a numbered choice, whether to keep the finding in
   the entry or delete it.
4. **Reference material**: tables, vocabularies, lists of consumers. Propose a file for it, which
   the user decides on. Put it in the project's docs directory, or at the project root if it has
   none. Never create a docs directory to hold it. Where the project has more than one, ask which.
   If the user declines the file, treat the material as kind 2.

**Show each proposal and wait for confirmation before writing.** A proposal shows:
- the entry as it would read after the trim, within the limit
- each removed part, with its kind and destination
- the files that cite the entry, and any change they need

**Compare the destinations you found with the ones the header names.** The header was filled in
at setup, and the project may since have gained a `KNOWLEDGE.md` or a docs directory. Where a
destination now exists that the header does not name, add the update to the header's last
sentence to the first proposal of the trim. Change only that sentence.

A trimmed entry keeps its id, its position, and every tag in its parenthetical. Keep its name
unless the name is itself the excess.

**After the write, count the trimmed entries again with the same tool.** Report any still over the
limit. A successful write does not show that the entry fits.

If the trim is committed, the commit message names the commit that held the removed text.

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
