# Changelog

Read this file only when `session-start.md`'s version check finds `KNOWLEDGE.md`'s
`Feature check:` behind `SKILL.md`'s current skill version. Most runs it is already current and
this file stays closed.

**Versioning policy.** Semver, bumped only for a change an existing `KNOWLEDGE.md` could want told
about: MINOR for an opt-in feature, or an automatic change to behaviour that is already on. MAJOR
for a format change that needs migration. Wording and bug fixes do not bump it. Patch stays `0`,
unused. The current version lives at the top of `SKILL.md`. Only MINOR+ versions get an entry
below, because those are the only ones a file can be behind on.

Each entry says what is new and **whether there is anything to opt into**:

- **Opt-in entries** hand off to that feature's own gate, never a new one invented here.
- **Automatic entries** change how something already on behaves. There is nothing to accept or
  decline, so do not pose one as a question. Say it in a clause if it changes what the user will
  see. Stay silent if it does not. Bump `Feature check:` either way.

- **1.0.0** — *baseline, automatic, nothing to opt into.* Everything in this skill as of the
  version field's introduction. A file backfilled from a missing stamp to `0.0.0` is not behind on
  anything this file tracks. The only visible change is the new `Feature check:` header line. Say
  that in a clause, then stamp.
