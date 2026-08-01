# Bootstrap setup (one-time per user)

Read this file only when `SKILL.md`'s Step 0 finds no `~/.claude/commit-message-conventions.md`
yet. This is a one-time interrogation — once the file exists, later runs never need this file
again (the user can always ask for it to be edited directly, which doesn't require re-running
this bootstrap).

**Create it before checking any commit message** — this is part of the skill, not a separate
setup step the user has to remember to do first.

The conventions file is organized around the structural parts of a commit message — `## Prefix`,
`## Subject`, `## Body`, `## Footer`, `## Whole-message`, `## Miscellaneous` — matching
`SKILL.md`'s Steps 1-6. **Every rule SKILL.md checks against must end up written under one of
these six headings, including the ones with a built-in default.** A default the user never saw
isn't a confirmed preference, it's a silent behavior — and a step that always applies with no
visible way to change it stops being a choice at all. Don't summarize this as "just use the
defaults?" and move on; actually list each default's concrete effect so the user is agreeing to
something specific, not a vague gesture at "standard practice."

1. **Check for an existing seed first.** Some users already have commit conventions written down
   somewhere general-purpose — a "Commit message conventions" section in their global `CLAUDE.md`,
   or similar. If one exists, offer to use it as the starting point rather than interrogating from
   scratch: show what was found, ask if it should be copied in as-is, edited, or ignored in favor
   of a fresh interrogation. Don't silently assume it's still accurate just because it's written
   down — confirm before writing it as the file's contents. Whatever is seeded still gets sorted
   into the six headings and checked against the full list below — a seed predating this skill's
   part-based structure won't already be organized that way, and won't already cover parts (like
   Footer) it never had reason to mention.

2. **Show the full set of parts in one message, defaults included, then ask.** Per this project's
   "one check-in, not two" — one combined message covering all of the below, not a volley of
   separate questions:

   - **Prefix.** No built-in default (most users don't use one). Does this user's work involve
     ticket keys (Jira, Linear, GitHub issues) that should prefix commit subjects? If yes: what
     format, which repos it applies to (a detection rule the skill can check against, e.g. "repos
     with existing TICKET-#### history"), what to do when no ticket is known (a placeholder,
     and/or a rule for when to stop and ask instead of defaulting for non-trivial work). If no:
     record that explicitly.
   - **Subject.** Built-in default: imperative mood, no trailing period, well under 72 characters,
     always names the object of the verb (`Fix broken retry loop`, not bare `Fix`). Show this
     concretely, ask if it fits or if anything should change or be added (e.g. a language/spelling
     convention belongs under Whole-message instead, not here — see below).
   - **Body.** Built-in default: no body unless the subject genuinely can't carry the why; when
     present, always `-`-bulleted and each bullet passes the strip-test (delete every proper
     noun/function/class/library name from it, check what's left still reads as a complete
     rationale on its own, rewrite if not). Show this concretely (a one-line example is enough),
     ask if it fits or if this user wants something else — always a body, never a body, a specific
     template, a different body format entirely.
   - **Footer.** No built-in default. Does this user want anything appended after the body —
     a required link (ticket, PR, doc), a co-author trailer policy, anything else that goes at the
     end? If no: record that explicitly rather than leaving it blank and ambiguous.
   - **Whole-message.** Built-in default: always scan the finished message for `Claude`,
     `Anthropic`, `Generated with`, any AI-naming `Co-Authored-By`, `Claude-Session`, or similar,
     and strip it. Show this list, ask if it should stay as-is, whether anything should be
     added/removed, or whether this user actually wants an AI-attribution trailer included by
     default (rare, but don't assume against it). Also ask here about anything that applies
     uniformly across the whole message rather than to one part — a language/spelling variant
     (e.g. British vs. American English), a tone rule, capitalization conventions that apply
     beyond just the subject.
   - **Miscellaneous.** No built-in default. Anything specific to this user's workflow that
     doesn't cleanly belong to one part above — revert message conventions, how iteration/WIP
     commits within one piece of work should relate to each other, repo-specific overrides, a rule
     that only makes sense considering more than one part at once. Don't manufacture questions
     nobody would think to ask; this is a genuine catch-all for whatever the user volunteers, not
     a mandatory checklist item — but whatever does go here still gets checked every run (see
     `SKILL.md` Step 6), it is not a lower-priority bucket.

3. **Write the file** at `~/.claude/commit-message-conventions.md` under the six headings, with
   the confirmed value for *every* part above — including the ones where the answer was "yes,
   keep the default." Write out what the default concretely does, don't just write "(default)" as
   a placeholder that points back at `SKILL.md` — that file may change later, and the conventions
   file needs to stay a complete, accurate record of what this user actually agreed to at the
   time, not a pointer that can drift out from under them. Keep the format plain prose/bullets —
   this file is read by a model, not parsed by code, so there's no fixed schema beyond the six
   headings themselves. Shape:

   ```markdown
   # Commit message conventions

   ## Prefix
   <rule, or "not used">

   ## Subject
   <the confirmed rules, written out in full — not "default">

   ## Body
   <the confirmed policy and format, written out in full>

   ## Footer
   <rules, or "none">

   ## Whole-message
   <AI-scan behavior plus any language/tone rules, written out in full>

   ## Miscellaneous
   <anything else volunteered, or omit the heading entirely if nothing was volunteered>
   ```

4. Confirm the written file with the user before moving on to actually checking a commit message
   — this is a stored preference file the skill will keep trusting on every future run, so it's
   worth getting right the first time rather than silently guessing and correcting later.
