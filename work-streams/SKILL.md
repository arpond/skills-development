---
name: work-streams
description: Parks and resumes named work streams — parallel threads of work in one repo, like "fix skipped tests" or "refactor the auth flow" — in a personal store outside any repo, so a session's context survives exit or /clear. Wrapping up updates the stream's manifest (goal, state of play), refreshes its task-scoped context files (test logs, progress summaries, temporary learnings), sweeps a per-stream list of repo files that may need updating (a cheatsheet, README, KNOWLEDGE.md, an improvement tracker), and optionally writes a continuation prompt addressed to the next session. Resuming loads all of that back into a fresh session, checks it against the repo's current state, and briefs the user with numbered next steps to pick from before any work starts. Use this whenever the user says "wrap up", "wrap this session up", "park this", "let's stop here for today", "pick up where we left off", "resume the <x> stream", "what streams are open here", or asks to archive, re-activate, or delete a stream — even when they never say the word "stream", ending a session with unfinished work is the trigger. A bare "commit and push" is ordinary git work, not a wrap-up — but an end-of-day remark beside it ("I'm done for today, just commit and push") still earns a one-line wrap-up offer once the git work is done. Not a memory system — a stream is scoped to one piece of work and dies with it.
---

# Work streams

A stream is one named thread of work — "skipped-tests", "auth-refactor" — that outlives any
single session. Several can run in parallel against the same repo. The store lives outside every
repo, is never committed, and holds three things per stream: a manifest (goal and current state),
task-scoped context files (logs, summaries, temporary learnings), and optionally a continuation
prompt for the next session to start from.

This skill is the whole lifecycle: create at first wrap-up, update at every wrap-up, load at
resume, archive when finished. It deliberately does not duplicate permanent-knowledge homes: a
fact that should outlive the stream belongs in the repo (KNOWLEDGE.md, a cheatsheet, CLAUDE.md),
and wrap-up's job is to notice those and route them there, not to hoard them in the store.

Two companion files:

- `setup.md` — the one-time config bootstrap. Read it when Step 0 finds no config file, or when
  the user asks to move the base directory.
- `lifecycle.md` — archiving a finished stream, re-activating an archived one, deleting. Read it
  when a stream is declared finished at wrap-up, or when the user asks for any of those directly.

## The store

```
~/.claude/work-streams-config.md     # config: one base: line (fixed location, see below)
<base>/                              # from config; default ~/.claude/work-streams/
  <project-slug>/                    # repo root's folder name, lowercased
    <stream-slug>/
      stream.md                      # the manifest
      continuation.md                # optional, written only when wanted
      context/                       # task-scoped files, free-form
    archive/
      <stream-slug>/                 # finished streams, moved whole
```

- **The config file's location is fixed** at `~/.claude/work-streams-config.md`, never inside
  `<base>`. It is what says where `<base>` is, so it cannot live there.
- **`<project-slug>`** is the repo root's folder name, lowercased. If the current directory is not
  inside a git repo, use the working directory's own folder name the same way.
- **`<stream-slug>`** is kebab-case and names the work, never a date. `archive` is reserved and
  can never be a stream slug.
- **Cross-repo streams** are ordinary streams whose manifest lists more than one repo in `repos:`.
  A stream lives under the project where it started. Step 0's scan finds it from any listed repo.
- **A stream folder sits at exactly one depth**: directly under its project folder, or directly
  under that project's `archive/`. A `stream.md` anywhere deeper is a stray, handled at Step 0.
- The store is personal and machine-local. Absolute paths are fine inside it. Nothing in it is
  ever committed anywhere.

## The manifest

```markdown
---
stream: <slug>
title: <short human title>
repos:
  - <absolute path to each repo root this stream touches>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

## Goal
<one or two sentences: what done looks like>

## State of play
<current progress and position, rewritten at every wrap-up>

## Update targets
- `<path relative to its repo root>` — <what this stream records there>
- skill: <skill name> — <what to hand it at wrap-up>

## Notes
<anything worth keeping that is not a context file>
```

- **State of play is rewritten, not appended.** A resume needs the current position, not a diary.
  History that nothing reads is stored state with no staleness handling.
- **Update targets** are the repo files this stream is responsible for keeping current, plus
  skills to hand off to at wrap-up (e.g. `repo-knowledge` for a gotcha, `next-improvement` to
  record progress). Seeded at stream creation, edited any time.
