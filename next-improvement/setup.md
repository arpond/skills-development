# Bootstrap setup (one-time per project)

Read this file only when `session-start.md`'s Step 0 finds no `IMPROVEMENT_TRACKER.md` for the
current project. This is a one-time-per-project interrogation — once the file exists, later runs
never need this file again (see `session-start.md`'s Step 0.5 for ongoing staleness checks
instead).

Look for `IMPROVEMENT_TRACKER.md` at the root of whichever project the user is currently working
in (use judgement on project boundary: the nearest enclosing directory with its own README,
package manifest, or similar — not necessarily the git repo root, since one repo can contain
several projects with different concerns).

**Create it before doing anything else** — this is part of the skill, not a separate setup step
the user has to remember to do first:

1. Propose 2-4 idea categories based on what this project actually is (read its README/CLAUDE.md/
   directory structure to ground this, don't guess blind). If genuinely unsure, "Refactors" and
   "Features" are a safe universal default that can be renamed or split later.
2. Propose a tiered goal list, again grounded in what the project seems to be for. A reasonable
   generic starting point, if nothing more specific is obvious: (1) improve the actual
   user-facing output/quality of the thing this project produces, (2) automate/streamline the
   process of producing it, (3) keep the system maintainable and readable, (4) avoid building
   things that aren't necessary. Notice none of these tiers is phrased as "add new features" —
   that's deliberate, not an oversight to fix. The typical use case for this skill leans toward
   maintenance and improving what already exists rather than expanding scope, and new-feature
   work is also the area where users most want direct say over scope and direction rather than
   a generically-proposed tier speaking for them. If the project genuinely calls for a
   features-focused tier (e.g. it's early-stage and clearly still building out core
   functionality), it's fine to propose one — this is about not defaulting to it, not about
   treating feature work as invalid — but don't rank it above maintenance/quality tiers by
   default; let the user actively push it up during interrogation if that's really where their
   priority is. But don't just default to any of this without thinking — a project
   that's a library has different natural tiers than one that's an end-user tool.
3. **Interrogate this with the user before writing anything — don't just show a list and wait
   for a thumbs-up.** This is one of the skill's hard rules (see the table in `SKILL.md`). Walk
   through the proposed tiers and actively ask: does this order match
   what actually matters right now, is anything missing, is anything here not actually a
   priority, would any two tiers swap if a candidate pitted them against each other? Use
   AskUserQuestion for the ranking itself (e.g. "which matters more right now: A or B?") rather
   than a single open-ended "sound good?" — it's cheap now and wrong tiers quietly misrank
   every candidate for as long as the tracker lives. This is a one-time setup cost per project;
   getting it right once is worth a real back-and-forth rather than silently guessing. If a
   features-type tier ends up ranked at or above maintenance/quality tiers, confirm that's
   actually intended rather than letting it pass silently — it's the one case in this step
   worth double-checking given the default lean described above.
   If the user resists ranking two tiers against each other — "they're both important",
   "depends on the week" — that's a signal for a genuine tie, not a cue to keep pushing for a
   forced order. Confirm it's a real tie, then ask directly for the tie-break rule to store
   (e.g. "if these two ever conflict on a specific candidate, which should win by default, or
   would you rather I ask you each time?"), and write both goals at the same tier number with
   that rule inline (see `SKILL.md`'s tracker format).
4. Ask three more questions — see `strategies.md`, `feedback.md`, and `risk-register.md` for their
   exact wording — covering presentation strategy, outcome feedback, and the risk register. All
   three have a safe, zero-effort default (`top-tier` / `Feedback: on` / `Risk register: off`) if
   the user doesn't care, and none should turn into a back-and-forth interrogation like Step 3's
   tier ranking does. But "don't over-interrogate" is about not volleying follow-up questions — it
   does not mean skipping or compressing the actual menu of options. For presentation strategy
   specifically, `strategies.md`'s own Setup section requires showing the full option set (both
   base modes, all additive modifiers, one sentence each) plus a worked combination example, in
   that one message, before asking what they want — a bare "want a selection strategy, or keep the
   default?" does not satisfy this, since the user can't choose from options they were never shown.
   Feedback's and the risk register's questions each stay a single short yes/no, no menu needed.
5. Write the file with the confirmed tiers, `Selection strategy:`, `Feedback:`, `Risk register:`
   setting, and today's date as `Last reviewed:`, then proceed to Step 1 in `SKILL.md` (it will
   find the categories empty, which is an expected and normal case of "running low," not an
   error).
