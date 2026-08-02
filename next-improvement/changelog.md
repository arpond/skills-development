# Changelog

Read this file only when `session-start.md`'s version check finds a tracker's `Feature check:`
behind `SKILL.md`'s current skill version — most sessions, for most projects, it's already caught
up and this file is never opened.

What a tracker's version-gap actually names. Each entry: what's new, and which existing setup flow
to hand off to for opting in (never a new confirm-gate of its own — reuse the feature's own setup
ask, don't invent a parallel one).

- **1.0.0** — baseline. Everything in this skill as of the version field's introduction: idea ids
  (leading `I<N>:` prefix on new entries; existing entries in the older trailing `(id: I<N>)` style
  stay valid and don't need rewriting — both are readable, only new writes use the prefix),
  `Selection strategy:`, `Feedback:`, `Risk register:`, `Done archive:`, closed tracker sections.
  No disclosure owed for reaching baseline itself — a tracker backfilled to `1.0.0` (see
  `session-start.md` Step 0) isn't behind anything, it's caught up.
