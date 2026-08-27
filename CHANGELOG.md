# Changelog

Changes worth a reader's attention, newest first. This is not the commit log. An entry records
one of three things: what a skill now does for its user, what an author here must follow, or how
the repo is organised. `next-improvement` keeps a versioned changelog in
`next-improvement/changelog.md`. Entries here point to it.

Format: one heading per period, named by theme and dated by its start. Three fixed sections:
Skills, Standards, Tooling. One line per item. Prose in the flavored mode of `ste-writing`.

## Plan red team · 2026-08-26

**Skills**
- `plan-red-team`: new. Attacks a plan with blind persona subagents, a cross-perspective wave,
  and an aggregator that passes reasoned verdicts.
- `plan-red-team`: roster derivation now runs as three blind subagents merged on convergence.
  Configurable at setup, skipped on re-runs.
- `plan-red-team`: a blind review pass closed thirteen findings. Unavailable derivation or
  aggregation now falls back to the main thread, always labelled.

**Standards**
- `DESIGN_PHILOSOPHY.md`: two new principles, *A fallback wears a label* and *An example an
  interpreter can parse is data*.
- `CLAUDE.md` *Review loop*: a blind-subagent variant is offered when the change was authored
  in the same session.

## Work streams · 2026-08-26

**Skills**
- `work-streams`: new. Parks and resumes named work streams in a personal store, with wrap-up,
  resume, archive, and re-activate flows.

## README prose in STE · 2026-08-23

**Skills**
- All seven `README.md` files and `next-improvement/changelog.md`: rewritten in flavored STE. One
  stale fact fixed: the 1.0.0 entry's backfill value.

**Standards**
- `CLAUDE.md` *Prose standards*: every README and per-skill changelog is in flavored STE, like
  `CHANGELOG.md`. Fenced dialogue is exempt.
- Spec *Skill README contents*: carries the prose rule.
- Spec *Vocabulary*: `mechanical bookkeeping` is the one name for a gate-less write. Four other
  spellings renamed.
- `CONVENTIONS.md` and `CLAUDE.md`: rewritten in flavored STE and added to *Prose standards*.
  Vocabulary fixes there and in `DESIGN_PHILOSOPHY.md`: `bullet` to `principle`, `flags` to `marks`.

## Skill versioning · 2026-08-23

**Skills**
- `repo-knowledge`: versioned, at 1.0.0. `KNOWLEDGE.md` gets a `Feature check:` stamp. New
  `changelog.md`.
- `repo-knowledge`: bootstrap says the header stamp moves itself and that an upgrade is disclosed
  once.
- `next-improvement`: `changelog.md`'s policy sentence matches the new spec. No behaviour change.
- `ste-writing`: the README pins the upstream commit that the skill came from.

**Standards**
- Spec: *Skill versioning*. Version a skill only when an artifact outside the repo compares
  against it. One mechanism for the skills that do.
- Principle *Don't persist a signal*: points at the versioning spec for the when-to-version test.
- Spec *The hard-rules table*: `prohibition` is the third `Kind` value.

**Tooling**
- `check-vocabulary.py`: greps every banned name in the Vocabulary table, condition beside each hit.
  Fails loudly on an unparseable table.
- `ste-lint.py`: a possessive `'s` no longer counts as a contraction. Scores drop by about 1 per
  100 words on prose-heavy files.

## Writing standards and `ste-writing` · 2026-08-22

**Skills**
- New: `ste-writing`. Rewrites or reviews prose as Simplified Technical English, with a lint
  script. Vendored. Its README lists the local changes.
- All six skills: each rule is now its own sentence or a list item. The `gate` and `surface`
  vocabulary applies throughout.
- `plan-technical-jira-ticket`: the gates table has a `Kind` column. Two rows were surfaces, not
  gates.
- `repo-knowledge`: `setup.md` dropped `doc/` from the docs-folder list. Fixed.
- `commit-message-check`: `SKILL.md` states the built-in defaults once. `setup.md` points to them.
- `next-improvement`: one throttle for the foreign-section surfacing, not two.

