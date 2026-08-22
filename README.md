# skills-development

A collection of custom skills for [Claude Code](https://claude.com/product/claude-code).

## Skills

- **[next-improvement](next-improvement/README.md)** — a repeatable "what should we work on
  next" loop that maintains a per-project priority tracker, brainstorms and ranks ideas against
  it, and proposes the next thing to build before ever planning or coding anything.
- **[plan-technical-jira-ticket](plan-technical-jira-ticket/README.md)** — turns a single,
  well-scoped technical Jira ticket into an implementation plan grounded in the actual
  codebase(s) it touches, verifying the ticket's claims against real code before proposing a
  plan for approval.
- **[repo-knowledge](repo-knowledge/README.md)** — captures repo gotchas, root-causes, and
  dependency/environment quirks into a per-project `KNOWLEDGE.md` at the moment they're
  discovered, applies a capture bar to keep it noise-free, and runs an occasional review to
  prune entries that have gone stale or never proved useful.
- **[operational-requirements-audit](operational-requirements-audit/README.md)** — audits a repo
  against Findmypast's Operational Requirements (bundled from Discourse, not re-derived from
  memory) and produces a per-requirement Met/Partial/Not Met/N/A/Unverifiable report backed by
  concrete evidence from the codebase.
- **[commit-message-check](commit-message-check/README.md)** — a mandatory pre-commit gate that
  re-reads the user's own conventions file (bootstrapped via interrogation on first use) and
  checks a draft message part by part (prefix, subject, body, footer, whole-message,
  miscellaneous) before it's ever shown or committed.
- **[jira-ticket-audit](jira-ticket-audit/README.md)** — audits a single Jira ticket for
  ambiguity, internal inconsistency, gaps, oversized scope, and missing links to sibling tickets
  in its epic, producing per-dimension findings backed by evidence quoted from the ticket.
- **[ste-writing](ste-writing/README.md)** — rewrites or reviews prose (docs, READMEs, PR text,
  error messages — never code) in ASD-STE100 Simplified Technical English to strip "AI slop",
  with a bundled lint script that scores the result. Vendored from woosal1337's "The cure for AI
  slop" episode; see its README for origin and local changes.

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

## Design philosophy

See [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md) for the principles applied consistently across
the skills in this repo, and [CONVENTIONS.md](CONVENTIONS.md) for the concrete cross-skill specs
they all implement identically — currently where each skill writes the files it maintains inside
a user's project. Both are authoring references: since installing a skill copies only its own
folder, neither file travels with it, so every spec is also restated inside each skill that
implements it.
