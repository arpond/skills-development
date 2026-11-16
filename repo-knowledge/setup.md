# Setup: one-time bootstrap

Read this file the first time `session-start.md`'s Step 0 finds no `KNOWLEDGE.md` for the current
project. A later run reads it for a hand-off from `changelog.md`'s 1.1.0 entry. It also reads it
when the user asks for the on-demand doc scan or for the header. It's kept out of `session-start.md` so the
every-run read stays focused on finding the file and checking staleness, not on a bootstrap flow
that only ever happens once per project.

## Gather everything before asking anything

Before proposing creation, check the project's existing documentation for content that belongs in
`KNOWLEDGE.md` instead — a read-only step, so do it before asking permission to create anything,
not after. These files are supposed to document the repo *as designed* (or, for a troubleshooting
guide, as curated reference), but in practice they often accumulate gotcha-shaped bullets anyway,
simply because there was nowhere else to put them before now. This isn't the redundancy test from
`SKILL.md` Step 2 (the content is already written down, that's the premise). It's a
classification question. **Does this bullet describe a deliberate convention, decision, or curated
guidance (leave it), or an incidentally-discovered quirk or root-cause that ended up there for
lack of a better home (candidate to migrate)?** See `SKILL.md`'s intro for the full
CLAUDE.md/KNOWLEDGE.md boundary this test is drawing on.

Check a curated, bounded set of conventional locations — not every markdown file in the repo,
which would make this slow and noisy over content that's mostly unrelated (changelogs, ADRs, API
docs, contributing guides):
- At the project root: `README.md`, `CLAUDE.md`/`AGENTS.md`, `TSG.md`/`TROUBLESHOOTING.md`,
  `RUNBOOK.md`.
- The same filenames one level inside a `docs/`, `doc/`, or `documentation/` folder, if one exists — don't
  recurse further. A project with docs nested deeper than that needs the on-demand path (below)
  pointed at the specific file, since the automatic scan won't find it.

## Propose everything in one message

Fold all of the following into a single message rather than asking in stages — this is one of the
skill's hard rules (see the table in `SKILL.md`):
- Propose creating `KNOWLEDGE.md`:
  - at the location `session-start.md`'s "Found nowhere" rule resolves (an existing docs
    directory, else the project root; never a new one).
  - with a one-line explanation of what it's for: a place for repo gotchas/quirks/root-causes that
    cost real time to discover and aren't recorded anywhere else.
  - mentioning that it'll periodically prompt a "judgment-drift review" on its own (roughly every
    60-90 days, or sooner if entries have piled up) to prune stale entries (see
    `session-start.md`), so accepting the default means agreeing to that occasional review
    prompt, not just to the file existing.
  - mentioning that its header carries a `Feature check:` skill-version stamp, which the skill
    moves itself. After a skill upgrade, the skill says once what changed, then moves the stamp.
  - showing the header from "The header and the pointer".
- If the project has an instruction file, propose adding the pointer from "The header and the
  pointer". It keeps the two files DRY without duplicating content.
- If the scan above found candidates, list them as a single numbered list and propose migrating
  them (move, don't duplicate).
- Ask whether there's anywhere else worth checking for this kind of content — an internal wiki
  export, a team-specific notes file, anything the curated list above wouldn't anticipate. The
  curated list is a bet on common conventions, not a claim that it's exhaustive; rather than
  trying to keep growing it, ask once instead. This question is bootstrap-only — on later runs the
  on-demand path (below) covers it, since by then the user can just name a file directly instead
  of being asked in the abstract.

On confirmation:
1. Create `KNOWLEDGE.md` with today's date as `Last reviewed:`, the current skill version (top of
   `SKILL.md`) as `Feature check:`, the header, and an empty `## Entries` section. No
   `## Declined` section yet. That is added the first time a proposal is actually declined, see
   `SKILL.md` Step 2.
2. Add the pointer if confirmed.
3. Move (don't duplicate) each confirmed migration candidate into `KNOWLEDGE.md` as a proper
   entry, filling in Evidence from what's described and noting `Captured: <today> — migrated from
   <source file>`. The original discovery date isn't recoverable, so don't guess one.
4. Remove each migrated candidate from its source file.

**Check it's actually tracked.** The skill's "no archive needed, git history covers it" design
(see `SKILL.md`) only holds if `KNOWLEDGE.md` is actually committed, not gitignored or left
untracked. Right after creating it:
- Check (`git status` on the path) that it isn't ignored.
- If it is, say so and suggest committing it.
- This is a one-time check here, not repeated on later runs.

If the user names another location in answer to the open-ended question, check it with the same
classification test and propose whatever turns up as its own follow-up gate. This is new
information arriving after the first answer, not a second ask of the same question.

## The header and the pointer

A session often acts on an entry without this skill loaded. It reaches the entry through the
pointer or a grep. A person may also edit the file by hand. So `SKILL.md` Step 1 travels with
the file as its header, and the pointer sends readers there. This section holds the only copy of
both texts.

**The header** goes below the `Feature check:` line. It is the whole of Step 1 for a reader
without the skill:

```markdown
How to use this file, with or without the repo-knowledge skill:
- Before you act on an entry, check that its Evidence still holds. The file, symbol,
  heading or config key still exists, and a line number still shows what the entry says.
- Never run a command to check it if the command changes anything, such as a migration
  or a deploy. Check only that the command is still defined.
- If the Evidence holds, set `Last referenced` to today and add 1 to the count. If
  `Last referenced` is already today, change nothing.
- If it does not hold, set `Status: needs-review` and say so. If a `needs-review` entry
  holds again, set `Status: active` and say so.
- If you cannot reach the Evidence from this checkout, say so and change nothing.
- Give a new entry the same fields as the others. Anchor its Evidence on a file, symbol,
  heading or command, not on a line number.
```

**The pointer** is one line, with the path the file actually has:

```markdown
See `<path>` for known repo gotchas and quirks. Before you act on an entry, read the rules at the top of that file and follow them.
```

It goes in the project's instruction file, the first of these that applies:
1. The file that already holds a pointer to `KNOWLEDGE.md`. Keep its wording and path, and add
   the second sentence.
2. `AGENTS.md`, when `CLAUDE.md` imports it or there is no `CLAUDE.md`.
3. `CLAUDE.md`.

The pointer reaches a session that never opens the header, because an instruction file is read
at the start. The rules stay in the header, so there is one copy of them.

## Adding the header and pointer to an existing file

`changelog.md`'s 1.1.0 entry hands off here. The user can also ask for it at any time. This is one
of the skill's hard rules (see the table in `SKILL.md`):
- Show both texts in one message, and wait for an answer before writing either.
- The user accepts or declines each one separately.
- If the file or the instruction file already states the same rules in other words, say so. Offer
  to leave that text as it is.
- If the project has no instruction file, offer the header only.
- Write nothing for a declined text. The version check does not offer it again.

## Available on demand later, too

The curated-file scan (not the open-ended question) is also available any time after bootstrap —
e.g. "check CLAUDE.md for things that should move to repo knowledge" — for projects that adopted
this skill before this check existed, or where one of these files picked up new gotcha-shaped
content since.
