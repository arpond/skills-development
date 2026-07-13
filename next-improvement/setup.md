# Bootstrap setup (one-time per project)

Read this file only when `SKILL.md` Step 0 finds no `IMPROVEMENT_TRACKER.md` for the current
project. This is a one-time-per-project interrogation -- once the file exists, later runs never
need this file again (see `SKILL.md` Step 0.5 for ongoing staleness checks instead).

Look for `IMPROVEMENT_TRACKER.md` at the root of whichever project the user is currently working
in (use judgment on project boundary: the nearest enclosing directory with its own README,
package manifest, or similar -- not necessarily the git repo root, since one repo can contain
several projects with different concerns).

**Create it before doing anything else** -- this is part of the skill, not a separate setup step
the user has to remember to do first:

1. Propose 2-4 idea categories based on what this project actually is (read its README/CLAUDE.md/
   directory structure to ground this, don't guess blind). If genuinely unsure, "Features" and
   "Refactors" are a safe universal default that can be renamed or split later.
2. Propose a tiered goal list, again grounded in what the project seems to be for. A reasonable
   generic starting point, if nothing more specific is obvious: (1) improve the actual
   user-facing output/quality of the thing this project produces, (2) automate/streamline the
   process of producing it, (3) keep the system maintainable and readable, (4) avoid building
   things that aren't necessary. But don't just default to this without thinking -- a project
   that's a library has different natural tiers than one that's an end-user tool.
3. **Interrogate this with the user before writing anything -- don't just show a list and wait
   for a thumbs-up.** Walk through the proposed tiers and actively ask: does this order match
   what actually matters right now, is anything missing, is anything here not actually a
   priority, would any two tiers swap if a candidate pitted them against each other? Use
   AskUserQuestion for the ranking itself (e.g. "which matters more right now: A or B?") rather
   than a single open-ended "sound good?" -- it's cheap now and wrong tiers quietly misrank
   every candidate for as long as the tracker lives. This is a one-time setup cost per project;
   getting it right once is worth a real back-and-forth rather than silently guessing.
   If the user resists ranking two tiers against each other -- "they're both important",
   "depends on the week" -- that's a signal for a genuine tie, not a cue to keep pushing for a
   forced order. Confirm it's a real tie, then ask directly for the tie-break rule to store
   (e.g. "if these two ever conflict on a specific candidate, which should win by default, or
   would you rather I ask you each time?"), and write both goals at the same tier number with
   that rule inline (see `SKILL.md`'s tracker format).
4. Ask two more short questions -- see `strategies.md` and `feedback.md` for their exact wording
   -- covering presentation strategy and outcome feedback. Both are one-line opt-ins with a safe,
   zero-effort default (`top-tier` / `Feedback: on`) if the user doesn't care; don't turn either
   into its own long interrogation.
5. Write the file with the confirmed tiers, `Selection strategy:`, `Feedback:` setting, and
   today's date as `Last reviewed:`, then proceed to Step 1 in `SKILL.md` (it will find the
   categories empty, which is an expected and normal case of "running low," not an error).
