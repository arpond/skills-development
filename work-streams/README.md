# work-streams

Parks and resumes named streams of work. A stream is one thread of work with a name, such as
`skipped-tests` or `auth-refactor`. Several streams can run in parallel against the same repo. A
stream can also span more than one repo. Each stream keeps a manifest with its goal and current
state. It also keeps a folder of task-scoped context files and an optional continuation prompt
for the next session. All of it lives in a personal store outside every repo, so nothing is committed and
nothing depends on one project's layout.

The skill exists because session context dies at exit or `/clear`. Claude Code has no way to run
a model step at session end, so an automatic wrap-up is not possible. Instead the user says
"wrap up", and the skill records what the next session needs. Wrap-up also sweeps a per-stream
list of repo files that the work should keep current. Where another skill owns the record,
wrap-up hands off to it, such as `repo-knowledge` for gotchas or `next-improvement` for
progress.

Files:

- `SKILL.md` — the store layout, the manifest format, the wrap-up flow, and the resume flow.
  Read on every invocation.
- `setup.md` — the one-time config bootstrap. Read only when no config file exists yet.
- `lifecycle.md` — archive, re-activate, and delete. Read only when a stream finishes or the
  user asks for one of those.

## What it writes

- `~/.claude/work-streams-config.md` — one config file per machine. It holds the store's base
  path. Created once, after the proposal is confirmed.
- The store, default `~/.claude/work-streams/` and configurable. One folder per project, one
  folder per stream. Each stream holds `stream.md`, an optional `continuation.md`, and a
  `context/` folder. Every write is part of a wrap-up plan that is shown and confirmed first.
- Repo files, only as part of that same confirmed plan. The wrap-up sweep can propose edits to
  files the stream lists as update targets, such as a cheatsheet or a README. It never edits a
  repo file without showing the edit first.
- Removals, as part of that same plan. Every wrap-up reviews `context/` and proposes the prune
  of files the work has outgrown, so the folder stays small. The store has no version control,
  so a confirmed removal is permanent.

The store is personal and machine-local. The skill never commits it, and never commits anything
else on its own. It never writes secrets, credentials, or PII into a stream file. When pasted
material contains one of those, it asks how to redact it first.

## Requires

Nothing beyond local file read and write. The handoffs to `repo-knowledge` and
`next-improvement` are optional. When a listed skill is not installed, the sweep says so and
moves on.

## When it triggers

- "wrap up" / "wrap this session up" / "park this" / "let's stop here for today"
- "pick up where we left off" / "resume the skipped-tests stream"
- "what streams are open here?"
- "archive that stream" / "bring back the auth-refactor stream" / "delete the old stream"

## Example

```
User: let's stop here for today

Claude: Wrapping up. This session's work matches the active stream "skipped-tests"
  (updated 2026-08-20). Here's the wrap-up plan:

  Store (~/.claude/work-streams/titan/skipped-tests/):
  - State of play rewritten: 14 of 31 skipped tests re-enabled; the auth suite is
    blocked on a fixture rewrite.
  - context/re-enable-progress.md refreshed with the per-suite table.
  - context/auth-fixture-notes.md added: why the fixture rewrite is needed.

  Repo update targets:
  - docs/test-cheatsheet.md — add the fixture workaround found today.
  - skill: repo-knowledge — the fixture's clock dependency looks like a capture
    candidate; I'll run its capture bar if you confirm.

  Continuation prompt: want one? Draft covers the fixture rewrite as the next step.

  Is this stream finished, or does it stay active?

User: not finished. yes to all of it

Claude: Written. Store updated, cheatsheet edited, repo-knowledge proposed one entry
  (confirmed separately), continuation.md written. The stream stays active.
```
