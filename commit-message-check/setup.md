# Bootstrap setup (one-time per user)

Read this file only when `SKILL.md`'s Step 0 finds no `~/.claude/commit-message-conventions.md`
yet. This is a one-time interrogation — once the file exists, later runs never need this file
again (the user can always ask for it to be edited directly, which doesn't require re-running
this bootstrap).

**Create it before checking any commit message** — this is part of the skill, not a separate
setup step the user has to remember to do first.

**Every dimension SKILL.md checks against must be shown and confirmed here, including the ones
with a built-in default.** A default the user never saw isn't a confirmed preference, it's a
silent behavior — and a step that always applies with no visible way to change it stops being a
choice at all. Don't summarize this as "just use the defaults?" and move on; actually list each
default's concrete effect so the user is agreeing to something specific, not a vague gesture at
"standard practice."

1. **Check for an existing seed first.** Some users already have commit conventions written down
   somewhere general-purpose — a "Commit message conventions" section in their global `CLAUDE.md`,
   or similar. If one exists, offer to use it as the starting point rather than interrogating from
   scratch: show what was found, ask if it should be copied into the new conventions file as-is,
   edited, or ignored in favor of a fresh interrogation. Don't silently assume it's still accurate
   just because it's written down — confirm before writing it as the file's contents. Whatever is
   seeded still gets shown against the full dimension list below — a seed may predate one of these
   dimensions entirely (e.g. never mentioned the strip-test or the AI-scan list), and a gap in the
   seed isn't the same as a deliberate "no preference."

2. **Show the full set of dimensions in one message, defaults included, then ask.** Per this
   project's "one check-in, not two" — one combined message covering all of the below, not a
   volley of separate questions:

   - **Ticket-key prefix.** No built-in default (most users don't use one). Does this user's work
     involve ticket keys (Jira, Linear, GitHub issues) that should prefix commit subjects? If yes:
     what format, which repos it applies to (a detection rule the skill can check against, e.g.
     "repos with existing TICKET-#### history"), what to do when no ticket is known (a
     placeholder, and/or a rule for when to stop and ask instead of defaulting for non-trivial
     work). If no: record that explicitly.
   - **Subject line style.** Built-in default: imperative mood, no trailing period, well under 72
     characters, always names the object of the verb (`Fix broken retry loop`, not bare `Fix`).
     Show this concretely, ask if it fits or if anything should change.
   - **Body policy.** Built-in default: no body unless the subject genuinely can't carry the why.
     Show this, ask if it fits or if this user wants something else (e.g. always a rationale,
     never a body, a specific template).
   - **Body format / strip-test.** Built-in default when a body is written: always `-`-bulleted,
     never prose, and each bullet is run through a "strip-test" — delete every proper
     noun/function/class/library name from it and check what's left still reads as a complete
     rationale on its own, rewriting it if not. Show this mechanism concretely (a one-line
     example is enough), ask if it fits or if this user wants a different body format/discipline
     or none at all.
   - **AI-authorship scan.** Built-in default: always scan the finished message for `Claude`,
     `Anthropic`, `Generated with`, any AI-naming `Co-Authored-By`, or similar, and strip it.
     Show this list, ask if it should stay as-is, whether anything should be added/removed, or
     whether this user actually wants an AI-attribution trailer included by default (rare, but
     don't assume against it).
   - **Co-author trailer** (distinct from the AI-scan above — this is about a *human* co-author
     trailer policy, if this user ever pairs). Only ask if it seems relevant; skip silently
     otherwise rather than manufacturing a question nobody would ask.
   - **Anything else specific to this user's workflow** — revert message conventions, how
     iteration/WIP commits within one piece of work should read, repo-specific overrides. Don't
     manufacture questions nobody would think to ask; this is a catch-all for whatever the user
     volunteers, not a mandatory checklist item.

3. **Write the file** at `~/.claude/commit-message-conventions.md` with the confirmed value for
   *every* dimension above — including the ones where the answer was "yes, keep the default."
   Write out what the default concretely does, don't just write "(default)" as a placeholder that
   points back at this file — `SKILL.md` may change later, and the conventions file needs to stay
   a complete, accurate record of what this user actually agreed to at the time, not a pointer
   that can drift out from under them. Keep the format plain prose/bullets — this file is read by
   a model, not parsed by code, so there's no fixed schema to match. A reasonable shape:

   ```markdown
   # Commit message conventions

   ## Ticket-key prefix
   <rule, or "not used">

   ## Subject line
   <the confirmed rule, written out in full — not "default">

   ## Body
   <policy, written out in full>

   ## Body format / strip-test
   <confirmed format and whether the strip-test applies, written out in full>

   ## AI-authorship scan
   <confirmed term list and behavior, written out in full>

   ## Co-author trailer
   <policy, if applicable>

   ## Other
   <anything else volunteered>
   ```

4. Confirm the written file with the user before moving on to actually checking a commit message
   — this is a stored preference file the skill will keep trusting on every future run, so it's
   worth getting right the first time rather than silently guessing and correcting later.
