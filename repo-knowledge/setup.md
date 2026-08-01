# Setup: one-time bootstrap

Read this file only the first time `session-start.md`'s Step 0 finds no `KNOWLEDGE.md` for the
current project — never on later runs, once the file exists. It's kept out of `session-start.md`
so the every-run read stays focused on finding the file and checking staleness, not on a bootstrap
flow that only ever happens once per project.

## Gather everything before asking anything

Before proposing creation, check the project's existing documentation for content that belongs in
`KNOWLEDGE.md` instead — a read-only step, so do it before asking permission to create anything,
not after. These files are supposed to document the repo *as designed* (or, for a troubleshooting
guide, as curated reference), but in practice they often accumulate gotcha-shaped bullets anyway,
simply because there was nowhere else to put them before now. This isn't the redundancy test from
`SKILL.md` Step 2 — the content is already written down, that's the premise — it's a
classification question: does this bullet describe a deliberate convention/decision or curated
guidance (leave it), or an incidentally-discovered quirk/root-cause that ended up there for lack of
a better home (candidate to migrate)? See `SKILL.md`'s intro for the full CLAUDE.md/KNOWLEDGE.md
boundary this test is drawing on.

Check a curated, bounded set of conventional locations — not every markdown file in the repo,
which would make this slow and noisy over content that's mostly unrelated (changelogs, ADRs, API
docs, contributing guides):
- At the project root: `README.md`, `CLAUDE.md`/`AGENTS.md`, `TSG.md`/`TROUBLESHOOTING.md`,
  `RUNBOOK.md`.
- The same filenames one level inside a `docs/` or `documentation/` folder, if one exists — don't
  recurse further. A project with docs nested deeper than that needs the on-demand path (below)
  pointed at the specific file, since the automatic scan won't find it.

## Propose everything in one message

Fold all of the following into a single message rather than asking in stages — this is one of the
skill's hard rules (see the table in `SKILL.md`):
- Propose creating `KNOWLEDGE.md`, with a one-line explanation of what it's for (a place for repo
  gotchas/quirks/root-causes that cost real time to discover and aren't recorded anywhere else),
  and mention that it'll periodically prompt a "judgment-drift review" on its own — roughly every
  60-90 days, or sooner if entries have piled up — to prune stale entries (see
  `session-start.md`), so accepting the default means agreeing to that occasional check-in, not
  just to the file existing.
- If the project has a `CLAUDE.md`, propose adding a single pointer line to it (e.g. "See
  KNOWLEDGE.md for known repo gotchas and quirks") — keeps the two files DRY without duplicating
  content.
- If the scan above found candidates, list them as a single numbered list and propose migrating
  them (move, don't duplicate).
- Ask whether there's anywhere else worth checking for this kind of content — an internal wiki
  export, a team-specific notes file, anything the curated list above wouldn't anticipate. The
  curated list is a bet on common conventions, not a claim that it's exhaustive; rather than
  trying to keep growing it, ask once instead. This question is bootstrap-only — on later runs the
  on-demand path (below) covers it, since by then the user can just name a file directly instead
  of being asked in the abstract.

On confirmation: create `KNOWLEDGE.md` with an empty `## Entries` section and today's date as
`Last reviewed:` (no `## Declined` section yet — that's added the first time a proposal is
actually declined, see `SKILL.md` Step 2); add the CLAUDE.md pointer if confirmed; move (don't
duplicate) each confirmed migration candidate into `KNOWLEDGE.md` as a proper entry, filling in
Evidence from what's described and noting `Captured: <today> — migrated from <source file>` (the
original discovery date isn't recoverable, so don't guess one), removing it from the source file.

**Check it's actually tracked.** The skill's "no archive needed, git history covers it" design
(see `SKILL.md`) only holds if `KNOWLEDGE.md` is actually committed, not gitignored or left
untracked. Right after creating it, check (`git status` on the path) that it isn't ignored; if it
is, say so and suggest committing it — a one-time check here, not repeated on later runs.

If the user names another location in answer to the open-ended question, check it with the same
classification test and propose whatever turns up as its own follow-up confirmation — this is new
information arriving after the first answer, not a second ask of the same question.

## Available on demand later, too

The curated-file scan (not the open-ended question) is also available any time after bootstrap —
e.g. "check CLAUDE.md for things that should move to repo knowledge" — for projects that adopted
this skill before this check existed, or where one of these files picked up new gotcha-shaped
content since.
