# Review: judgment-drift pass

Read this file when `session-start.md` says a review is due, or when the user explicitly asks to
review/prune repo knowledge. This is deliberately separate from `SKILL.md` Step 1's mechanical
staleness check: that check runs per-entry, cheaply, only when an entry is about to be relied on,
and it can only catch mechanical drift (does the Evidence pointer still resolve). This pass is
occasional and judgment-based — it catches the case a mechanical check can't: a fact that's still
technically true but is no longer the most useful framing, has been superseded by a better fix, or
never turned out to matter to anyone.

## Gather candidates

Read every entry in `KNOWLEDGE.md` and collect, without editing anything yet:

- Any entry already marked `Status: needs-review` from Step 1's mechanical check.
- Any entry with `referenced: 0` — never used since capture. Zero references doesn't necessarily
  mean the entry is wrong, but it's a real signal worth a human eye: either nobody's hit the
  situation it describes since, or nobody's finding it when they do.
- As a soft suggestion, not a removal candidate: entries with a notably high reference count.
  These are working, but a fact that keeps coming up repeatedly is also a candidate for a more
  permanent fix — promoting the note into `CLAUDE.md`, fixing the underlying issue in code, or
  adding a lint rule — rather than staying a workaround note indefinitely. Mention this as a
  suggestion alongside the candidate list; it's not one of the three removal triggers and doesn't
  need the same confirm-before-acting treatment, since nothing's being removed.

## Present, then wait

Fold everything into a single message, one per review, not one prompt per entry.
**Number every candidate in one sequential list** (needs-review and zero-reference entries
together, in whatever order), so the user can respond by number ("prune 1 and 3, keep 2") instead
of re-typing titles — e.g.:

"5 entries could use a look: 1. '<title>' — needs-review, Evidence no longer resolves.
2. '<title>' — needs-review, Evidence no longer resolves. 3. '<title>' — never referenced since
<date>. 4. '<title>' — never referenced since <date>. Want to prune any of these, or keep them
as-is? Separately, '<title>' has been referenced 6 times — might be worth promoting into
CLAUDE.md or fixing properly instead of staying a workaround note." (The high-reference-count
suggestion stays outside the numbered list — nothing is being removed there, so there's no
selection to make.)

**Wait for confirmation before removing or archiving anything.** This is one of the skill's hard
rules (see the table in `SKILL.md`). A needs-review flag or a zero reference count is a candidate,
not a verdict; the user may know the entry is still exactly right and just hasn't come up
recently, or may confirm it's genuinely gone.

Whatever the user decides:
- Confirmed-gone entries are removed outright — no archive section, git history already preserves
  them (see `SKILL.md`'s "no archive section" note).
- Entries the user wants to keep stay exactly as they are.
- If a kept entry had been `needs-review` and the user confirms it's still valid (e.g. the thing
  moved rather than disappeared): reset `Status` to `active`, and update Evidence to the new
  location instead of leaving it marked.
- **Bump `Last reviewed:` to today regardless of outcome.** Same as `next-improvement`'s Goals
  check-in — so the next run doesn't re-prompt immediately even if nothing changed.
