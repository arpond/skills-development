# Changelog

The changes worth a reader's attention, newest first. This is not the commit log; a commit gets
an entry here only when it changes what a skill does for its user, what an author of a skill in
this repo has to follow, or how the repo is organised. `next-improvement` keeps its own
versioned changelog in `next-improvement/changelog.md`, because its users' trackers carry a
version stamp and get told what changed; entries below point there rather than repeat it.

## 2026-08-22 to 2026-08-23: writing standards, and a vendored skill to enforce them

**New skill: `ste-writing`.** Rewrites or reviews prose in ASD-STE100 Simplified Technical
English to strip "AI slop", with a bundled lint script that scores a draft. Vendored from
[woosal1337/blog, ep01](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop);
its README lists the local changes. The lint script diverges from upstream in four ways that
matter if you run it: it unwraps hard-wrapped markdown before counting sentences (upstream counted
each wrapped line as one, so long sentences in wrapped files never registered), it handles
sentences that open or close with bold, it keeps line numbers true across code fences, and it
gains `--cap N` and `--show`.

**Three STE rules adopted for the repo's own instruction text.** The rest of the standard was
deliberately not adopted: it strips voice, and the reasoning in the shared files is the voice.
- *A rule is a sentence, an instruction block is a list* (`DESIGN_PHILOSOPHY.md`): every rule a
  reader would copy into a hard-rules table is its own sentence of at most 25 words; a block of
  several instructions is a list. Scoped after two review rounds showed the unscoped version
  produced findings in proportion to file size rather than defects (see the next bullet).
- *Vocabulary* (`CONVENTIONS.md`): one name per concept across the repo. `gate`, `surface`,
  `read condition`, `core file`, `companion file`, `hard rule`, `artifact` are now the canonical
  terms; `check-in`, `confirm-point`, `flag`/`raise` (as "tell the user"), `always-loaded` are
  out, with the exemptions listed in the table. `next-improvement`'s `check-in` is a named
  mechanism and keeps its name.
- Review-loop check 2 gained three concrete tests and a list of what is *not* repetition (table
  rows, mandated inline copies, README summaries, a file's own intro).

**Every skill re-edited to the new rules**, one commit per skill per round, across three blind
review rounds. The findings that mattered were a small fixed set: three cross-file drifts
(`repo-knowledge`'s docs-folder list dropped `doc/` in one file; `commit-message-check`'s
built-in defaults had diverged between `SKILL.md` and `setup.md`; `next-improvement` carried two
different throttles for one surfacing), `gate` used for read conditions at seven sites, and a
dozen hard rules buried mid-sentence. `plan-technical-jira-ticket`'s gates table now has a
`Kind` column, since two of its rows were surfaces, not gates.

**New principle: a review criterion needs a floor.** The three review rounds measured 119, then
~160, then 74 findings; the rule had to be bounded before a review of it could converge. Written
up in `DESIGN_PHILOSOPHY.md` so the next new rule ships with its scope.

**New tool: `check-hard-rules.py`.** For every hard-rules table row in every skill, finds the
closest prose sentence and reports whether it fits the cap. A row with no close sentence is a
rule that lives only in the index. A locator, not a verdict.

## 2026-08-02 to 2026-08-03: conventions become specs; next-improvement 2.x

**`CONVENTIONS.md` created**, separating concrete specs every skill matches identically from the
principles in `DESIGN_PHILOSOPHY.md`. Specs at creation: self-correcting counters, numbered
choices, the hard-rules table, artifact locations, and required README contents. Each names
where its inline copies live; the per-skill conformance scorecards that briefly existed were
replaced by pointer indexes, since a stored ✓ rots.

**Hard-rules tables re-scoped.** The inclusion test is now "does skipping this fail silently?",
not "is this important?". Unprompted surfacings are indexed alongside confirm-before-write gates,
with a `Kind` column where a table holds both.

**Artifact locations are resolved, not assumed.** Skills that maintain a file in the user's
project (`IMPROVEMENT_TRACKER.md`, `KNOWLEDGE.md`) look in the project root, then an existing
docs folder, then `.claude/`; two hits is ambiguity to surface, none means bootstrap without
inventing a docs directory. Config artifacts (`commit-message-conventions.md`) live at the repo
root's `.claude/`, deliberately per-repo rather than per-project.

**Every skill README now says what it writes and where it looks** before a reader installs it.

**`next-improvement` 1.1.0 through 2.2.0.** Skill versioning with a changelog walk at session
start; risk entries keyed to project areas instead of stored idea ids; outcome vocabulary renamed
to match the risk register's; date-based Done archiving and feedback re-offers; rare maintenance
cases moved out of the always-loaded file; a session-start fallback for the archive sweep; bulk id
backfill on migration. Details per version in `next-improvement/changelog.md`.

**Review loop gained a size check**: a core file at or above ~500 lines gets a whole-file skim for
progressive-disclosure drift, not just a diff-scoped pass.

## 2026-08-01: design philosophy becomes a file; commit-message-check reworked

**`DESIGN_PHILOSOPHY.md` and `CLAUDE.md` created.** The philosophy moved out of the README into
its own file with a table of contents, and the repo's review loop (four checks after any
non-trivial change, offered once, run on request) was written down. The loop applies to the two
shared files as well as to skills; that asymmetry had already caused drift once.

