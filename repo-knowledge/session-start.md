# Session start: find/bootstrap the knowledge file

Read this file every time the skill triggers, right after `SKILL.md`'s intro — this is Step 0 of
the loop. Unlike `review.md`, this one isn't optional or occasional: every run needs to know
whether `KNOWLEDGE.md` exists and is well-formed before Step 1 can reference anything against it.
It lives in its own file purely to keep `SKILL.md` focused on the steady-state
reference/capture/removal loop — the split is about what's loaded into the common-case read, not
about this content being rare.

Once this file's step is done, continue to Step 1 in `SKILL.md`.

## Step 0: Find or bootstrap `KNOWLEDGE.md`

Look for `KNOWLEDGE.md` at the root of whichever project the user is currently working in (use
judgement on project boundary: the nearest enclosing directory with its own README, package
manifest, or similar — not necessarily the git repo root, since one repo can contain several
projects with different concerns).

**If it doesn't exist yet, don't create it silently.** This is a new git-tracked file the whole
team will see, not a private note — propose creating it, with a one-line explanation of what it's
for (a place for repo gotchas/quirks/root-causes that cost real time to discover and aren't
recorded anywhere else), and wait for confirmation. This is one of the skill's hard rules (see the
table in `SKILL.md`). If confirmed, create it with an empty `## Entries` section and today's date
as `Last reviewed:` — no `## Declined` section yet; that gets added the first time a proposal is
actually declined (see `SKILL.md` Step 2), not pre-created empty.

If the project has a `CLAUDE.md`, also propose adding a single pointer line to it (e.g. "See
`KNOWLEDGE.md` for known repo gotchas and quirks") at the same time — this keeps the two files DRY
without duplicating content, and only needs proposing once at bootstrap, not re-checked on every
later run.

**Also check for content in the project's existing documentation that belongs in `KNOWLEDGE.md`
instead.** These files are supposed to document the repo *as designed* (or, for a troubleshooting
guide, as a curated reference), but in practice they often accumulate gotcha-shaped bullets anyway,
simply because there was nowhere else to put them before now. This isn't the redundancy test from
Step 2 — the content is already written down, that's the premise — it's a classification question:
does this bullet describe a deliberate convention/decision, or curated general guidance (leave it),
or an incidentally-discovered quirk/root-cause that only ended up there for lack of a better home
(candidate to migrate)?

Check a curated, bounded set of conventional locations — not every markdown file in the repo,
which would make bootstrap slow and noisy over content that's mostly unrelated (changelogs, ADRs,
API docs, contributing guides):
- At the project root: `README.md`, `CLAUDE.md`/`AGENTS.md`, `TSG.md`/`TROUBLESHOOTING.md`,
  `RUNBOOK.md`.
- The same filenames one level inside a `docs/` or `documentation/` folder at the project root, if
  one exists — but don't recurse further into subfolders there. If a project's docs are nested
  deeper than that, use the on-demand trigger below pointed at the specific file instead of
  expecting the automatic pass to find it.

Propose migration candidates as a single numbered list and wait for confirmation before moving
anything — this is one of the skill's hard rules (see the table in `SKILL.md`). On confirmation,
move (don't duplicate) each one into `KNOWLEDGE.md` as a proper entry, filling in Evidence from
what's described and noting `Captured: <today> — migrated from <source file>` (the original
discovery date isn't recoverable, so don't guess one), and remove it from the source file.

**The curated list is a bet on common conventions, not a claim that it's exhaustive.** A project
could keep this kind of content somewhere the list doesn't anticipate — an internal wiki export, a
team-specific notes file, anything not named like one of the conventional locations above. Rather
than trying to keep growing the list to cover every possibility, ask once, the first time
`KNOWLEDGE.md` is created: "anywhere else worth checking for this kind of thing?" — folded into the
same message as the migration-candidate proposal above, whether or not that scan found anything, so
it's one check-in, not two. This is one of the skill's hard rules (see the table in `SKILL.md`):
don't silently assume the curated list was enough. If the user names something, check it with the
same classification test and propose whatever turns up as its own follow-up confirmation (this is
new information arriving after the first answer, not a second ask of the same question). If they
say there's nothing else, proceed — this question doesn't get asked again on later runs.

This whole check (curated scan plus the "anywhere else?" question) runs automatically the first
time `KNOWLEDGE.md` is created. The curated-file part of it is also available on request at any
later point (e.g. "check CLAUDE.md for things that should move to repo knowledge") for projects
that adopted this skill before this check existed, or where one of these files picked up new
gotcha-shaped content since — but the open-ended question is bootstrap-only, since by then the
user can always just name a file directly instead of being asked in the abstract. Neither part is
re-run automatically every session — same reasoning as Step 0.5's staleness check being
event/request-triggered rather than a standing sweep.

**If it exists, read it as-is and continue** — don't re-ask whether to create it. Judgment-drift
review timing is handled separately below, not here.

**If it exists but is malformed** (no `## Entries` section, an entry missing one of the required
fields, an unparseable `Last reviewed:` date) — this is a case of "unreachable isn't resolved," not
a normal empty file: don't silently reshape it back into form (that guesses at intent the user
never confirmed) and don't refuse to proceed either. Name the specific thing that doesn't parse
and ask directly: fix it by hand, or walk through repairing just that piece, leaving everything
else untouched. Never fabricate plausible-looking Evidence or dates to paper over a broken entry —
a wrong guess here is exactly the kind of silent-drift failure the mechanical staleness check in
`SKILL.md` Step 1 exists to catch, not create. This is one of the skill's hard rules (see the
table in `SKILL.md`).

**If it exists but clearly isn't ours** — reads as unrelated documentation with no `## Entries`
section and no resemblance to this schema at all, rather than a broken/partial version of it —
that's a naming collision, not a malformed file: don't touch it, and don't try to bolt entries onto
someone else's document. Say so and ask where this skill's file should live instead (a different
filename is the obvious fix; note the actual name chosen wherever this skill would otherwise
assume `KNOWLEDGE.md`).

## Checking whether a judgment-drift review is due

Check the `Last reviewed:` date at the top of `KNOWLEDGE.md`:

- **Missing** (file predates this field, or was created by hand): treat as due.
- **Older than ~60-90 days, or entry count has grown noticeably since the last review**: a
  judgment-drift review is due — read `review.md` and follow it before Step 1, folding the
  check-in into a single message rather than interrupting twice.
- **Recently reviewed and nothing suggests drift**: skip straight to Step 1 in `SKILL.md`.

This is separate from Step 1's mechanical staleness check (which runs per-entry, only when an
entry is actually about to be relied on) — this is the occasional, calendar/volume-based trigger
for the judgment call that only a human can make: is a fact still true *and* still the most useful
way to record it. The user can also trigger `review.md` at any time outside a normal run, e.g. by
asking to "review repo knowledge."
