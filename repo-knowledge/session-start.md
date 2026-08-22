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
fields, an unparseable `Last reviewed:` date. This is a case of "unreachable isn't resolved," not
a normal empty file; reshaping guesses at intent the user never confirmed.
- Name the specific thing that doesn't parse and ask directly: fix it by hand, or walk through
  repairing just that piece, leaving everything else untouched.
- Never fabricate plausible-looking Evidence or dates to paper over a broken entry. A wrong guess
  here is exactly the kind of silent-drift failure the mechanical staleness check in `SKILL.md`
  Step 1 exists to catch, not create.

This is one of the skill's hard rules (see the table in `SKILL.md`).

**If it exists but clearly isn't ours, don't touch it, and don't bolt entries onto someone else's
document.** "Clearly isn't ours" means it reads as unrelated documentation with no `## Entries`
section and no resemblance to this schema at all, rather than a broken/partial version of it: a
naming collision, not a malformed file. Say so and ask where this skill's file should live instead
(a different filename is the obvious fix; note the actual name chosen wherever this skill would
otherwise assume `KNOWLEDGE.md`).

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
