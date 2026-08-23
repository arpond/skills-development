# Changelog

Read this file only when `session-start.md`'s version check finds a tracker's `Feature check:`
behind `SKILL.md`'s current skill version. Most sessions, for most projects, the tracker is
already current and this file stays closed.

**Versioning policy.** Semver, bumped only for changes that matter to an existing tracker: MINOR
for an opt-in feature, or an automatic change to behaviour that is already on. MAJOR for a
breaking tracker-format change that needs migration. Ordinary wording and bug fixes do not bump
it. Patch stays `0`, unused. The current version lives at the top of `SKILL.md`. Only MINOR+
versions get an entry below, because those are the only ones a tracker can be behind on.

Each entry says what is new and **whether there is anything to opt into**:

- **Opt-in entries** hand off to that feature's own setup ask (the Setup sections of
  `feedback.md`, `strategies.md`, and `risk-register.md`, or the relevant inline instructions).
  Never a new gate of its own. Reuse the feature's own flow, do not invent a parallel one.
- **Automatic entries** change how something already on behaves. There is nothing to accept or
  decline, so do not pose one as a question. Say it in a clause if it changes what the user will
  see. Stay silent if it does not. Bump `Feature check:` either way.
- **A pure rename of existing values is automatic too.** No gate, because a rewrite that keeps
  the meaning exactly has no judgement in it (the same category as the id-restyling mechanics in
  `tracker-maintenance.md`). Say it happened in the same disclosure clause. Then sweep every
  occurrence across the live tracker and its archive in that one edit, not lazily on next touch.
  Old and new spellings mixed indefinitely is exactly the drift this kind of change exists to
  close.

- **2.2.0** — *opt-in, only for trackers whose `Next id:` existed before this fix. A tracker that
  adopts ids fresh under 2.2.0 has nothing to opt into.* A tracker that adopted the id system
  before this fix left its pre-existing entries without ids. Each got one only when something
  first referenced it. Entries added after adoption got ids immediately, in order. So id numbers
  tracked "whenever something happened to reference it", not age or position. An old entry near
  the top of a category could get a higher id than newer entries below it. Setup ask: offer a
  one-time bulk backfill. Assign ids to every entry still without one in one pass: Done entries by
  `shipped` date, oldest first, then each outstanding category top to bottom in file order.
  Rejected stays untouched, per the format's usual id-less-by-default rule. Continue `Next id:`
  from the highest id assigned. See the bulk-backfill section of `tracker-maintenance.md` for the
  mechanics. Accept or decline, `Feature check:` still advances past 2.2.0, so this is asked once
  per project.
- **2.1.0** — *automatic, all projects, nothing to opt into.* Done's archive sweep (age against
  `floor` and `backstop`) now also runs at every session start (`session-start.md` Step 0.5), not
  only as a side effect of Step 6 after a fresh ship. The append-triggered sweep could stay
  incomplete for reasons nothing else re-checked: a hand-edited tracker, a session that ended
  before that check ran, an older tracker that predates `Done archive:`. Done could then grow well
  past `age`, `floor`, and `backstop` with nothing left to trigger a catch-up. If eligible entries
  exist, archiving now also happens automatically at session start, the same no-confirmation
  bookkeeping as Step 6's own sweep. Say it in a clause if it moves anything. Otherwise stay
  silent.
- **2.0.0** — *breaking, `Feedback:` outcome values only, migrated automatically.* The outcome
  vocabulary changed for clarity and to match `risk-register.md`'s own `mitigated-by:` vocabulary
  instead of a duplicate under different words: `delivered → effective`, `mixed → partial`,
  `missed → ineffective` (`pending`, `reverted`, `skipped` unchanged). `delivered` read too much
  like a synonym for the ship date's own `shipped`, not like a verdict on whether the ship worked.
  Disclosure sweeps every `outcome:` value across the live tracker and
  `IMPROVEMENT_TRACKER_DONE.md` (if it exists) and rewrites old spellings to new in that same edit.
  A pure rename, so nothing to confirm beyond the ordinary version-gap disclosure.
- **1.1.0** — *automatic, `Risk register: on` only, nothing to opt into.* Risk entries now key on
  `areas:` (the files, modules, or subsystem a risk is about) instead of a stored `at-risk:` list
  of idea ids. The skill computes which outstanding ideas are exposed fresh from those areas at
  Steps 2, 3, and 4, and records nothing. So the list cannot go stale, needs no clearing on
  archival or re-population on reactivation, and survives a hand-edited or absent tracker.
  `mitigated-by:` is unchanged and still carries an idea id. It is a stored judgement, not a
  computable match. An existing `RISK_REGISTER.md` keeps working: the skill ignores an `at-risk:`
  field on read and drops it the next time it rewrites that entry. No bulk migration. The
  per-entry idea `Category` is gone for the same reason: areas scope a risk more precisely, and
  two join keys can drift apart. Entries need `areas:` to match against anything. So the first
  time an older entry appears, propose areas for it as part of whatever write is already in
  progress.
- **1.0.0** — baseline. Everything in this skill as of the version field's introduction, in two
  kinds. **Core, mandatory, never dependent on presence**: idea ids, `Done archive:`, and closed
  tracker sections. Idea ids use a leading `I<N>:` prefix on new entries. Existing entries in the
  older trailing `(id: I<N>)` style stay valid and need no rewrite. Both are readable, and only new
  writes use the prefix. **Optional, read by value**: `Selection strategy:`, `Feedback:`,
  `Risk register:`. Baseline itself needs no *changelog* disclosure. A tracker backfilled to
  `0.0.0` (see `session-start.md` Step 0) is not behind on anything this file tracks, because
  nothing here is a change from baseline. That is not the same as a tracker that was asked about
  the optional trio. A tracker old enough to need this backfill also never went through
  `setup.md`'s own bootstrap interrogation. `session-start.md` Step 0 gives it that one-time
  catch-up separately from this walk.