**Standards**
- Principle: *A rule is a sentence, an instruction block is a list*. A rule-bearing sentence has
  at most 25 words.
- Principle: *A review criterion needs a floor*. Three review rounds found 119, 160, then 74
  sites.
- Spec: *Vocabulary*. One name per concept: `gate`, `surface`, `read condition`, `core file`,
  `companion file`.
- Review-loop check 2: three concrete tests, and a list of repetition that is by design.

**Tooling**
- `check-hard-rules.py`: matches each hard-rules row to its prose sentence. Flags long or missing
  sentences.
- `ste-lint.py`: unwraps wrapped markdown, splits bold-edged sentences, and adds `--cap` and
  `--show`.

## Conventions become specs; `next-improvement` 2.x · 2026-08-02

**Skills**
- `next-improvement` 1.1.0 to 2.2.0: skill versioning, risk areas keyed to project paths,
  date-based archiving, bulk id backfill. See its changelog.
- All skills: the README states what the skill writes and where it looks.
- Artifact files (`IMPROVEMENT_TRACKER.md`, `KNOWLEDGE.md`): found in the project root, then a
  docs folder, then `.claude/`. On two hits the skill asks rather than picking one.
- `commit-message-conventions.md`: lives in `.claude/` at the repo root, per repo rather than per
  project.

**Standards**
- `CONVENTIONS.md` created: specs every skill matches identically. Counters, numbered choices,
  the hard-rules table, artifact locations, README contents.
- Hard-rules tables index rules that fail silently, surfacings included, not only gates.
- Pointer indexes replace the conformance scorecards. A stored tick rots.
- Review loop: a core file at or above ~500 lines needs a whole-file skim.

## Design philosophy as a file; `commit-message-check` rebuilt · 2026-08-01

**Skills**
- `commit-message-check` rebuilt. Rules live in a user-owned conventions file, bootstrapped by
  interrogation, organised by message part. A repo-level file merges above the personal one.
- `next-improvement`: idea ids, and an optional risk register (off by default).
- `operational-requirements-audit`: a mechanical age check on the bundled OR text. The
  stage-expectations file ships empty.

**Standards**
- `DESIGN_PHILOSOPHY.md` created, with a table of contents.
- `CLAUDE.md` created: the four-check review loop, offered once after a non-trivial change.
- Seven principles added. Among them: a default the user never saw is not a default. Split
  skills along orthogonal triggers.

## `commit-message-check` and `jira-ticket-audit` · 2026-07-30

**Skills**
- New: `commit-message-check`. A pre-commit gate against conventions the user owns. Rebuilt on
  2026-08-01.
- New: `jira-ticket-audit`. Audits one ticket for ambiguity, gaps, scope, and epic linkage.
  Stage expectations per project. Vertical splits over horizontal.

## `repo-knowledge`, the OR audit, `next-improvement` split · 2026-07-15

**Skills**
- New: `repo-knowledge`. A per-project `KNOWLEDGE.md` of repo gotchas, with a capture bar,
  staleness checks, and a drift review. Bootstrap migrates misfiled gotchas from existing docs.
- New: `operational-requirements-audit`. Audits a repo against the Findmypast ORs from a bundled
  export.
- `next-improvement`: `session-start.md` and `setup.md` are now their own files. Selection
  strategies, knobs, synergy noticing, Done archiving.
- `plan-technical-jira-ticket`: full confirm-points table, mid-plan assumption checks, a plan
  template, a cost warning up front.

## First two skills · 2026-07-13

**Skills**
- New: `next-improvement`. A "what next" loop over a per-project tracker, with
  confirm-before-write gates.
- New: `plan-technical-jira-ticket`. Plans a technical Jira ticket against the real codebase, for
  approval before code.

**Standards**
- Repo shape: one folder per skill with its own README. The top-level README is an index.
