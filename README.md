# skills-development

A collection of custom skills for [Claude Code](https://claude.com/product/claude-code).

## Skills

- **[next-improvement](next-improvement/README.md)** — a repeatable "what should we work on
  next" loop. It maintains a per-project priority tracker, brainstorms and ranks ideas against
  it, and proposes the next thing to build before it plans or codes anything.
- **[plan-technical-jira-ticket](plan-technical-jira-ticket/README.md)** — turns one
  well-scoped technical Jira ticket into an implementation plan grounded in the codebase(s) it
  touches. It checks the ticket's claims against real code before it proposes a plan for
  approval.
- **[repo-knowledge](repo-knowledge/README.md)** — captures repo gotchas, root causes, and
  dependency or environment quirks into a per-project `KNOWLEDGE.md` at the moment of
  discovery. A capture bar keeps the file free of noise. An occasional review prunes entries
  that went stale or never proved useful.
- **[operational-requirements-audit](operational-requirements-audit/README.md)** — audits a repo
  against Findmypast's Operational Requirements, bundled from Discourse and not re-derived from
  memory. It produces a per-requirement Met/Partial/Not Met/N/A/Unverifiable report backed by
  concrete evidence from the codebase.
- **[commit-message-check](commit-message-check/README.md)** — a mandatory pre-commit gate. It
  re-reads the user's own conventions file, bootstrapped by interrogation on first use, and
  checks a draft message part by part (prefix, subject, body, footer, whole-message,
  miscellaneous) before it shows or commits the message.
- **[jira-ticket-audit](jira-ticket-audit/README.md)** — audits one Jira ticket for ambiguity,
  internal inconsistency, gaps, oversized scope, and missing links to sibling tickets in its
  epic. It produces per-dimension findings backed by evidence quoted from the ticket.
- **[work-streams](work-streams/README.md)** — parks and resumes named streams of work in a
  personal store outside any repo. Wrap-up records the state, sweeps repo files the stream keeps
  current, and can write a continuation prompt. Resume loads it all back and checks it against
  the repo's current state.
- **[ste-writing](ste-writing/README.md)** — rewrites or reviews prose (docs, READMEs, PR text,
  error messages, never code) in ASD-STE100 Simplified Technical English to remove "AI slop". A
  bundled lint script scores the result. Vendored from woosal1337's "The cure for AI slop"
  episode. Its README gives the origin and the local changes.

## Installation

Claude Code loads skills from `~/.claude/skills/<name>/` (user-level, available in every
project) or `<project>/.claude/skills/<name>/` (project-level, that project only). To install
a skill from this repo:

1. Copy the skill's folder into one of those locations, e.g.:
   ```
   cp -r next-improvement ~/.claude/skills/next-improvement
   ```
2. That is all. No restart needed. Claude Code reads skills from disk each time it looks for one
   to trigger.

To update an installed skill after you pull changes from this repo, repeat step 1 and overwrite
the existing folder. Each skill's own `README.md` travels with it, so the usage docs and examples
stay available after it is installed elsewhere.

## Design philosophy

See [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md) for the principles applied across the skills in
this repo, and [CONVENTIONS.md](CONVENTIONS.md) for the concrete cross-skill specs they all
implement identically: counters, numbered choices, vocabulary, the hard-rules table, artifact
locations, skill versioning, and README contents. Both are authoring references. Installing a
skill copies only its own folder, so neither file travels with it, and each skill restates the
specs it implements inside its own folder.

## Changelog

[CHANGELOG.md](CHANGELOG.md) records the changes worth a reader's attention, newest first: what
a skill now does differently for its user, what an author here has to follow, how the repo is
organised. It is curated, not a commit log.
