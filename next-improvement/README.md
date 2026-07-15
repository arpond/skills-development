# next-improvement

A repeatable "what should we work on next" loop for any project. Instead of re-deciding from
scratch every session what to build next, it maintains a per-project `IMPROVEMENT_TRACKER.md`:
a small set of idea categories, a tiered list of priorities, and a running history of what's
shipped (and what's been rejected, and why). Each time it runs, it proposes fresh ideas for any
category that's run thin, ranks whatever's outstanding against the project's own priority
tiers, and proposes the next thing to build — but never writes a new idea to the tracker, starts
planning, or starts building anything without the user confirming first.

Files:
- `SKILL.md` — the steady-state loop (ties, idea top-up, ranking, propose/
  confirm/plan/build/record). Always loaded when the skill triggers.
- `session-start.md` — finding/bootstrapping the tracker and checking whether Goals are stale.
  Read every run, right after `SKILL.md`'s intro — unlike the other companion files below, it's
  not optional or one-time, just split out to keep `SKILL.md` itself focused on the loop.
- `setup.md` — the one-time-per-project bootstrap interrogation. Only read the
  first time the skill runs for a project, before its tracker file exists.
- `strategies.md` — optional alternate ways of presenting candidates (spread
  across tiers, a wildcard slot, a quick-win lane, category rotation). Only read when a project
  actually configures a `Selection strategy:` beyond the default. See that file for the full
  option reference (syntax, defaults, and how modes combine).
- `feedback.md` — an optional loop that asks how past ships actually landed
  (delivered / mixed / missed) and feeds that back into future judgement, capped so it never
  turns into a nagging backlog. Only read when a project has `Feedback: on`.

## Requires

Nothing beyond local file read/write — no MCP server, no external service. The one optional
dependency is Claude Code's plan mode, used for the approval flow in Step 4.5 if available;
falls back to presenting the plan inline and waiting for a go-ahead otherwise.

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
        Based on the codebase, I'd propose these idea categories: Features, Refactors.
        And this priority order: (1) fix broken/flaky behaviour, (2) ship features users
        are waiting on, (3) pay down debt that's slowing things down. Does that order
        match what actually matters right now, or would anything swap?

You: Swap 1 and 2, we don't have anything broken right now.

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

Claude: Last shipped "Add retry logic" (3 weeks ago) — deliver as expected, mixed, or miss?

You: Delivered as expected.

Claude: 1. Tier 1 pick: "Fix pagination bug" — because X.
        2. Tier 2 pick: "Add dark mode" — because Y.
        3. Wildcard: "Rewrite the CSV export" — oldest idea in the backlog, worth
           a second look.
```

(The feedback check-in runs at session start, before candidates are ranked — not appended after
the proposal. If Goals were also due a check-in this run, both questions would be folded into
that same opening message instead of asked one after another.)