- **`updated:`** moves at every wrap-up as mechanical bookkeeping.
- **`continuation.md`** is addressed to the next session as its opening brief: where things
  stand, what to do next, what to avoid. It is rewritten wholesale at each wrap-up, never
  appended to. Keep it to roughly a page. It points at `context/` files by name for the detail,
  and inlines nothing a pointer covers. It is the most optional piece and only exists if the
  user wanted one.
- **`context/`** holds task-scoped files a later session will actually read: a failing-test log,
  a progress table, a temporary learning too task-bound for the repo. Not a dumping ground —
  each file kept is one the next session would otherwise have to regenerate. W2 prunes it at
  every wrap-up, so it only ever holds what the stream still needs.

## Hard rules

Scope: this table indexes the rules that fail silently when skipped — gates, prohibitions, and
surfaces. It deliberately omits every-run behaviour whose omission is visible in the output
(a missed stream shows up as a wrong or missing listing). Absence from this table never means
optional.

| Step | Kind | Hard rule |
|---|---|---|
| 0 (setup.md) | gate | Propose the config file and base directory with their concrete paths, and wait for confirmation before creating either |
| 0 | gate | If the config file or a manifest is malformed, show what was found and ask — never rewrite it or bootstrap over it |
| 0 | surface | Say when the configured base directory does not exist, rather than treating it as "no streams yet" |
| 0 | surface | Surface a slug-matched stream whose `repos:` does not list this repo root, rather than assuming it active |
| 0 | surface | Surface a `stream.md` found at an unexpected depth as a stray — never list it as active, never silently ignore it |
| trigger | surface | Offer wrap-up in one line when a session-end signal rides another request — never launch unasked, never stay silent |
| W1 | gate | Propose a new stream (slug, title, goal, update targets) and wait for confirmation before creating it |
| W2 | surface | Propose context-file prunes at every wrap-up, or say none are needed, rather than letting `context/` grow silently |
| W3 | surface | Say when an update target no longer resolves, or a listed skill is unavailable, rather than silently skipping it |
| W5 | gate | Present the whole wrap-up plan in one message and wait for confirmation before writing any of it |
| R1 | gate | With more than one active stream and none named, list them and wait for the pick, whatever the `updated:` dates suggest |
| R2 | surface | Surface a mismatch between a stream's claims and the repo's current state, rather than silently reconciling it |
| R2 | prohibition | Never run a side-effectful command to verify a stream's claims |
| R3 | gate | Brief the stream's state and propose numbered next steps, then wait — never resume straight into the work |
| lifecycle.md | gate | Confirm before archiving, re-activating, or deleting a stream |
| every write | prohibition | Never write secrets, credentials, or PII into a stream file, including pasted logs — ask how to redact |

*Update this table in the same edit whenever a hard rule is added, removed, or moved.*

**Whenever two or more options are presented for the user to pick from, number them `1.`, `2.`,
`3.`… in a single sequential list**, whatever label each carries. Sites in this skill: the
stream pick at W1 and R1, the next steps at R3, the malformed-config and stray-manifest choices
at Step 0, the base-directory choice in `setup.md`, the slug collisions in `lifecycle.md`, and
any added later. A label explains an option; a number is what the user can
say back ("go with 2") to pick one unambiguously. A single unambiguous recommendation with
nothing else to choose between needs no number.

## Step 0 — Resolve the config and the store

Runs before either flow below.

1. Read `~/.claude/work-streams-config.md`. If it does not exist, read `setup.md` and run the
   bootstrap, then continue here.
2. If it exists but has no parseable `base:` line, show what was found and ask, as a numbered
   choice:
   1. fix it into the expected format
   2. re-bootstrap via `setup.md`
   3. give a one-off base path for this run only
3. If the configured base directory does not exist, that is a third state, not an empty store.
   The store may have moved or the config may be stale. Say what was expected where, and ask.
4. Resolve `<project-slug>` from the current repo root. A stream is active for this project when
   its folder sits under `<base>/<project-slug>/` outside `archive/`, or its manifest's `repos:`
   lists this repo root (scan the other project folders' manifests for that — it is one glob and
   a few frontmatter reads). A slug-matched stream still has to name this repo root in its
   `repos:`, because two repos can share a folder name. A slug match without a `repos:` match is
   surfaced, not assumed active.
5. Glob `stream.md` at any depth when scanning, not only at the expected level. A manifest
   deeper than one level under the project folder (or one under `archive/`) is a stray — a
   botched move, a hand-copied folder, a checkout dropped into the store. Never list a stray as
   active, and never silently ignore it. Surface each one as a numbered choice:
   1. move it up to be a real stream
   2. it is reference material — leave it where it sits
   3. delete it
