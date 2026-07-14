# skills-development

A collection of custom skills for [Claude Code](https://claude.com/product/claude-code).

## Design philosophy

Principles applied consistently across the skills in this repo:

- **Propose, don't just do.** Every consequential write — a new idea added to a tracker, a
  choice of what to build, an implementation plan — gets shown to the user and confirmed before
  it happens. A recommendation is not a decision. Where a skill has more than one such gate, they
  should be explicitly numbered/cross-referenced so drift is easy to catch on review, not left
  implicit — and that cross-reference needs to mirror the skill's actual structure (one entry per
  step/section, e.g. a table keyed to step number) rather than free prose that bundles items under
  a loose phrase. Prose summaries let a gap hide behind vague bundling and drift silently as steps
  change; a structurally mirrored one makes a missing entry visible by inspection, and should carry
  an explicit note to update it in the same edit that changes what it's summarizing.
- **Progressive disclosure.** The always-loaded core file stays lean; anything one-time
  (a bootstrap/setup step) or opt-in (a feature most projects won't touch) lives in a companion
  file read only when its trigger condition is actually met. A file's size is a signal — if a
  section only matters rarely, it usually belongs somewhere that's only read rarely too.
- **Re-ground, don't cache.** Judgements (priorities, rejected ideas, plans) can go stale as a
  project changes. Rather than trusting a cached decision indefinitely, skills re-check it
  against current state — but the check itself should be cheap and only interrupt the user when
  there's real reason to think something's drifted, not on every run.
- **Reasons over blacklists.** When something gets declined, record *why*, not just *that* it
  was declined. A flat suppression list risks permanently hiding something that was only
  rejected for timing, not substance — the reason is what lets a future judgement call be made
  correctly.
- **Concrete over vague.** Prompts push for specific, defensible reasoning ("checked X, Y, Z,
  here's why") rather than accepting a shrug as an answer — both from the model's own outputs
  and in what it asks the user to confirm.
- **Ask when genuinely ambiguous, don't silently resolve.** Ties, close calls, and conflicting
  signals get surfaced explicitly rather than picked arbitrarily and presented as if there was
  only ever one obvious answer.
- **One check-in, not two.** When a skill needs several related confirmations before proceeding
  (e.g. scope and understanding), fold them into a single message rather than gating twice in a
  row. Back-to-back stops for adjacent information don't add safety — they train the user to skim
  past confirmations instead of actually reading them, which undermines "propose, don't just do"
  more than it reinforces it.
- **Inputs are claims, not truth.** "Re-ground, don't cache" covers a skill's own judgements going
  stale as a project changes over time; this is the same discipline applied to what comes in from
  outside the skill on a single pass — a ticket description, a config file, a local checkout. None
  of these are guaranteed accurate just because they were provided: verify them against a more
  authoritative source (the actual code, the actual remote, the actual current state) before
  building on them, and treat a mismatch as something to surface, not quietly reconcile.

## Installation

Claude Code loads skills from `~/.claude/skills/<name>/` (user-level, available in every
project) or `<project>/.claude/skills/<name>/` (project-level, that project only). To install
a skill from this repo:

1. Copy the skill's folder into one of those locations, e.g.:
   ```
   cp -r next-improvement ~/.claude/skills/next-improvement
   ```
2. That's it — no restart needed. Claude Code picks up skills from disk each time it looks for
   one to trigger.

To update an installed skill after pulling changes from this repo, repeat step 1 (overwrite the
existing folder).

## next-improvement

A repeatable "what should we work on next" loop for any project. Instead of re-deciding from
scratch every session what to build next, it maintains a per-project `IMPROVEMENT_TRACKER.md`:
a small set of idea categories, a tiered list of priorities, and a running history of what's
shipped (and what's been rejected, and why). Each time it runs, it proposes fresh ideas for any
category that's run thin, ranks whatever's outstanding against the project's own priority
tiers, and proposes the next thing to build — but never writes a new idea to the tracker, starts
planning, or starts building anything without the user confirming first.

Files:
- `next-improvement/SKILL.md` — the steady-state loop (ties, idea top-up, ranking, propose/
  confirm/plan/build/record). Always loaded when the skill triggers.
- `next-improvement/setup.md` — the one-time-per-project bootstrap interrogation. Only read the
  first time the skill runs for a project, before its tracker file exists.
- `next-improvement/strategies.md` — optional alternate ways of presenting candidates (spread
  across tiers, a wildcard slot, a quick-win lane, category rotation). Only read when a project
  actually configures a `Selection strategy:` beyond the default.
- `next-improvement/feedback.md` — an optional loop that asks how past ships actually landed
  (delivered / mixed / missed) and feeds that back into future judgement, capped so it never
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

### Example: steady-state run

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

### Example: reprioritising mid-project

```
You: Priorities have changed, we need to focus on performance now.

Claude: [jumps to the staleness-check step, updates the Goals tiers, bumps the
         review date — no need to re-run full setup]
```

### Example: with optional strategies/feedback turned on

```
You: Show me more than just one option each time, and check back on whether
     past work actually delivered.

Claude: [sets Selection strategy: spread(3) + wildcard(rotate) and Feedback: on
         in the tracker]

...next run...

Claude: Tier 1 pick: "Fix pagination bug" — because X.
        Tier 2 pick: "Add dark mode" — because Y.
        Wildcard: "Rewrite the CSV export" — oldest idea in the backlog, worth
        a second look.
        Also: last shipped "Add retry logic" (3 weeks ago) — deliver as expected,
        mixed, or miss?
```

## plan-technical-jira-ticket

Turns a single, well-scoped technical Jira ticket (tech debt, a refactor, a performance fix, a
config/infra change) into an implementation plan grounded in the actual codebase(s) it touches,
rather than just restating the ticket in different words. It fetches the ticket plus everything
that might carry context the ticket body doesn't — linked issues, remote links, attachments, a
parent epic — verifies the ticket's claims (and the local checkout's freshness) against real code
rather than trusting either at face value, and recaps its understanding once in a single check-in
before spending any effort exploring. Deliberately narrow in scope: it flags rather than plans
epics, bug reports, and multi-integration feature tickets, since each of those needs a different
process than "plan one well-defined technical change."

Files:
- `plan-technical-jira-ticket/SKILL.md` — the whole flow (resolve/classify, gather context,
  understand, recap, ground in code, write the plan, hand off). Single file — nothing here is
  one-time or opt-in the way `next-improvement`'s companion files are, so there's nothing to split
  out; every step runs on every ticket.

### When it triggers

Claude reaches for this skill when you give it a ticket number and ask it to plan, scope, break
down, or figure out the approach for that kind of technical work:

- "Plan out SD-4821, it's the tech debt ticket about the old retry logic."
- "What would it take to do PROJ-456?"
- Pasting a Jira URL and asking what the change actually involves.

### Example: straightforward run

```
You: Plan out SD-4821, it's a tech debt ticket about the old retry logic.

Claude: [fetches SD-4821, checks status/assignee (To Do, unassigned) and links
         (none blocking), confirms it's tech debt rather than a bug or feature,
         pulls a linked Confluence doc for design detail]
        Here's what I'm taking this ticket to mean: replace the manual retry loop
        in the sync job with the shared retry helper the rest of the codebase uses.
        Looks scoped to just this repo — right so far?

You: Yes, that's right.

Claude: [confirms the local checkout is current, checks for any branch already
         referencing SD-4821 (none), explores the sync job and how the shared
         retry helper is used elsewhere]
        Plan: replace the loop in sync_job.py with RetryHelper (same pattern as
        export_job.py), add a unit test for the backoff behaviour, verify against
        the existing integration tests. Covers both acceptance criteria on the
        ticket. Want me to go ahead?

You: Approved, go ahead.

Claude: [implements per the plan]
```

### Example: a scope gate firing

```
You: Can you plan JIRA-991?

Claude: [fetches JIRA-991] This reads as a bug report — it describes users seeing
        stale cached data, not a known change to make. Want a bug-investigation
        process instead, or is the root cause already known, in which case this
        is really just "invalidate the cache on write"?

You: Root cause is known, just implement the cache invalidation.

Claude: [proceeds with a plan scoped to that specific, already-diagnosed change]
```

