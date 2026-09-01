# next-improvement

A repeatable "what should we work on next" loop for any project. Instead of a fresh decision
every session about what to build next, it maintains a per-project `IMPROVEMENT_TRACKER.md`: a
small set of idea categories, a tiered list of priorities, and a running history of what shipped
and what was rejected, with reasons. Each run proposes fresh ideas for any category that ran thin,
ranks the outstanding ideas against the project's own priority tiers, and proposes the next thing
to build. It never writes a new idea to the tracker, starts a plan, or starts a build until the
user confirms.

Files:
- `SKILL.md` — the steady-state loop (ties, idea top-up, ranking, propose/confirm/plan/build/
  record). The core file, read every time the skill triggers.
- `session-start.md` — finds or bootstraps the tracker, checks whether the tracker is behind this
  skill version, checks whether Goals are stale, and surfaces due reassess flags and revisit
  dates. Read every run, right after `SKILL.md`'s intro. A second core file, not a companion: not optional
  or one-time, only separated to keep `SKILL.md` focused on the loop.
- `setup.md` — the one-time-per-project bootstrap interrogation. Read only the first time the
  skill runs for a project, before its tracker file exists.
- `strategies.md` — optional alternate ways to present candidates (spread across tiers, a
  wildcard slot, a quick-win lane, category rotation). Read only when a project sets a
  `Selection strategy:` beyond the default. That file holds the full option reference (syntax,
  defaults, and how modes combine).
- `feedback.md` — an optional loop that asks how past ships landed (effective / partial /
  ineffective) and uses the answers in future judgement. Capped, so it never becomes a nagging
  backlog. On by default. Skipped only when a project sets `Feedback: off`.
- `risk-register.md` — an optional loop that traces which shipped ideas needed follow-up fixes or
  reworks, or had bad outcomes. It persists each as a named risk area, keyed to the files or
  modules it is about, in a sibling `RISK_REGISTER.md`, and cross-references future proposals
  against it. Off by default. Read only when a project has `Risk register: on`.
- `tracker-maintenance.md` — rare per-project edge cases: minting or migrating idea ids, catching
  up a tracker older than the skill's version stamps, and retiring, merging, or narrowing an idea
  category. Read only when one of those occurs.
- `changelog.md` — what each skill version added, plus the versioning policy. Read only when an
  existing tracker is behind the installed skill version.

## Cost

Cheap on the common path, and no MCP server or external service on any path. Two things cost more
than a file read. Topping up a category (Step 2) explores the project to ground new ideas: recent
commits, new or changed files, rough edges, test gaps. That runs only when a category drops below
about three items, not on every run. Planning a confirmed pick (Step 4.5) can hand off to another
skill, and one of those may be expensive. `plan-red-team` spawns a panel of subagents. The offer
says so, the handoff is never automatic, and declining leaves the step as cheap as it ever was.

## What it writes

All inside the project you work in. Nothing elsewhere on your machine, nothing off it.

- **`IMPROVEMENT_TRACKER.md`** — the tracker itself, created on first use after a setup
  conversation. One per project (the directory with its own README or package manifest, not
  necessarily the repo root).
- **`IMPROVEMENT_TRACKER_DONE.md`** — appears once Done history gets long. Older shipped entries
  move here automatically, so the live tracker stays a manageable read. Opened only when older
  history is needed.
- **`RISK_REGISTER.md`** — only if you set `Risk register: on`. It is off by default.

**Where it looks:** the project root first, then the project's own docs directory (`docs/`,
`doc/`, `documentation/`) if it has one, then `.claude/`. It uses an existing tracker wherever it
finds one and never moves it. A new tracker goes into the docs directory if the project already
has one, otherwise the project root. It never creates a docs directory to hold it. The other two
files always sit beside the tracker, wherever that is.

The skill shows and confirms every write first, apart from mechanical bookkeeping (a shipped item
moved to Done, entries aged into the archive).

## Requires

No hard dependencies. No MCP server, no external service, and nothing the skill cannot do with
local file read and write plus reading the project it is pointed at (see `## Cost`). Three
optional dependencies, all in Step 4.5. Claude Code's plan mode carries the approval flow when it is
available. Without it, the skill presents the plan inline and waits for a go-ahead. A skill that
interviews you about a plan, such as `grill-me`, gets offered before the plan is drafted. A skill
that attacks a drafted plan, such as `plan-red-team`, gets offered after it. Without either, the
skill says nothing and plans as it always did.

One internal dependency is worth knowing before you turn things on. The risk register records a
mitigation as planned, then relies on the feedback loop to ask how it landed. With the risk
register on and feedback off, nothing ever asks, so those mitigations stay unchecked for ever. The
skill says so the first time it would matter, but the pairing is easier to get right at setup.

## When it triggers

Claude reaches for this skill when you say things like:

- "What should we work on next?"
- "What's next on the improvement tracker?"
- "Any more ideas for this project?"
- Starting a work session on a project with nothing specific queued up.

## Example: first run on a new project

```
You: What should we work on next?

Claude: No IMPROVEMENT_TRACKER.md yet for this project — let's set one up.
        Based on the codebase, I'd propose these idea categories: Refactors, Features.
        And this priority order: (1) fix broken/flaky behaviour, (2) pay down debt that's
        slowing things down, (3) ship features users are waiting on. Does that order
        match what actually matters right now, or would anything swap?

You: Actually features matter more to us right now than debt — swap 2 and 3.

Claude: [writes IMPROVEMENT_TRACKER.md with confirmed tiers, then brainstorms ideas
         for both categories grounded in the actual codebase]
        Proposed for Features: ... Proposed for Refactors: ... — add these?

You: Looks good, add them all.

Claude: [appends the confirmed ideas, ranks them, and proposes the top candidate
         with reasoning tied to the tiers]
```

## Example: steady-state run

```
You: What's next?

Claude: Goals last reviewed 3 weeks ago, nothing suggests drift — skipping that check.
        Top candidate: "Add retry logic to the sync job" — serves tier 1 (nothing's
        broken, but this is the closest thing to a reliability gap) and touches one
        function. Want me to build it, or is something else more pressing?

You: Build it.

Claude: [writes a detailed implementation plan — what changes, where, how it'll be
         verified — and asks for approval before touching any code]

You: Looks good, go ahead.

Claude: [implements per the plan, then moves the item to Done in the tracker with a
         one-line note on what actually shipped]
```

## Example: reprioritising mid-project

```
You: Priorities have changed, we need to focus on performance now.

Claude: [jumps to the staleness-check step, updates the Goals tiers, bumps the
         review date — no need to re-run full setup]
```

## Example: with optional strategies/feedback turned on

```
You: Show me more than just one option each time, and check back on whether
     past work actually delivered.

Claude: [sets Selection strategy: spread(3) + wildcard(rotate) and Feedback: on
         in the tracker]

...next run...

Claude: Last shipped "Add retry logic" (3 weeks ago) — worked as intended, partial, or ineffective?

You: Worked as intended.

Claude: 1. Tier 1 pick: "Fix pagination bug" — because X.
        2. Tier 2 pick: "Add dark mode" — because Y.
        3. Wildcard: "Rewrite the CSV export" — oldest idea in the backlog, worth
           a second look.
```

(The feedback check-in runs at session start, before the skill ranks candidates, not after the
proposal. If Goals are also due a check-in this run, both questions fold into that same opening
message instead of one after another.)
