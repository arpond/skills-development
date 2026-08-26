# One-time setup: the config file and the base directory

Read this only when Step 0 found no `~/.claude/work-streams-config.md`. It runs once per
machine, not per project or per stream.

## Step 1 — Check for an existing store

A store can exist without a config (copied from another machine, or the config was deleted).
Before proposing anything, check whether `~/.claude/work-streams/` already exists and contains
project folders. If it does, say so — the proposal below then reconnects the config to it rather
than creating a fresh store.

## Step 2 — Propose, concretely

Show exactly what will be created and where, and wait for confirmation. The default is a real
decision the user has to see, not a formality:

- `~/.claude/work-streams-config.md` — the config file, always at this fixed path.
- The base directory, as a numbered choice:
  1. `~/.claude/work-streams/` — the default. Every stream this skill ever writes lands under it.
  2. A custom path the user names instead.

Nothing is created until they answer.

## Step 3 — Write

Create the base directory (if it does not already exist) and write the config:

```markdown
# Work streams config

Read by the work-streams skill. `base:` is where every stream lives.

base: ~/.claude/work-streams/
```

With a custom path, write that path on the `base:` line instead. Then return to Step 0 in
`SKILL.md` and continue.

## Changing the base later

Editing the `base:` line is all it takes for new lookups — but the existing store does not move
itself. Moving it is the user's own copy, done deliberately, never a side effect of a config
edit. Step 0 catches a configured base that does not exist. A base that exists but is empty
looks like "no streams yet", so after a config edit, check the old path still holds nothing
before trusting an empty listing.
