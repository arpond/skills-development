# Stream lifecycle: archive, re-activate, delete

Read this when a wrap-up declares a stream finished, or when the user asks directly for any of
the three flows below. All three end in a gate — nothing here happens on the skill's own
judgement alone (see the hard-rules table in `SKILL.md`).

## Archiving a finished stream

A stream is archived when its goal is met or the user calls it done. Two things happen, proposed
together in one message, confirmed once:

1. **The graduation sweep.** Reread State of play, Notes, and the `context/` file names for
   anything that deserves a permanent home now the stream will stop being read: a gotcha for
   `repo-knowledge`, progress for an improvement tracker, a fact for a cheatsheet or README.
   Task-scoped material that dies with the stream stays put — the test is whether someone
   working *outside* this stream would ever want it. Propose each candidate with its
   destination. When the wrap-up's W3 sweep already ran this session, only look for what the
   archive decision itself changes — do not re-propose what W3 just handled.
2. **The move.** Move the whole stream folder to `<base>/<project-slug>/archive/<stream-slug>/`
   and add `archived: <YYYY-MM-DD>` to the manifest's frontmatter.

An archived stream is read-only history. Nothing updates it, no listing of active streams
includes it, and its format is whatever it was when archived.

## Re-activating an archived stream

On request ("bring back the skipped-tests stream"), propose the move back out of `archive/` and
wait for confirmation. Then:

- Remove the `archived:` line from the frontmatter.
- If an active stream already has that slug, that is a numbered choice, not a race:
  1. rename the re-activated stream
  2. rename the active one
  3. keep both under new, distinct slugs
- The repo has moved on since the archive date. Run the same claim-verification as resume's R2 —
  branches, paths, commands the manifest names — and surface what no longer holds, so the first
  session back starts from the real current state, not the archived one.

## Deleting a stream

Only on an explicit ask, never proposed by the skill. Confirm before deleting, naming exactly
what is lost: the manifest, the continuation prompt, every context file, active or archived.
Mention once that archiving keeps the history instead, then respect whatever the user answers.
There is no undo — the store is not under version control.
