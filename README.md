# skills-development

A collection of custom skills for [Claude Code](https://claude.com/product/claude-code).

## Installation

Claude Code loads skills from `~/.claude/skills/<name>/` (user-level, available in every
project) or `<project>/.claude/skills/<name>/` (project-level, that project only). To install
a skill from this repo:

1. Copy the skill's folder into one of those locations, e.g.:
   ```
   cp -r next-improvement ~/.claude/skills/next-improvement
   ```
2. That's it -- no restart needed. Claude Code picks up skills from disk each time it looks for
   one to trigger.

To update an installed skill after pulling changes from this repo, repeat step 1 (overwrite the
existing folder).

## next-improvement

A repeatable "what should we work on next" loop for any project. Instead of re-deciding from
scratch every session what to build next, it maintains a per-project `IMPROVEMENT_TRACKER.md`:
a small set of idea categories, a tiered list of priorities, and a running history of what's
shipped. Each time it runs, it tops up any idea category that's gotten thin, ranks whatever's
outstanding against the project's own priority tiers, and proposes the next thing to build --
but never starts building without the user confirming first.

Files:
- `next-improvement/SKILL.md` -- the core loop (tiers, ties, idea top-up, ranking, propose/
  confirm/build/record). Always loaded when the skill triggers.
- `next-improvement/strategies.md` -- optional alternate ways of presenting candidates (spread
  across tiers, a wildcard slot, a quick-win lane, category rotation). Only read when a project
  actually configures a `Selection strategy:` beyond the default.
- `next-improvement/feedback.md` -- an optional loop that asks how past ships actually landed
  (delivered / mixed / missed) and feeds that back into future judgment, capped so it never
  turns into a nagging backlog. Only read when a project has `Feedback: on`.

### When it triggers

Claude reaches for this skill when you say things like:

- "What should we work on next?"
- "What's next on the improvement tracker?"
- "Any more ideas for this project?"
- Starting a work session on a project with nothing specific queued up.

### Example: first run on a new project

```
You: What should we work on next?

Claude: No IMPROVEMENT_TRACKER.md yet for this project -- let's set one up.
        Based on the codebase, I'd propose these idea categories: Features, Refactors.
        And this priority order: (1) fix broken/flaky behavior, (2) ship features users
        are waiting on, (3) pay down debt that's slowing things down. Does that order
        match what actually matters right now, or would anything swap?

You: Swap 1 and 2, we don't have anything broken right now.

Claude: [writes IMPROVEMENT_TRACKER.md with confirmed tiers, then tops up both
         categories with ideas grounded in the actual codebase, ranks them, and
         proposes the top candidate with reasoning tied to the tiers]
```

### Example: steady-state run

```
You: What's next?

Claude: Goals last reviewed 3 weeks ago, nothing suggests drift -- skipping that check.
        Top candidate: "Add retry logic to the sync job" -- serves tier 1 (nothing's
        broken, but this is the closest thing to a reliability gap) and touches one
        function. Want me to build it, or is something else more pressing?

You: Build it.

Claude: [implements, then moves the item to Done in the tracker with a one-line note
         on what actually shipped]
```

### Example: reprioritizing mid-project

```
You: Priorities have changed, we need to focus on performance now.

Claude: [jumps to the staleness-check step, updates the Goals tiers, bumps the
         review date -- no need to re-run full setup]
```

### Example: with optional strategies/feedback turned on

```
You: Show me more than just one option each time, and check back on whether
     past work actually delivered.

Claude: [sets Selection strategy: spread(3) + wildcard(rotate) and Feedback: on
         in the tracker]

...next run...

Claude: Tier 1 pick: "Fix pagination bug" -- because X.
        Tier 2 pick: "Add dark mode" -- because Y.
        Wildcard: "Rewrite the CSV export" -- oldest idea in the backlog, worth
        a second look.
        Also: last shipped "Add retry logic" (3 weeks ago) -- deliver as expected,
        mixed, or miss?
```

