# commit-message-check

A mandatory pre-commit gate for any git commit message, in any repo. Instead of trust in a
remembered summary of the user's commit-message conventions, it re-reads their conventions file
every time and checks the draft part by part: prefix, subject, body, footer, whole-message (an
AI-authorship scan, a language or spelling convention), and a miscellaneous bucket for anything
that attaches to no single part. This happens before the user sees a message or `git commit`
receives it.

This exists because the failure it prevents kept recurring even though the rules were already
written down. A commit message gets drafted from whatever vocabulary is fresh in context (the
mechanism just implemented), and the user sees it without the check ever running. The fix is to
turn "remember to check" into an explicit, ordered procedure.

The conventions themselves are **not part of this skill**. They live in a standalone conventions
file. This skill reads that file fresh every run and bootstraps it, through a short interrogation,
the first time it finds none. That is what makes the skill portable across users rather than tied
to one person's ruleset. The conventions file has six headings, `Prefix`, `Subject`, `Body`,
`Footer`, `Whole-message`, `Miscellaneous`, which match the structural parts of a commit message.
So a new rule (a required footer link, a spelling convention, anything) always has an obvious home
and always gets checked, instead of a place in an unstructured pile that is only sometimes read.

There are two possible locations, and both can exist at once: **personal**
(`~/.claude/commit-message-conventions.md`, this user's own preferences, which apply across every
repo) and **repo-level** (`.claude/commit-message-conventions.md` at a repo's root, a team's
shared, committed convention). Where both define the same heading, repo-level wins. It is the
explicit shared standard, not one person's default. Where only one defines a heading, that one
applies. Where neither does, the skill's built-in default applies.

Files:
- `SKILL.md` — the whole flow: find or bootstrap the conventions file, then one step per
  structural part (prefix, subject, body, footer, whole-message, miscellaneous), each a check of
  every rule listed under its heading, then a final gate. A single file. Every step runs on every
  commit message. Nothing here is one-time or opt-in.
- `setup.md` — the one-time bootstrap interrogation, read only when no conventions file exists
  yet. It offers to seed from an existing "Commit message conventions" section in the user's
  `CLAUDE.md`, or from consistent patterns in example commits or repo history if offered. Then it
  asks through all six parts for anything not already covered.

## Cost

Cheap: one file read (the conventions file) plus reasoning against a checklist. No external tools
or MCP calls. Setup, on the first run only, is a short exchange with the user.

## What it writes

- **`.claude/commit-message-conventions.md`** — your conventions, written once at first use after
  an interrogation about how you like commit messages written. Two possible homes: at the **repo
  root** as a committed team standard, or at `~/.claude/` as a personal one that follows you
  across every repo. The skill asks which at bootstrap, reads both when both exist (repo wins per
  heading), and updates one only when you say a rule in it is wrong.

**Where it looks:** repo root `.claude/` first, then `~/.claude/`. Deliberately not the repo root
itself or a docs folder. This is config you rarely open, not documentation. It is per-repo rather
than per-project because a repo with several projects still has one commit history.

Beyond that it writes nothing into your project. It does affect your commits, which is the job,
but it never runs `git commit` on its own. It gates a message you were already about to make.

## Requires

- **A conventions file, personal (`~/.claude/commit-message-conventions.md`) and/or repo-level
  (`.claude/commit-message-conventions.md`)** — a hard dependency on at least one. The skill reads
  it fresh every invocation, never paraphrased from memory. If neither exists, the skill runs
  `setup.md`'s bootstrap interrogation to create one instead of improvised conventions from
  general commit-message knowledge.

## When it triggers

Claude reaches for this skill any time it is about to draft, show, or execute a commit message:

- Right before `git commit` or `git commit --amend`.
- When asked to "give me a commit message" or "write the commit" without a commit yet.
- When the user objects to an already-shown message ("that's not right", "check this against
  conventions", "why did you skip x"). That objection signals the checklist was not applied, not
  a style nitpick. So the skill re-runs from the top instead of a patch to the one complaint
  raised.

## Example

```
You: Create a commit.

Claude: [invokes commit-message-check — conventions file already exists, no
        Prefix rules for this repo]
        Re-read commit-message-conventions.md.

        Drafted subject: "Forward refs through Dialog's overlay and content
        components" — imperative, capitalized, no trailing period, under 72
        chars, names the object of the verb.

        Considered a body — the why isn't fully obvious from the subject, so
        added one bullet and ran the strip-test: removing "console warning"
        and "ref"/"element" still leaves a complete rationale, so it stands.

        No AI-authorship references present.

        Forward refs through Dialog's overlay and content components

        - Without it, consumers hit a console warning and any ref passed
          through it was silently dropped instead of reaching the element

        Want me to commit this?
```

**With a `Prefix` rule defined** (for example, this user's conventions file says findmypast-style
repos prefix with a Jira ticket key):

```
You: Create a commit.

Claude: [invokes commit-message-check — conventions file defines a Prefix rule,
        this repo matches its detection rule]
        This repo has TICKET-#### history but none for this change, and it's
        small/scoped, so the placeholder applies per the Prefix rule: TICKET-000.

        Drafted subject: "TICKET-000: Retry flaky upload requests" —
        imperative, capitalized after the prefix, no trailing period, under
        72 chars, names the object of the verb.

        No body needed — the subject carries the why on its own.

        No AI-authorship references present.

        TICKET-000: Retry flaky upload requests

        Want me to commit this?
```

**A messier draft, where the checklist catches things** instead of a pass-through of a clean
draft. The conventions file here has a `Footer` rule that requires a link back to the PR or
ticket, a `Whole-message` rule for British spelling, and opts into the strip-test (an optional,
stricter body technique offered at setup, not a `SKILL.md` built-in. See `setup.md`):

```
You: Write the commit for this.

Claude: [invokes commit-message-check]
        Step 2 (Subject): first draft was "Refactor" — bare, no object, fails
        the "names the object of the verb" rule even though this is a small
        change. Rewritten: "Refactor retry loop to back off on 429s".

        Step 3 (Body): the why isn't obvious from the subject alone (why back
        off specifically on 429s, not all errors), so a body is needed.
        Drafted bullet mentioned "RetryPolicy class" and "HttpClient" by name
        — failed the strip-test, rewritten as pure rationale.

        Step 4 (Footer): conventions file requires a PR link in the footer —
        added.

        Step 5 (Whole-message): conventions file specifies British spelling;
        draft had "behavior" — corrected to "behaviour". AI-authorship scan:
        clean.

        Refactor retry loop to back off on 429s

        - Retrying immediately on rate-limit responses was making the
          problem worse instead of recovering from it

        See: https://github.com/org/repo/pull/123

        Want me to commit this?
```

With neither file present yet, the first invocation runs the `setup.md` bootstrap before it checks
any commit message. The bootstrap offers to seed from an existing `CLAUDE.md` conventions section,
example commits or repo history, or a repo's own README or CONTRIBUTING doc if available. Each
seed is a hypothesis to confirm, not adopted in silence, because real history is often
inconsistent. It asks whether the result should be personal or repo-level. Then it asks through
all six parts for whatever is still uncovered, with defaults shown explicitly rather than assumed.

**Conflicting rules.** If two rules conflict, within one heading, across headings, or against a
built-in default, the skill stops and asks rather than a silent pick. See `SKILL.md`'s intro. The
skill writes the resolution back into the conventions file, so the same conflict needs no
re-litigation on the next commit.
