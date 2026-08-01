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

**The checklist is organized around the structural parts of a commit message, not around a fixed
list of named rules.** A commit message is made of a prefix (optional), a subject, a body
(optional), and a footer (optional) — plus rules that apply across the whole message rather than
to one part, and rules that don't cleanly attach to any single part. Each part gets exactly one
kind of step: *iterate every rule the conventions file lists for this part, check the draft
against each one individually.* That's the same mechanism reused six times, not six different
mechanisms — so a brand new rule (a spelling/language convention, a required footer link, a rule
that only makes sense when both subject and body are considered together) always has a home and
always gets the same enforced check, without SKILL.md itself needing to change to accommodate it.

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
  worked examples — those illustrate the mechanism, they aren't a default ruleset. Every "safe
  general default" referenced in Steps 2-6 below gets explicitly shown and confirmed during that
  interrogation, not silently assumed — see `setup.md`. A default a user never saw isn't really a
  default, it's undisclosed forced behavior.

The conventions file is organized under six headings, matching the parts below: `## Prefix`,
`## Subject`, `## Body`, `## Footer`, `## Whole-message`, `## Miscellaneous`. Any heading can be
empty or absent (e.g. most users have no `## Prefix` rules) — an empty/absent section means that
step below has nothing to check, not that the step gets skipped without looking.

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

If a body is written, check it against every rule listed under `## Body`, individually — same as
every other step, no special-cased technique hardcoded here. Built-in default (light, deliberately
— applies only to whatever isn't overridden):

- Format is `-`-bulleted, never a prose paragraph.
- Each bullet explains *why* the change happened, not what changed or how — the diff already shows
  the mechanism, so a bullet that just narrates the diff in prose isn't adding anything.

If `## Body` defines a specific technique for checking that (e.g. a strip-test — see `setup.md`
for what that looks like, and `README.md` for a worked example), apply exactly what's written
there, the same way Step 1 applies whatever prefix rule is written under `## Prefix`.

## Step 4 — Footer

Check for any rules under `## Footer` — trailers, required links, co-author lines, anything that
goes after the body. This has no built-in default content (most users have none), but it always
gets checked: if `## Footer` lists something (e.g. "append a link to the relevant ticket/PR"),
apply it; if it's empty, there's no footer to add.

Note the built-in AI-authorship scan (Step 5) also touches trailer-shaped text but is checked
separately, since it applies regardless of whether this user has any footer rules of their own.

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

Check every rule listed under `## Miscellaneous` — this is for rules that don't cleanly attach to
one structural part (e.g. how revert messages should read, how a sequence of iteration commits on
the same piece of work should relate to each other, a rule conditional on more than one part at
once). This section exists because not every rule fits Steps 1-5 cleanly, not as a place rules go
to avoid being checked — it gets the same individual, one-by-one check as every other section, not
a skim.

## Step 7 — Only now, show it or commit it

The message may only be shown to the user or passed to `git commit` once Steps 1-6 have all been
walked through for *this* draft — not carried over from an earlier draft in the same conversation.
If the user pushes back on something you show them, that means the checklist was skipped or
rushed: go back to Step 1 on the corrected version rather than only patching the specific
complaint they happened to notice. If the pushback reveals the conventions file itself is wrong
or out of date, that's a separate, explicit edit to the conventions file — confirm the change with
the user before writing it, same as any other update to their stored preferences.
