# Session start: find the knowledge file, check staleness

Read this file every time the skill triggers, right after `SKILL.md`'s intro — this is Step 0 of
the loop. Every run needs to know whether `KNOWLEDGE.md` exists and is well-formed before Step 1
can reference anything against it.

Once this file's step is done, continue to Step 1 in `SKILL.md`.

## Step 0: Find `KNOWLEDGE.md`, or bootstrap it

First establish the project: the nearest enclosing directory with its own README, package manifest,
or similar — not necessarily the git repo root, since one repo can contain several projects with
different concerns.

**Then resolve `KNOWLEDGE.md` over these locations, in order, first hit wins:**

1. `<project>/KNOWLEDGE.md`
2. `<project>/<docs-dir>/KNOWLEDGE.md` — where `<docs-dir>` is `docs/`, `doc/`, or
   `documentation/`, whichever the project already has
3. `<project>/.claude/KNOWLEDGE.md`

Don't assume location 1 and stop. A knowledge file that exists somewhere else would be invisible,
and the next step would bootstrap a second one on top of real entries — silently.

**Found in more than one location**: don't take the first and don't merge them. Say which files
were found where and ask which is authoritative; "first hit wins" orders the *lookup*, it isn't
permission to strand a second copy.

**Found nowhere**: read `setup.md` and follow it before doing anything else — a one-time-per-project
bootstrap, kept out of this file since every run after the first doesn't need it. It creates the
file in `<docs-dir>/` if the project already has one, otherwise at `<project>/`. **Never create a
docs directory to hold it.** That imposes a layout the project didn't choose.

**Found somewhere other than location 1**: normal, not something to fix. Use it where it is;
existing files never get moved as a side effect of a run.

**If it exists, read it as-is and continue.** Don't re-run setup. Judgment-drift review timing is
handled separately below, not here.

**If it exists but is malformed, don't silently reshape it back into form, and don't refuse to
proceed either.** Malformed means: no `## Entries` section, an entry missing one of the required
fields, an unparseable `Last reviewed:` date, or a `Feature check:` that is not a valid `X.Y.Z`
version. This is a case of "unreachable isn't resolved," not a normal empty file; reshaping
guesses at intent the user never confirmed.
- Name the specific thing that doesn't parse and ask directly: fix it by hand, or walk through
  repairing just that piece, leaving everything else untouched.
- Never fabricate plausible-looking Evidence or dates to paper over a broken entry. A wrong guess
  here is exactly the kind of silent-drift failure the mechanical staleness check in `SKILL.md`
  Step 1 exists to catch, not create.

This is one of the skill's hard rules (see the table in `SKILL.md`).

**If it exists but clearly isn't ours, don't touch it, and don't bolt entries onto someone else's
document.** "Clearly isn't ours" means it reads as unrelated documentation with no `## Entries`
section and no resemblance to this schema at all, rather than a broken/partial version of it: a
naming collision, not a malformed file. Say so and ask where this skill's file should live
instead; a different filename is the obvious fix. Note the actual name chosen wherever this skill
would otherwise assume `KNOWLEDGE.md`.

## Checking the skill version

`KNOWLEDGE.md`'s `Feature check:` stamp records the skill version last disclosed to this file.
Compare it against `SKILL.md`'s current skill version every run, once Step 0 accepts a file as
ours and before Step 1.

**Missing** (the file predates the field, or someone created it by hand): not malformed. Backfill
it to `0.0.0` as mechanical, no-confirmation bookkeeping, then continue as behind. A missing stamp
is evidence of being behind, never proof of being current. To stamp it straight to the current
version and skip the walk below is exactly the failure this paragraph exists to block.

**Compare as semver**: major, then minor, then patch, each numerically. `1.10.0` is newer than
`1.9.0`. Never compare as strings.

**Behind:**
1. Read `changelog.md`. This is its only read condition.
2. Walk every entry newer than the stamp, oldest first. `changelog.md` lists newest first for a
   human reader. Application order is the reverse, because a later entry can assume an earlier
   one landed.
3. Fold the result into the same message as any judgment-drift review that is due (below), not a
   second message. An opt-in item hands off to its own gate. Say an automatic item in a clause if
   it changes what the user will see. Otherwise stay silent about it.
4. Bump `Feature check:` to the current skill version after the disclosure, whatever the user
   decided. Do not re-offer a declined item every session.

**Ahead** (the stamp is newer than this install's version: a downgraded install, or a file copied
from a machine running a newer skill): surprising input, not a case to resolve either way. Say so
once and ask whether the install is stale. Do not walk `changelog.md`, because nothing in it is
newer. Do not touch the stamp.

**Current**: nothing to do.

Both surfaces here are hard rules (see the table in `SKILL.md`).

## Checking whether a judgment-drift review is due

Check the `Last reviewed:` date at the top of `KNOWLEDGE.md`:

- **Missing** (file predates this field, or was created by hand): treat as due.
- **Older than ~60-90 days, or entry count has grown noticeably since the last review**: a
  judgment-drift review is due. Read `review.md` and follow it before Step 1. Fold its gate into a
  single message rather than interrupting twice.
- **Recently reviewed and nothing suggests drift**: skip straight to Step 1 in `SKILL.md`.

This is separate from Step 1's mechanical staleness check; `review.md`'s header says how. The
user can also trigger `review.md` at any time outside a normal run, e.g. by asking to "review
repo knowledge."
