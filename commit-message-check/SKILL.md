---
name: commit-message-check
description: Mandatory pre-commit gate for any git commit message drafted on this user's behalf, in any repo. Loads the user's own conventions from a per-user conventions file (bootstrapped on first use if it doesn't exist yet), organized by the structural parts of a commit message — prefix, subject, body, footer, whole-message, and miscellaneous — and checks the draft against every rule listed under each part before the message is ever shown to the user or passed to `git commit`. Invoke this every time a commit message is about to be drafted, presented, or executed: before running `git commit` or `git commit --amend`, when asked to "give me a commit message" or "write the commit", or right before typing one out in a Bash/PowerShell call. Also invoke it if the user pushes back on a message you've shown them ("that's not right", "check this against conventions", "why did you skip x") — that pushback is a signal the checklist wasn't actually applied, not just a style nitpick. Do not skip this because the change "looks simple" or the draft "already looks like intent" — that exact self-assessment is what this skill exists to catch instead of relying on memory alone.
---

# Commit message check

This is a checklist skill, not an advisory one: the point is to make re-deriving and rechecking a
commit message mechanical, so it doesn't depend on remembering the rules correctly under time
pressure mid-task. The failure this skill exists to prevent isn't "not knowing the rules" — it's
drafting a message from whatever's fresh in context (the technical vocabulary of the change just
made) and presenting it without ever running the check. Actually walk through the steps below, in
order, every time.

The rules themselves are **not baked into this skill** — they're the user's own conventions,
kept in a conventions file this skill reads fresh every run and bootstraps on first use if it
doesn't exist yet. That split is deliberate: this skill is the mechanical checklist, portable
across users; the conventions file is one person's preferences, specific to them.

**The checklist is organized around the structural parts of a commit message — Prefix, Subject,
Body, Footer, Whole-message, Miscellaneous — matching the conventions file's six headings, not
around a fixed list of named rules.** Every step below does exactly the same thing: *iterate every
rule the conventions file lists under that heading, check the draft against each one
individually.* Same mechanism, six times, not six bespoke ones — so a brand new rule always has a
home and always gets checked, without SKILL.md needing to change to accommodate it. This is stated
once, here; the steps below don't repeat it.

One companion file:

- `setup.md` — the one-time bootstrap interrogation. Read it when Step 0 finds no conventions
  file yet.

## Step 0 — Find or bootstrap the conventions file

Look for a conventions file at `~/.claude/commit-message-conventions.md` (the user's home
directory on whichever machine this is running on — never a path copied from a different
machine or account).

- **Exists** → read it fresh, in full, every run. Don't work from a paraphrased memory of it —
  the user can edit it any time, and a stale mental copy defeats the point of keeping it external.
- **Doesn't exist** → read `setup.md` and run the bootstrap interrogation before continuing.
  Don't improvise conventions from general commit-message knowledge or from this skill's own
  worked examples — those illustrate the mechanism, they aren't a default ruleset. `setup.md`
  covers why every built-in default below gets shown and confirmed there rather than assumed.

Any of the six headings can be empty or absent (e.g. most users have no `## Prefix` rules) — that
means the matching step has nothing to check, not that the step gets skipped without looking.

## Step 1 — Prefix

Not every user or repo uses a ticket-key or other prefix — this step is conditional on whether
`## Prefix` has any rules, not a universal requirement.

If it does, it should specify: which repos it applies to (a detection rule, e.g. "repos with
existing TICKET-#### style history"), the format, and what to do when no ticket key is known (a
placeholder value, and/or a threshold for when to stop and ask instead of defaulting). Apply
exactly that rule, checking each listed condition individually:

- Repo matches the convention's detection rule → prefix required, following its format/placeholder
  rules.
- Repo doesn't match → no prefix.
- **Genuinely can't tell** (too few commits to judge, mixed/inconclusive history) — this is a
  third state, not a coin flip. Don't silently default to "no prefix" just because nothing
  confirmed "yes" — say what you checked and ask the user directly which convention applies.

If `## Prefix` is empty, skip straight to Step 2.

## Step 2 — Subject

Check the drafted subject against every rule listed under `## Subject`, individually — don't
eyeball the whole line at once and call it good. If that section is silent on a point, these are
the skill's built-in defaults (shown and confirmed at setup, not assumed here):

- Imperative, present tense (`Add`, `Fix`, `Remove` — not `Added`, `Fixed`, `Adding`).
- No trailing period.
- One line, well under 72 characters.
- Names the object of the verb. A bare `Fix`, `Refactor`, or `WIP` fails this even on an
  iteration commit inside a bigger ticket — these get read individually later (bisect, blame,
  cherry-pick), not just squash-merged away.

If anything here fails, rewrite the subject before touching the body — a body can't rescue a bad
subject.

## Step 3 — Body

First: does this commit even need a body? Check `## Body` for a stated policy; the built-in
default is *no, unless the why genuinely isn't recoverable from the subject alone*.

If a body is written, check it against every rule listed under `## Body`, individually. Built-in
default (deliberately light — no format imposed, applies only to whatever isn't overridden):

- Explain *why* the change happened, not what changed or how — the diff already shows the
  mechanism, so text that just narrates the diff isn't adding anything.
- No mandated structure (bulleted vs. prose vs. something else) — that's a formatting choice, not
  a universal git convention, so it's asked at setup rather than assumed here.

If `## Body` defines a specific technique for checking that (e.g. a strip-test — see `setup.md`
and `README.md`), apply exactly what's written there.

## Step 4 — Footer

Check for any rules under `## Footer` — trailers, required links, co-author lines, anything that
goes after the body. No built-in default content (most users have none): if `## Footer` lists
something (e.g. "append a link to the relevant ticket/PR"), apply it; if it's empty, there's no
footer to add.

## Step 5 — Whole-message

Check the fully composed message (prefix + subject + body + footer together) against every rule
listed under `## Whole-message` — rules that apply uniformly across the entire text rather than to
one part (e.g. a language/spelling convention, a tone rule). One built-in default always applies
here regardless of what the conventions file says, unless it explicitly opts out for a specific
commit:

- Scan for `Claude`, `Anthropic`, `Generated with`, any `Co-Authored-By` naming an AI,
  `Claude-Session`, or any other harness-injected AI-authorship trailer. Strip it immediately —
  this applies even when a tool/template tries to add it automatically, every time, without being
  asked, unless this specific commit was explicitly asked to include one.

## Step 6 — Miscellaneous

Check every rule listed under `## Miscellaneous` — rules that don't cleanly attach to one
structural part (e.g. how revert messages should read, how iteration commits within one piece of
work should relate to each other, a rule conditional on more than one part at once).

## Step 7 — Only now, show it or commit it

The message may only be shown to the user or passed to `git commit` once Steps 1-6 have all been
walked through for *this* draft — not carried over from an earlier draft in the same conversation.
If the user pushes back on something you show them, that means the checklist was skipped or
rushed: go back to Step 1 on the corrected version rather than only patching the specific
complaint they happened to notice. If the pushback reveals the conventions file itself is wrong
or out of date, that's a separate, explicit edit to the conventions file — confirm the change with
the user before writing it, same as any other update to their stored preferences.
