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
- **Unreachable isn't resolved, in either direction.** Sometimes a check can't be run at all — a
  linked ticket without read access, an unfetchable remote link, a search with zero results, a
  missing git remote. That's a third state, distinct from "confirmed true" and "confirmed false,"
  and collapsing it into either — treating it as absent, or treating it as an automatic blocker —
  is the mistake. Surface the specific thing that couldn't be checked and let the user decide,
  rather than guessing which direction is safer.
- **Documentation travels with the skill.** Installing a skill means copying its folder, so
  anything a person needs to evaluate or use it — what it does, when it triggers, example runs,
  prerequisites — belongs inside that folder as its own `README.md`, not in a repo-level file that
  doesn't get copied along. This is a different concern from progressive disclosure (which is
  about what Claude loads into context); this is about what a human still has once the skill is
  installed elsewhere. The top-level README stays a thin index pointing into each skill's own
  docs, rather than duplicating them.
- **Numbered choices, not just labels.** When presenting two or more options for the user to
  pick from, number them `1.`, `2.`, `3.`... in a single sequential list, regardless of what other
  labels each option carries (a tier name, "wildcard", a category). A descriptive label explains
  an option; it isn't a substitute for a number the user can just say back ("go with 2") to
  confirm unambiguously.
- **Independent knobs, not piggybacked defaults.** When a skill has multiple configurable
  quantities that interact — how many items a sub-mode generates vs. an overall cap on the total,
  say — keep each one separately named and settable rather than hardcoding one to silently ride on
  another's number or on an unstated constant. A user changing one shouldn't have to reason about
  which other knobs secretly moved with it.
- **State hard dependencies explicitly, distinguish them from what degrades gracefully.** If a
  skill can't function at all without something external (an MCP server, a specific tool), that
  belongs up front in its own docs — not just handled gracefully at runtime once someone's already
  hit it. Dependencies the skill already works around on its own (and notes the limitation for,
  per "unreachable isn't resolved") don't need the same billing; conflating the two either buries
  a real blocker behind a wall of caveats or overstates how fragile the skill actually is.

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
existing folder). Each skill's own `README.md` travels with it, so the usage docs and examples
stay available even once it's installed elsewhere.

## Skills

- **[next-improvement](next-improvement/README.md)** — a repeatable "what should we work on
  next" loop that maintains a per-project priority tracker, brainstorms and ranks ideas against
  it, and proposes the next thing to build before ever planning or coding anything.
- **[plan-technical-jira-ticket](plan-technical-jira-ticket/README.md)** — turns a single,
  well-scoped technical Jira ticket into an implementation plan grounded in the actual
  codebase(s) it touches, verifying the ticket's claims against real code before proposing a
  plan for approval.

