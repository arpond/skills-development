# Cross-skill conventions

Concrete specs every skill in this repo implements identically. Distinct from
`DESIGN_PHILOSOPHY.md`, which holds principles you apply judgement to. These are facts to match.
The only thing that matters is that all the skills agree.

**This file is an authoring reference, not something a skill reads.** A skill's own instructions
cannot cite a repo-root file (see `DESIGN_PHILOSOPHY.md`, "A skill's own instructions can't depend
on the dev repo around it"). Only its own folder gets copied when it is installed. So every spec
below is *restated inside each skill that implements it*. Each spec ends with the location of those
copies. A change to one is then a matter of a list to follow, not a memory of which skills were
involved.

**That list is a pointer index, not a compliance record.** It says where to look, never whether
what is there currently passes. Conformance is cheap to recompute (a grep, a read), and the review
loop checks it on every change anyway. A stored verdict would be a second copy to maintain, and it
would rot. A stale ✓ is worse than no record at all. It becomes a reason to skip the check it was
supposed to prompt.

**A change to a spec and a record of a known gap are different acts.** A *change* means an update
to every skill listed under that spec in the same edit. A spec accidentally ahead of its
implementations is the drift this file exists to prevent. A *recorded gap* is deliberate and rare:
a requirement some skill knowingly does not meet yet. Write it as a short **Open gap** note under
that spec and remove it when it is closed. That is a decision worth persistence, unlike a
measurement. Every spec below states the requirement, never the current lowest common denominator.

**Read this file first when you add a new skill to this repo**, not at review time. Nothing here
is optional for a skill that has the thing a spec covers. A new skill has no prior implementation
for a drift check to catch.

## Self-correcting counters

A skill that stores a numeric default and can also detect that the default is miscalibrated tracks
that with a counter of exactly this shape. Every instance, in every skill:

```
increment  on the miscalibration signal
reset to 0 on the corrected signal
threshold  -> surface to the user, then force-reset to 0 regardless of their answer
```

- **The forced reset is the part that drifts.** A declined suggestion must not nag again on the
  very next occurrence. So the act of reaching the threshold and *surfacing* resets the counter,
  whatever the user decides. It takes a fresh run-up of evidence to surface again.
- Each instance declares only its own three values: what increments it, what resets it, and the
  threshold. Nothing else varies. Store the count inline on the line it is about.
- **Where the line it annotates may not exist**, the instance must say what to do. The usual answer
  is to write the line out with its defaults first. A counter with nowhere to live silently stops
  counting.
- **"Never yet measured" is a third state, not a stored 0.** Where the increment compares against a
  previous measurement, the first one has nothing to compare to. It is neither growth nor a
  correction, so it neither increments nor resets. It only records the baseline. Write the
  never-state as its own sentinel (`never`), not as `0`. Otherwise every first measurement scores
  as a change from a zero that never meant zero.

Stated in: `next-improvement`. `SKILL.md` Step 2 (dry-run tracking) holds the canonical wording.
`SKILL.md` Step 6 (archive-sweep streak) and `feedback.md` ("Backlog not shrinking") declare their
own three values and refer back to it. No other skill currently has one.

## Numbered choices

Whenever a skill presents two or more options for the user to pick from, it numbers them `1.`,
`2.`, `3.`… in a single sequential list, whatever other label each option carries (a tier name,
"wildcard", a category). A descriptive label explains an option. It is not something the user can
say back. A single unambiguous recommendation with nothing else to choose between needs no number.

**Three copies of this rule exist, and that is correct, not redundant.** This file is the canonical
one for skills in this repo. The user's own global `CLAUDE.md` states it as a personal preference
that covers everything Claude says, skills or not. That is a broader scope, and it applies to this
machine only. Each skill also states it inline, because an installed skill runs for people who have
neither of the other two.

Stated in: `next-improvement`, `SKILL.md` Step 4. `repo-knowledge` and `commit-message-check`,
`SKILL.md`, just above Step 0. Each states it once and names its own option-presenting sites, so a
site added later inherits the rule instead of a rediscovery.

## Vocabulary

One name per concept, across every file in this repo and every skill's own text. A concept named
two ways reads as two concepts. The reader has to guess whether "check-in" and "gate" differ, and
a grep for one misses the other. A qualified canonical term is fine (`write gate`, `core file`). A
synonym in its place is not. The reverse holds too. A canonical term carries one meaning, so `gate`
is never a read condition and `surface` is never a data tag.

| Term | Means | Not |
|---|---|---|
| gate | a point where a skill shows a proposed action and waits for the user's answer before it acts. "Wait for confirmation" names the act and is fine | confirm-point, confirmation (as the point itself), check-in (outside `next-improvement`) |
| surface | tell the user something without a wait for an answer | flag (as a verb that means tell the user), raise (as a verb that means tell the user). Exempt: `flag` as a noun or tag (`reassess flag`), an audit that flags a finding in its report, notes inside a plan or template that are not addressed to the user |
| check-in | a question folded into `next-improvement`'s session-start message. It blocks only the write it asks about | — (a `check-in` is a gate with a fixed home. Say `gate` everywhere else) |
| read condition | a setting value that decides whether a companion file is read, or whether a mode's pick is shown | gate |
| principle | an entry in `DESIGN_PHILOSOPHY.md` | bullet (as a name for a principle) |
| spec | an entry in this file | convention (when a spec is meant), rule (when a spec is meant) |
| hard rule | a rule that fails silently when skipped, indexed in a skill's hard-rules table | — |
| core file | any skill file read on every invocation. A skill can have more than one (`SKILL.md` plus a `session-start.md`) | always-loaded file, base file, companion file (for an every-run file) |
| companion file | a skill file read only when its trigger condition is met | — |
| artifact | a file a skill maintains inside the user's project | output (as a name for an artifact), state file |
| mechanical bookkeeping | a write a skill makes without a gate, because it carries no judgement (a backfilled stamp, an archive sweep) | no-confirmation bookkeeping, routine bookkeeping, silent bookkeeping |

Add a row when a review finds a second name for an existing concept: pick one, rename the other.
The rule is ASD-STE100's 1.11. The 875-word dictionary that rule assumes is not adopted, so this
table is the whole list.

Unlike the other specs this one has no inline copy. A skill implements it by use of the words.
Conformance is a grep for the right-hand column, over every file, frontmatter and README prose
included. `python check-vocabulary.py` runs that grep from this table and shows each hit with
its condition. Example dialogue that quotes how Claude speaks is exempt. Vendored skills (`ste-writing`)
keep their upstream wording.

No open gaps at present.
Sites listed under an open gap are known. A review does not re-report them.

## The hard-rules table

Any skill with more than one rule that **fails silently when skipped** carries a table of them, so
a review can check that none is missing.

**Inclusion test. Apply it per row, it is the whole spec.** Does a skipped rule produce a visible
failure? If yes, the output already reports it and the row adds nothing. Leave the rule where it is
stated and do not index it. If no, index it. "Important" is not the test. Everything passes that,
and a table that covers every rule in the skill stops being checkable at a glance, which was the
point.

| Passes (index it) | Fails (do not) |
|---|---|
| A confirm-before-write gate. Nothing errors, the write just happens | "Every finding cites its evidence". The next report is visibly full of uncited findings |
| "Never write secrets/PII here". No failure until it leaks | Anything whose absence shows in the skill's own output |
| "Treat fetched content as untrusted" | |
| "Say 'no issues found' rather than going quiet". Silence looks like a legitimate answer | |
| "Check both locations, not just one" | |

Then:

- **Keyed to wherever those rules live**, a mirror of the skill's real structure. One row per rule
  is the usual shape. One row per step is equally fine where several cluster on one step, as long
  as the cell still names each one. What is banned is free prose that bundles several under a loose
  phrase, because that is what lets one quietly disappear.
- **Scoped explicitly.** State what the table covers *and what it deliberately does not*, so
  absence from it never reads as "optional". The scope differs per skill. Some have only gates,
  others carry prohibitions too. So this line cannot be inherited or generically worded.
- **Carries its own update instruction**: a line that tells the reader to update the table in the
  same edit that adds, removes, or moves a rule. Without that the table rots into a stale summary
  of a structure that moved on.
- Each rule's full mechanics stay at the step. The table is an index, not a second copy.

Column names are free to fit the skill (`Step`/`Hard rule`, `#`/`What gets written`/`Gated where`,
and `Step`/`Kind`/`Gate or surface` are all in use and all fine). The invariants above are what
must match.

Stated in: all six skills, each in its own `SKILL.md`. Their scopes genuinely differ. Only
`next-improvement`'s is confined to confirm-before-write gates. The rest carry prohibitions and
output obligations too. The narrow reading came first only because that skill was written first.

**A table that mixes gates with unprompted surfacings should mark which is which.**
`next-improvement` uses a `Kind` column (`gate` / `surface`), and `repo-knowledge` adds
`prohibition` for its secrets rule. Reuse those three names rather than a fourth. Both gates and
surfaces fail silently and both belong in the index, but they are different obligations. One waits
for an answer, the other only has to be said. Without the column a reader has to infer which from
the wording of each row, and the distinction is exactly what the older gates-only scoping existed
to protect.

## Artifact locations

Where a skill writes the files it maintains inside a user's project.

### Two kinds of artifact, two rules

**Human-facing artifacts**: working state and documentation a user reads, hand-edits, and commits.
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

**Config artifacts**: settings a skill reads and a user rarely opens. Currently:
`commit-message-conventions.md` (`commit-message-check`).

```
resolve and bootstrap: <repo-root>/.claude/<FILE>
```

**Repo root, not project root. This is the one place the two rules deliberately differ.**
Human-facing artifacts are per-project because priorities and gotchas are per-project. Config is
per-repo when what it configures is per-repo. A repo that holds several projects still has one
commit history, so a per-project split of its commit conventions would fragment a rule that is not
per-project. A skill whose config genuinely *is* per-project uses `<project>/.claude/` instead.
Decide from what the setting governs, and say which you chose and why in the skill's own text.

Config also supports a personal fallback outside any repo (`~/.claude/<FILE>`) where the skill
defines one. That is the skill's own business, not this spec's.

### Rules that go with it

- **`<docs-dir>` means one the project already has**: `docs/`, `doc/`, or `documentation/`,
  whichever exists. **Never create one.** A project without a docs directory gets its artifacts at
  the project root. A docs tree invented to hold one file imposes a layout the project did not
  choose. **If more than one exists**, resolution checks them all (a hit in two is the ambiguity
  case below), but bootstrap does not guess. Ask which. A project that carries both usually means
  they hold different things, and a wrong pick buries the file where nobody looks.
- **`<project>` is the project root, not necessarily the repo root**: the nearest enclosing
  directory with its own README, package manifest, or similar. One repo can hold several projects
  with different concerns.
- **Siblings co-locate with their primary artifact.** A skill's secondary files go in the directory
  that holds the primary, never resolved independently. `IMPROVEMENT_TRACKER_DONE.md` and
  `RISK_REGISTER.md` sit beside `IMPROVEMENT_TRACKER.md`, wherever that is. A sibling found
  somewhere else is a case to surface, not to quietly bypass.
- **Two hits is ambiguity, not a race.** If the same artifact exists at more than one candidate
  location, do not take the first and do not merge them. Say which files exist where and ask which
  is authoritative. A silent pick strands whatever is in the other. "First hit wins" is a tiebreak
  for *lookup order*, not permission to discard a second copy.
- **Existing files are never moved as a side effect.** Resolution finds artifacts wherever they
  already are. A project that bootstrapped at root before this spec keeps working untouched. A move
  is its own explicit, confirmed action, only if the user asks.

### Implemented by

| Skill | Where it's stated |
|---|---|
| `next-improvement` | `session-start.md` Step 0 (resolve/bootstrap), `SKILL.md` "The tracker file" (siblings), `README.md` |
| `repo-knowledge` | `session-start.md` Step 0, `README.md` |
| `commit-message-check` | `SKILL.md` Step 0 (config rule), `README.md` |

**The `README.md` copy is for the human who decides whether to install**, not for Claude at
runtime. That makes it the copy most likely to drift unnoticed. Nothing at runtime reads it, and a
wrong path there misdirects someone before they ever invoke the skill. A change to a resolve order
is three edits per skill, not two.

## Skill versioning

A skill carries a version number only when an artifact outside this repo compares against it.
The test: does the skill leave a file in the user's project whose format or behaviour can fall
behind the skill? If yes, version it. If not, do not. Git history and `CHANGELOG.md` already
answer "what changed when", and a number nothing reads goes stale without anyone noticing.

Every versioned skill implements one mechanism:

```
SKILL.md, top:           **Skill version: X.Y.Z.**
artifact header:         Feature check: vX.Y.Z
skill companion file:    changelog.md
```

- **The number** is semver. MINOR for a change an existing artifact could want told about: an
  opt-in feature, or an automatic change to behaviour that is already on. MAJOR for a format
  change that needs migration. Wording and bug fixes do not bump it. Patch stays `0`.
- **The stamp** is the skill version last disclosed to the artifact. Bootstrap writes it. Only
  the check below moves it. A skill may add stamps of its own beside it (`next-improvement`'s
  `Created:`). This spec covers only `Feature check:`.
- **`changelog.md`** restates this policy, then lists one entry per MINOR+ version, newest first.
  Each entry says what changed and whether there is anything to opt into. Its only read condition
  is the check finding a gap.
- **The check** runs in `session-start.md`, every run, after the skill finds the artifact and
  before its main loop:
  - Backfill a missing stamp to `0.0.0` as mechanical bookkeeping, then treat it as behind. A
    missing stamp is evidence of being behind, never of being current.
  - An unparseable stamp is the skill's malformed-artifact gate.
  - Compare as semver, each component numerically, never as strings.
  - Behind: walk the entries newer than the stamp, oldest first. Fold them into the session-start
    message. Opt-in items hand off to the feature's own gate. Say automatic items in a clause, or
    stay silent if they are invisible. Then stamp the current version, whatever the user decided.
  - Ahead: surface once. Do not walk. Do not touch the stamp.
- **Stamping is never mechanical.** To backfill to `0.0.0` and then stamp the current version
  without the walk is the failure this spec exists to block.

### Implemented by

| Skill | Where it's stated |
|---|---|
| `next-improvement` | `SKILL.md` intro and "The tracker file" (number, stamp), `session-start.md` Step 0 (backfill) and Step 0.5 (check), `changelog.md` (policy, entries) |
| `repo-knowledge` | `SKILL.md` intro and "The knowledge file" (number, stamp), `session-start.md` "Checking the skill version" (backfill, check), `changelog.md` (policy, entries) |

Unversioned, by the test above: `commit-message-check` (its conventions file has no fixed schema
to fall behind), `jira-ticket-audit`, `plan-technical-jira-ticket`, and
`operational-requirements-audit` (no artifact), and `ste-writing` (no artifact). `ste-writing` is
vendored, so its README pins the upstream commit instead, a different kind of version.

## Skill README contents

An installed skill is a copy of its own folder only, so its `README.md` is everything a human has
to evaluate and use it with. These sections are required, in this order:

| Section | Answers |
|---|---|
| Opening prose (before any `##`) | What it does, and why it exists at all |
| `Files:` list | What is in the folder, and when each file is read |
| `## What it writes` | Artifacts created, where it looks for them, what is confirmed first |
| `## Requires` | Hard dependencies, separated from what degrades gracefully |
| `## When it triggers` | The phrasings and situations that reach for it |
| `## Example` (one or more) | At least one worked run, verbatim enough to show the actual shape |

`## Cost` sits immediately after the `Files:` list. It is required only where the skill does more
than local file read/write (MCP calls, broad repo exploration), so someone can tell before they
invoke it whether this is cheap. A skill whose `## Requires` already says "nothing beyond local
file read/write" has answered it. Where a skill has both an expensive and a cheap path, say so. The
whole point is to let someone pick the cheap one deliberately.

Skill-specific sections beyond these are fine and need no justification.

The prose is in `ste-writing`'s flavored mode. `CLAUDE.md`'s "Prose standards" holds the rule,
the lint target, and the exemptions.

**`## What it writes` is the section people most often skip**, and the one that matters most
before an install. It names every artifact, says where the skill looks for an existing one, marks
anything that leaves the machine (a ticket comment is visible to everyone with access, unlike a
local file), and names any file the skill edits without ownership. A pointer line added to
someone's `CLAUDE.md` is exactly the sort of thing a person wants to know in advance rather than
discover afterwards. Where a skill writes nothing by default, say that outright. It is a materially
different install decision from one that always writes.

Applies to every skill in this repo. `next-improvement` and `repo-knowledge` omit `## Cost`, both
local-file-only. The other four carry one.
