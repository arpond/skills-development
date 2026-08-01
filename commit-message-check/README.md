# commit-message-check

A mandatory pre-commit gate for any git commit message, in any repo. Rather than trusting a
remembered summary of the user's commit-message conventions, it re-reads their conventions file
every time and walks through a literal checklist — ticket-key prefix (if the user uses one),
subject mood/length, whether a body is even needed, a strip-test on every body bullet, and a scan
for AI-authorship references — before a message is ever shown to the user or passed to
`git commit`.

This exists because the failure it prevents kept recurring even though the rules were already
written down: a commit message gets drafted from whatever vocabulary is fresh in context (the
mechanism just implemented), and gets shown to the user without the check ever actually running.
Turning "remember to check" into an explicit, ordered procedure is the fix.

The conventions themselves are **not part of this skill** — they're the user's own preferences,
kept in a standalone conventions file this skill reads fresh every run and bootstraps (via a short
interrogation) the first time it doesn't find one. That's what makes the skill itself portable
across users rather than tied to one person's ruleset.

Files:
- `SKILL.md` — the whole flow (find/bootstrap conventions, ticket prefix, subject checks,
  body-or-not, strip-test, AI-reference scan, final gate). Single file — every step runs on every
  commit message, nothing here is one-time or opt-in.
- `setup.md` — the one-time bootstrap interrogation, read only when no conventions file exists
  yet. Offers to seed from an existing "Commit message conventions" section in the user's
  `CLAUDE.md` if one's already there, otherwise asks from scratch.

## Cost

Cheap — one file read (the conventions file) plus reasoning against a checklist. No external
tools or MCP calls. Setup (first run only) is a short back-and-forth with the user.

## Requires

- **A conventions file at `~/.claude/commit-message-conventions.md`** — hard dependency, read
  fresh every invocation rather than paraphrased from memory. If it's missing, the skill runs
  `setup.md`'s bootstrap interrogation to create it rather than improvising conventions from
  general commit-message knowledge.

## When it triggers

Claude reaches for this skill any time a commit message is about to be drafted, shown, or
executed:

- Right before running `git commit` or `git commit --amend`.
- When asked to "give me a commit message" or "write the commit" without committing yet.
- When the user pushes back on an already-shown message ("that's not right", "check this against
  conventions", "why did you skip x") — that pushback signals the checklist wasn't actually
  applied, not just a style nitpick, so the skill re-runs from the top rather than only patching
  the one complaint raised.

## Example

```
You: Create a commit.

Claude: [invokes commit-message-check — conventions file already exists]
        Re-read commit-message-conventions.md. This repo has SD-#### tickets in
        its history but none for this change, and it's a small, scoped fix, so
        the ticket key is SD-000.

        Drafted subject: "SD-000: Forward refs through Dialog's overlay and
        content components" — imperative, capitalized, no trailing period,
        under 72 chars, names the object of the verb.

        Considered a body — the why isn't fully obvious from the subject, so
        added one bullet and ran the strip-test: removing "console warning"
        and "ref"/"element" still leaves a complete rationale, so it stands.

        No AI-authorship references present.

        SD-000: Forward refs through Dialog's overlay and content components

        - Without it, consumers hit a console warning and any ref passed
          through it was silently dropped instead of reaching the element

        Want me to commit this?
```

On a brand new machine/user with no conventions file yet, the first invocation instead runs the
`setup.md` bootstrap — offering to seed from an existing `CLAUDE.md` conventions section if found,
otherwise asking a short set of questions (ticket prefix, subject style, body policy, co-author
trailer policy) — before checking any commit message.
