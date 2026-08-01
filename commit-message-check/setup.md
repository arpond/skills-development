# Bootstrap setup (one-time per user)

Read this file only when `SKILL.md`'s Step 0 finds no `~/.claude/commit-message-conventions.md`
yet. This is a one-time interrogation — once the file exists, later runs never need this file
again (the user can always ask for it to be edited directly, which doesn't require re-running
this bootstrap).

**Create it before checking any commit message** — this is part of the skill, not a separate
setup step the user has to remember to do first.

1. **Check for an existing seed first.** Some users already have commit conventions written down
   somewhere general-purpose — a "Commit message conventions" section in their global `CLAUDE.md`,
   or similar. If one exists, offer to use it as the starting point rather than interrogating from
   scratch: show what was found, ask if it should be copied into the new conventions file as-is,
   edited, or ignored in favor of a fresh interrogation. Don't silently assume it's still accurate
   just because it's written down — confirm before writing it as the file's contents.

2. **Otherwise, interrogate from scratch.** Walk through each dimension below. Keep this
   conversational, not a wall of questions at once — group related ones, and skip ahead on
   anything the user answers before being asked (e.g. if they say up front "no ticket prefixes,
   Conventional Commits style," that answers several questions in one go).

   - **Ticket-key prefix.** Does this user's work involve ticket keys (Jira, Linear, GitHub
     issues) that should prefix commit subjects? If yes: what format, which repos does it apply
     to (a detection rule the skill can check against, e.g. "repos with existing TICKET-####
     history"), what to do when no ticket is known (a placeholder, and/or a rule for when to stop
     and ask instead of defaulting for non-trivial work). If no: record that explicitly rather
     than leaving the section blank and ambiguous.
   - **Subject line style.** Imperative mood is close to universal — confirm rather than assume.
     Any capitalization rule, length limit, or other house style beyond the general defaults
     already baked into `SKILL.md` (imperative, no trailing period, well under 72 chars, always
     name the object of the verb)? Only record deviations or additions here — no need to restate
     the defaults if the user's happy with them.
   - **Body policy.** Default-terse ("only when the subject can't carry the why") is a safe
     universal default — confirm it fits, or record what this user prefers instead (e.g. always
     bulleted rationale, a specific template, never a body at all).
   - **Co-author / AI-attribution trailers.** Confirm whether this user wants
     `Co-Authored-By: Claude` (or similar) included by default, only when explicitly asked, or
     never. Most users won't want it by default — but don't assume, ask.
   - **Anything else specific to this user's workflow** — revert message conventions, how
     iteration/WIP commits within one piece of work should read, repo-specific overrides. Don't
     manufacture questions nobody would think to ask; this is a catch-all for whatever the user
     volunteers, not a mandatory checklist item.

3. **Write the file** at `~/.claude/commit-message-conventions.md` with whatever was confirmed.
   Keep the format plain prose/bullets — this file is read by a model, not parsed by code, so
   there's no fixed schema to match. A reasonable shape:

   ```markdown
   # Commit message conventions

   ## Ticket-key prefix
   <rule, or "not used">

   ## Subject line
   <deviations from the general defaults, or "no deviations">

   ## Body
   <policy>

   ## Co-author trailer
   <policy>

   ## Other
   <anything else volunteered>
   ```

4. Confirm the written file with the user before moving on to actually checking a commit message
   — this is a stored preference file the skill will keep trusting on every future run, so it's
   worth getting right the first time rather than silently guessing and correcting later.
