# Changelog

Read this file only when `session-start.md`'s version check finds a tracker's `Feature check:`
behind `SKILL.md`'s current skill version — most sessions, for most projects, it's already caught
up and this file is never opened.

**Versioning policy.** Semver, bumped only for changes that matter to an existing tracker: MINOR
for a new optional feature/behavior a pre-existing tracker might want to opt into, MAJOR for a
breaking tracker-format change that needs migration. Ordinary wording/bug fixes don't bump it —
patch stays `0`, unused. The current version lives at the top of `SKILL.md`; only MINOR+ versions
get an entry below, since those are the only ones a tracker could be behind on in a way it'd want
told about.

What a tracker's version-gap actually names. Each entry says what's new and **whether there's
anything to opt into**:

- **Opt-in entries** hand off to that feature's own setup ask (`feedback.md`/`strategies.md`/
  `risk-register.md`'s Setup sections, or the relevant inline instructions) — never a new
  confirm-gate of its own; reuse the feature's own flow, don't invent a parallel one.
- **Automatic entries** change how something already turned on behaves. There's nothing to accept
  or decline, so don't pose one as a question — mention it in a clause if it changes what the user
  will see, or skip it silently if it doesn't, and bump `Feature check:` either way.
- **A pure rename of existing values is automatic too** — no confirm gate, since a rewrite that
  preserves meaning exactly has no judgement in it (same category as the id-restyling mechanics in
  `tracker-maintenance.md`). Say it happened in the same disclosure clause, then sweep every
  occurrence across the live tracker and its archive in that one edit — not lazily on next touch,
  since leaving old and new spellings mixed indefinitely is exactly the drift this kind of change
  exists to close.

- **2.1.0** — *automatic, all projects, nothing to opt into.* Done's archive sweep (age vs.
  `floor`/`backstop`) now also runs at every session start (`session-start.md` Step 0.5), not only
  as a side effect of Step 6 recording a fresh ship. The append-triggered sweep could go
  uncompleted for reasons nothing else ever re-checked (a hand-edited tracker, a session ending
  before that check ran, an older tracker predating `Done archive:`), so Done could grow well past
  `age`/`floor`/`backstop` with nothing left to trigger a catch-up. If eligible entries are found,
  archiving now happens automatically on session start too, same no-confirmation bookkeeping as
  Step 6's own sweep — mentioned in a clause if it moves anything, silent otherwise.
- **2.0.0** — *breaking, `Feedback:` outcome values only, migrated automatically.* Outcome
  vocabulary renamed for clarity and to match `risk-register.md`'s own `mitigated-by:` vocabulary
  instead of duplicating it under different words: `delivered → effective`, `mixed → partial`,
  `missed → ineffective` (`pending`, `reverted`, `skipped` unchanged) — `delivered` read too much
  like a synonym for the ship date's own `shipped`, not for whether the ship actually worked.
  Disclosure sweeps every `outcome:` value across the live tracker and
  `IMPROVEMENT_TRACKER_DONE.md` (if it exists), rewriting old spellings to new in that same edit —
  a pure rename, so nothing to confirm beyond the ordinary version-gap disclosure.
- **1.1.0** — *automatic, `Risk register: on` only, nothing to opt into.* Risk entries now key on
  `areas:` (the files/modules/subsystem a risk is actually about) instead of on a stored `at-risk:`
  list of idea ids. Which outstanding ideas are exposed is computed fresh from those areas at
  Steps 2/3/4 rather than recorded, so the list can't go stale, doesn't need clearing on archival
  or re-populating on reactivation, and survives a hand-edited or absent tracker. `mitigated-by:`
  is unchanged and still carries an idea id — it's a stored judgement, not a computable match. An
  existing `RISK_REGISTER.md` keeps working: an `at-risk:` field is ignored on read and dropped
  whenever that entry is next rewritten, no bulk migration. The per-entry idea `Category` is gone
  for the same reason — areas scope a risk more precisely, and two join keys can drift apart.
  Entries do need `areas:` to match against anything, so the first time an older entry comes up,
  propose areas for it as part of whatever write is already happening.
- **1.0.0** — baseline. Everything in this skill as of the version field's introduction: idea ids
  (leading `I<N>:` prefix on new entries; existing entries in the older trailing `(id: I<N>)` style
  stay valid and don't need rewriting — both are readable, only new writes use the prefix),
  `Selection strategy:`, `Feedback:`, `Risk register:`, `Done archive:`, closed tracker sections.
  No disclosure owed for reaching baseline itself — a tracker backfilled to `1.0.0` (see
  `session-start.md` Step 0) isn't behind anything, it's caught up.