**`commit-message-check` rebuilt.** Rules are no longer baked in: they live in a conventions file
the skill bootstraps by interrogation on first use, organised around the parts of a commit message
(prefix, subject, body, footer, whole-message, miscellaneous) rather than a fixed list of named
rules. A repo-level conventions file can sit above the personal one, merged per heading. Built-in
defaults are shown and confirmed at bootstrap, never assumed. The strip-test became an opt-in body
technique instead of a default.

**`next-improvement` gained idea ids and an optional risk register** (off by default): recurring
fix/rework patterns in the same part of a project are named, persisted, and checked against future
proposals. A planned idea can claim a risk's mitigation before it ships.

**Seven design-philosophy principles added** from the reworks above, including: a default the
user never saw isn't a default; every write path needs an explicit target; mechanism and personal
preference belong in different files; split skills along orthogonal triggers, not around size.

**`operational-requirements-audit`**: the soft "looks stale" heuristic on the bundled OR text was
replaced with a mechanical age check; the stage-expectations reference ships empty of any personal
data.

## 2026-07-30 to 2026-07-31: two new skills

**`commit-message-check`** (first version, since reworked; see above): a mandatory pre-commit gate
that checks a drafted message against the user's own conventions.

**`jira-ticket-audit`**: audits one ticket for ambiguity, inconsistency, gaps, oversized scope, and
missing epic linkage, with evidence quoted from the ticket. Distinct from
`plan-technical-jira-ticket`, which plans a ticket already judged sound. Gained a per-project
stage-expectations file (so a blank field isn't a gap if the ticket hasn't reached the stage
where it's decided) and a preference for vertical over horizontal splits.

## 2026-07-15 to 2026-07-23: repo-knowledge, the OR audit, and next-improvement's first split

**`repo-knowledge`** added: a per-project `KNOWLEDGE.md` of repo gotchas and root causes that cost
real time to rediscover, with a capture bar, mechanical staleness checks on each entry's evidence,
and an occasional judgment-drift review. Bootstrap scans existing docs (README, CLAUDE.md, TSG,
runbook, docs folders) for misfiled gotchas and offers to migrate them.

**`operational-requirements-audit`** added: audits a repo against Findmypast's Operational
Requirements, bundled as a point-in-time export so verdicts cite the actual wording.

**`next-improvement`** split its every-run Step 0 into `session-start.md` and its one-time
bootstrap into `setup.md`; gained selection strategies (`spread`, `wildcard`, `quick-win`),
configurable knobs, synergy noticing, and a once-per-session throttle on the feedback check-in.
Done history is archived out of the live tracker once it grows.

**`plan-technical-jira-ticket`**: confirm-points table completed; mid-plan assumptions confirmed
with the user; a plan template; the handoff reordered to lead with recording the plan on the
ticket; an up-front warning that the run is investigation-heavy.

## 2026-07-13 to 2026-07-14: the repo starts

**`next-improvement`** (first skill): a repeatable "what should we work on next" loop over a
per-project tracker, with the confirm-before-write gates that became the repo's first hard rules.

**`plan-technical-jira-ticket`** (second skill): turns a well-scoped technical Jira ticket into an
implementation plan grounded in the actual codebase, verified before approval.

**Repo shape settled**: one folder per skill with its own README, the top-level README an index,
and a design-philosophy section that later became its own file.
