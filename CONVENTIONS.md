# Cross-skill conventions

Concrete specs every skill in this repo implements identically. Distinct from
`DESIGN_PHILOSOPHY.md`, which holds principles you apply judgement to — these are facts to match,
where the only thing that matters is that all the skills agree.

**This file is an authoring reference, not something a skill reads.** A skill's own instructions
can't cite a repo-root file (see `DESIGN_PHILOSOPHY.md`, "A skill's own instructions can't depend
on the dev repo around it") — only its own folder gets copied when it's installed. So every spec
below is *restated inside each skill that implements it*, and this file exists to check those
copies haven't drifted apart. Changing a spec here means changing it in every skill listed under
it, in the same edit.

## Artifact locations

Where a skill writes the files it maintains inside a user's project.

### Two kinds of artifact, two rules

**Human-facing artifacts** — working state and documentation a user reads, hand-edits, and commits.
Currently: `IMPROVEMENT_TRACKER.md`, `IMPROVEMENT_TRACKER_DONE.md`, `RISK_REGISTER.md`
(`next-improvement`), `KNOWLEDGE.md` (`repo-knowledge`).

```
resolve (in order, first hit wins):
  1. <project>/<FILE>
  2. <project>/<docs-dir>/<FILE>
  3. <project>/.claude/<FILE>

bootstrap (nothing found):
  <docs-dir>/ if one already exists, else <project>/
```

**Config artifacts** — settings a skill reads and a user rarely opens. Currently:
`commit-message-conventions.md` (`commit-message-check`).

```
resolve and bootstrap: <project>/.claude/<FILE>
```

Config additionally supports a personal fallback outside the project
(`~/.claude/<FILE>`) where the skill defines one; that's the skill's own business, not this spec's.

### Rules that go with it

- **`<docs-dir>` means one the project already has** — `docs/`, `doc/`, or `documentation/`,
  whichever exists. **Never create one.** A project without a docs directory gets its artifacts at
  the project root; inventing a docs tree to hold one file imposes a layout the project didn't
  choose.
- **`<project>` is the project root, not necessarily the repo root** — the nearest enclosing
  directory with its own README, package manifest, or similar, since one repo can hold several
  projects with different concerns.
- **Siblings co-locate with their primary artifact.** A skill's secondary files go in whatever
  directory the primary was found in, never resolved independently — `IMPROVEMENT_TRACKER_DONE.md`
  and `RISK_REGISTER.md` sit beside `IMPROVEMENT_TRACKER.md` wherever that turned out to be. A
  sibling found somewhere else is a case to surface, not to quietly work around.
- **Two hits is ambiguity, not a race.** If the same artifact exists at more than one candidate
  location, don't take the first and don't merge them — say which files were found where and ask
  which is authoritative. Silently picking one strands whatever's in the other, and "first hit
  wins" is a tiebreak for *lookup order*, not permission to discard a second copy.
- **Existing files are never moved as a side effect.** Resolution finds artifacts wherever they
  already are; a project that bootstrapped at root before this spec keeps working untouched. Moving
  one is its own explicit, confirmed action, only if the user asks.

### Implemented by

Each of these restates the above in its own text; keep them in sync.

| Skill | Where it's stated |
|---|---|
| `next-improvement` | `session-start.md` Step 0 (resolve/bootstrap), `SKILL.md` "The tracker file" (siblings) |
| `repo-knowledge` | `session-start.md` Step 0 |
| `commit-message-check` | `SKILL.md` Step 0 (config rule) |
