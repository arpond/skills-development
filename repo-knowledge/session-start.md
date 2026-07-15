# Session start: find the knowledge file, check staleness

Read this file every time the skill triggers, right after `SKILL.md`'s intro — this is Step 0 of
the loop. Every run needs to know whether `KNOWLEDGE.md` exists and is well-formed before Step 1
can reference anything against it. It lives in its own file purely to keep `SKILL.md` focused on
the steady-state reference/capture/removal loop — the split is about what's loaded into the
common-case read, not about this content being rare.

Once this file's step is done, continue to Step 1 in `SKILL.md`.

## Step 0: Find `KNOWLEDGE.md`, or bootstrap it

Look for `KNOWLEDGE.md` at the root of whichever project the user is currently working in (use
judgement on project boundary: the nearest enclosing directory with its own README, package
manifest, or similar — not necessarily the git repo root, since one repo can contain several
projects with different concerns).

**If it doesn't exist yet**, read `setup.md` and follow it before doing anything else — that's a
one-time-per-project bootstrap, kept out of this file since every run after the first doesn't need
it.

**If it exists, read it as-is and continue** — don't re-run setup. Judgment-drift review timing is
handled separately below, not here.

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
