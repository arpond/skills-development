# Cross-skill conventions

Concrete specs every skill in this repo implements identically. Distinct from
`DESIGN_PHILOSOPHY.md`, which holds principles you apply judgement to — these are facts to match,
where the only thing that matters is that all the skills agree.

**This file is an authoring reference, not something a skill reads.** A skill's own instructions
can't cite a repo-root file (see `DESIGN_PHILOSOPHY.md`, "A skill's own instructions can't depend
on the dev repo around it") — only its own folder gets copied when it's installed. So every spec
below is *restated inside each skill that implements it*, and this file exists to check those
copies haven't drifted apart.

**Changing a spec and recording a gap are different acts.** *Changing* one means updating every
skill listed under it in the same edit — a spec that's ahead of its implementations by accident is
the drift this file exists to prevent. *Recording* a gap is the opposite: a requirement some skills
knowingly don't meet yet, written into its own implemented-by table as an explicit `✗`, because a
known gap that's visible is worth more than a spec quietly weakened to whatever everything already
does. Every spec below therefore states the requirement, not the current lowest common denominator.

**Adding a new skill to this repo means reading this file first**, not discovering it at review
time. Nothing here is optional for a skill that has the thing a spec covers, and a new skill has no
prior implementation for a drift check to catch.

## Self-correcting counters

A skill that stores a numeric default and can also detect that the default is miscalibrated tracks
that with a counter of exactly this shape. Every instance, in every skill:

```
increment  on the miscalibration signal
reset to 0 on the corrected signal
threshold  -> surface to the user, then force-reset to 0 regardless of their answer
```

- **The forced reset is the part that drifts** — a declined suggestion must not re-nag on the very
  next occurrence, so reaching the threshold and *surfacing* resets the counter whatever the user
  decides. It takes a fresh run-up of evidence to surface again.
- Each instance declares only its own three values: what increments it, what resets it, and the
  threshold. Nothing else varies. Store the count inline on the line it's about.
- **Where the line it annotates may not exist**, the instance must say what to do — writing the
  line out with its defaults first is the usual answer. A counter with nowhere to live silently
  stops counting.
- **"Never yet measured" is a third state, not a stored 0.** Where the increment compares against a
  previous measurement, the first one has nothing to compare to: it is neither growth nor a
  correction, so it neither increments nor resets — it just records the baseline. Write the
  never-state as its own sentinel (`never`), not as `0`, or every first measurement scores as a
  change from a zero that never meant zero.

| Instance | States the shape | Trigger / reset / threshold |
|---|---|---|
| `next-improvement` — `SKILL.md` Step 2, dry-run tracking | ✓ canonical | ✓ |
| `next-improvement` — `SKILL.md` Step 6, archive-sweep streak | refers to Step 2 | ✓ |
| `next-improvement` — `feedback.md`, "Backlog not shrinking" | refers to Step 2 | ✓ |

No other skill in this repo currently has a self-correcting counter.

## Numbered choices

Whenever a skill presents two or more options for the user to pick from, they're numbered `1.`,
`2.`, `3.`… in a single sequential list, whatever other label each option carries (a tier name,
"wildcard", a category). A descriptive label explains an option; it isn't something the user can
say back. A single unambiguous recommendation with nothing else to choose between needs no number.

**Three copies of this rule exist and that's correct, not redundant.** This file is the canonical
one for skills in this repo. The user's own global `CLAUDE.md` states it as a personal preference
covering everything Claude says, skills or not — broader scope, and it applies to this machine
only. Each skill also states it inline, because an installed skill runs for people who have neither
of the other two.

| Skill | Where it's stated | States the rule |
|---|---|---|
| `next-improvement` | `SKILL.md` Step 4 | ✓ covering every presentation mode |
| `repo-knowledge` | `SKILL.md`, above Step 0 | ✓ covering every site, present and future |
| `commit-message-check` | `SKILL.md`, above Step 0 | ✓ covering every site, present and future |

Each states the rule once and names its own option-presenting sites, so a site added later inherits
it instead of having to rediscover it.

## The hard-rules table

Any skill with more than one confirm-before-write gate carries a table of them, so a review can
check none have gone missing:

- **Keyed to wherever the gates actually live**, mirroring the skill's real structure. One row per
  gate is the usual shape; one row per step is equally fine where several cluster on one step, as
  long as each is still named individually in the cell. What's banned is free prose bundling
  several under a loose phrase, since that's what lets one quietly disappear.
- **Scoped explicitly.** State what the table covers (confirm-before-write gates: show, then wait)
  and what it deliberately doesn't, so absence from it never reads as "optional." Skills have
  always-surface obligations that need no confirmation; without this line the table silently
  implies those are discretionary.
- **Carries its own update instruction** — a line telling the reader to update the table in the
  same edit that adds, removes, or moves a gate. Without that the table rots into a stale summary
  of a structure that moved on.
- Each gate's full mechanics stay at the step; the table is an index, not a second copy.

Column naming is free to fit the skill (`Step`/`Hard rule`, `#`/`What gets written`/`Gated where`,
`Step`/`Confirm-point(s)` are all in use and all fine). The invariants above are what must match.

| Skill | Table | Update line | Explicit scope |
|---|---|---|---|
| `next-improvement` | ✓ "Hard rules by step" | ✓ | ✓ confirm-before-write gates only |
| `commit-message-check` | ✓ write-gate table | ✓ | ✓ consequential writes only |
| `repo-knowledge` | ✓ | ✓ | ✓ gates, prohibitions and must-asks |
| `jira-ticket-audit` | ✓ | ✓ | ✓ mostly output obligations, one gate |
| `operational-requirements-audit` | ✓ | ✓ | ✓ verdict obligations plus three gates |
| `plan-technical-jira-ticket` | ✓ one row per step | ✓ | ✓ every point that waits on the user |

**The scope statements differ per skill, and that's the point of requiring one** — these six tables
turn out to cover six different things, from writes only to output obligations that aren't gates at
all. A generic line would have been worse than none, since it would assert a uniformity that isn't
there.

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
resolve and bootstrap: <repo-root>/.claude/<FILE>
```

**Repo root, not project root — the one place these two rules deliberately differ.** Human-facing
artifacts are per-project because priorities and gotchas are per-project. Config is per-repo when
what it configures is per-repo: a repo holding several projects still has one commit history, so
splitting its commit conventions per project would fragment a rule that isn't per-project. A skill
whose config genuinely *is* per-project uses `<project>/.claude/` instead — decide from what the
setting governs, and say which you chose and why in the skill's own text.

Config additionally supports a personal fallback outside any repo (`~/.claude/<FILE>`) where the
skill defines one; that's the skill's own business, not this spec's.

### Rules that go with it

- **`<docs-dir>` means one the project already has** — `docs/`, `doc/`, or `documentation/`,
  whichever exists. **Never create one.** A project without a docs directory gets its artifacts at
  the project root; inventing a docs tree to hold one file imposes a layout the project didn't
  choose. **If more than one exists**, resolution checks them all (a hit in two is the ambiguity
  case below), but bootstrap doesn't guess: ask which, since a project carrying both usually means
  they hold different things and picking wrong buries the file where nobody looks.
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

| Skill | Where it's stated | Resolve order | Ambiguity case | Siblings |
|---|---|---|---|---|
| `next-improvement` | `session-start.md` Step 0, `SKILL.md` "The tracker file" | ✓ | ✓ | ✓ |
| `repo-knowledge` | `session-start.md` Step 0 | ✓ | ✓ | n/a — single file |
| `commit-message-check` | `SKILL.md` Step 0 | ✓ config rule | n/a — fixed location | n/a |