6. A manifest that exists but does not parse into the format above gets the malformed gate: show
   it, ask, never rewrite it silently.

## Wrapping up

Trigger: the user is ending or pausing a session — "wrap up", "park this", "let's stop here".
When the signal rides another request — "done for today, just commit and push" — complete that
request first. Then offer wrap-up in one line rather than launching the flow. Silence loses the
signal, and launching unasked hijacks the request the user actually made.

**W1 — pick the stream.** List the active streams for this project, numbered, and say which one
this session's work looks like it belongs to. If none fits, propose a new stream — slug, title,
goal, and update targets seeded from what the repo already has (a KNOWLEDGE.md, an improvement
tracker, a CLAUDE.md, an obvious cheatsheet) — and wait for confirmation. If the user declines a
stream altogether, skip to W3. The repo-file sweep still has value without a store entry, and
nothing gets written to the store.

**W2 — draft the store updates.** Rewrite State of play to the current position. Decide which
context files to add or refresh, keeping only what a later session will read. Then prune: list
what `context/` already holds, and propose the removal of anything the work has outgrown — a
superseded log, a learning now resolved or graduated to a repo file. Propose prunes at every
wrap-up, or say none are needed, rather than going quiet. An unbounded `context/` defeats the
folder's point: each stale file kept is one a resume has to consider loading. Move `updated:`.
Draft, do not write — everything lands together at W5.

**W3 — sweep the update targets.** For each entry in the manifest (or, with no stream, each
obvious candidate in the repo):

- Check the path still resolves. A target in a repo not currently checked out cannot be checked
  from here — say so rather than passing or failing it. A dangling path is surfaced with a
  proposed fix or removal, never silently skipped.
- Judge whether this session's work belongs in it, and draft the edit if so.
- For `skill:` entries, hand off to that skill's own flow. If the skill is not available here,
  say so.
- Then ask the one open question: did this session surface anything else that should be recorded
  somewhere permanent? This is the catch-all for what no listed target covers.

**W4 — offer the continuation prompt.** One line, unless the user already said either way. If
wanted, draft `continuation.md` to its rules under "The manifest" above.

**W5 — one gate, then write.** Assemble everything from W2–W4 into a single plan: store writes,
repo-file edits, the continuation draft. Alongside it, ask whether the stream is finished or
stays active. Present the whole plan in one message and wait for confirmation before writing
any of it. Then write it all and report what was written where. If the stream is finished, read
`lifecycle.md` and follow its archive flow.

## Resuming

Trigger: the user wants to pick work back up — "resume the skipped-tests stream", "pick up where
we left off", "what streams are open here".

**R1 — identify the stream.** A named stream resolves directly. With exactly one active stream,
"pick up where we left off" resolves to it. With more than one, list them numbered, with each
one's title and `updated:` date, and wait for the pick. Say which one the request looks closest
to when anything in it points at one. A closest match and an `updated:` date are hints, never
the pick itself. Load and brief exactly one stream. A user who wants a second one asks for it,
and it gets its own R2 and R3. A request that only asks what is open ends here, with the list.

No active streams is a plain answer, not an error. A named stream missing from the active list
may be archived. Check `archive/` before answering that it does not exist. On a hit, offer
`lifecycle.md`'s re-activation.

**R2 — load and verify.** Read the manifest and `continuation.md` if present. List the names of
what `context/` holds; read individual files as the work needs them, not all up front. The
stream's claims were true at the last wrap-up, not necessarily now. Cheaply verify that what it
names — a branch, a file path, a command's definition — still exists. Surface any mismatch
between the stream's claims and the repo's current state, rather than silently reconciling it.
R3's briefing is where that is said, so each mismatch is reported once.
Never run a side-effectful command to verify it.

**R3 — brief, then stop.** Give it in one message:

- the stream's goal, and where State of play left it
- what R2's verification found, including every mismatch with the repo as it stands now
- the next steps, numbered, each one concrete enough to start from. One obvious next step is a
  recommendation, not a list of one

Then wait. Never begin the work because the manifest or the continuation prompt names what it
is. The user is returning to a stream that is days old, and the position is what they need
first. A request that already names the work to do is itself the pick, and the briefing still
comes first. If the goal turns out to be already met, say so here and suggest wrapping up and
archiving instead of proposing steps.

**R4 — work.** Continue with the step the user picked. The store is written at a wrap-up, never
by a resume.
