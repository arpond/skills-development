# repo-knowledge

A place for the "why"-shaped facts about a repo that cost someone real time to (re)discover but
don't live anywhere else — not derivable from reading the code, not covered by `CLAUDE.md` (which
documents the repo as designed, not gotchas hit along the way), and not reliably captured in
commit messages (commit quality varies by author). Instead of that knowledge staying in Slack
threads, an incident channel, or someone's head until they leave, this skill captures it into a
per-project `KNOWLEDGE.md` at the moment it's discovered, applies a deliberate capture bar to keep
the file from filling with noise, and runs an occasional review to prune entries that have gone
stale or never turned out to matter.

Files:
- `SKILL.md` — the steady-state loop: reference existing entries when relevant work touches them
  (with a mechanical check that they still hold), capture new entries when something clears the
  capture bar (checking a `Declined` history first so the same idea isn't silently re-proposed or
  silently re-suppressed), and remove entries under three specific conditions. Always loaded when
  the skill triggers.
- `session-start.md` — finding or bootstrapping `KNOWLEDGE.md`, checking `CLAUDE.md`/`AGENTS.md`
  for gotcha-shaped content that should migrate over instead, and checking whether a
  judgment-drift review is due. Read every run, right after `SKILL.md`'s intro — not optional,
  just split out to keep `SKILL.md` itself focused on the loop.
- `review.md` — the occasional judgment-drift review/prune pass (mechanical staleness is handled
  inline in `SKILL.md`; this is the human-judgment pass on top of it). Read when a review is due,
  or on explicit request.

## Requires

Nothing beyond local file read/write — no MCP server, no external service.

## When it triggers

Proactively, whenever a session hits something worth recording:

- A debugging session resolves with a non-obvious root cause.
- A dependency, build, test, or environment quirk trips something up in a way that isn't obvious
  from reading the code.
- Work is about to touch a file/area that an existing `KNOWLEDGE.md` entry already covers.

And explicitly, when you say things like:

- "Note this in repo knowledge."
- "What do we know about this in repo knowledge?"
- "Review/prune repo knowledge."

## Example: first use on a new project

```
You: [after a long debugging session] Ah — it was because the migration runner needs
     DB_MIGRATIONS_URL set even in local dev, the default silently points at the wrong DB.

Claude: No KNOWLEDGE.md yet for this project — this seems worth capturing (cost real
        debugging time, isn't obvious from the code, and would trip up anyone else running
        migrations locally). Want me to create KNOWLEDGE.md and add it? I'd also add a
        one-line pointer to it from CLAUDE.md.

You: Yes to both.

Claude: [creates KNOWLEDGE.md with the entry, adds the CLAUDE.md pointer]
        While I'm here — CLAUDE.md has a couple of bullets that read more like gotchas than
        design decisions: 1. "remember to bump the cache version after touching config/" —
        2. "the export job silently no-ops if AWS creds aren't in env." Want me to move
        these into KNOWLEDGE.md instead of leaving them in CLAUDE.md?

You: Yes, move both.

Claude: [adds both as entries to KNOWLEDGE.md, removes them from CLAUDE.md]
```

## Example: referencing an existing entry

```
You: [starts editing migrations/runner.rb]

Claude: KNOWLEDGE.md has an entry for this file — "migration runner needs DB_MIGRATIONS_URL
        set in local dev." Evidence still checks out (env var still referenced at line 12).
        [uses it, bumps Last referenced and the reference count]
```

## Example: an entry has gone stale

```
You: [working in a file an entry references]

Claude: KNOWLEDGE.md's entry "retry wrapper needed around FlakyClient.call" points at
        lib/flaky_client.rb, but that file no longer exists — looks like it was removed.
        Marking Status: needs-review rather than trusting or deleting it silently.
        Was this superseded by something, or should I remove it?

You: Yeah, we replaced FlakyClient entirely last quarter, that note's dead.

Claude: [removes the entry]
```

## Example: a proposed capture gets declined

```
You: [after fixing a minor test flake] That was just a bad test, nothing repo-worthy.

Claude: Fair — noting it as declined (too narrow/one-off) so it doesn't get re-proposed
        if something similar comes up again.
```

## Example: occasional review

```
You: Review repo knowledge.

Claude: KNOWLEDGE.md last reviewed 74 days ago. 3 entries could use a look:
        1. "old S3 bucket permissions quirk" — needs-review, Evidence no longer resolves.
        2. "staging DB seed script order" — needs-review, Evidence no longer resolves.
        3. "webhook retry timing" — never referenced since it was added 3 months ago.
        Want to prune any of these, or keep them as-is? Separately, "flaky CI on the
        payments spec" has been referenced 5 times — might be worth fixing properly or
        adding to CLAUDE.md instead of staying a workaround note.

You: Prune 1 and 2, keep 3 for now, and yes let's look at actually fixing the flaky spec.

Claude: [removes the two confirmed-gone entries, leaves the unreferenced one as-is,
         bumps Last reviewed to today]
```
