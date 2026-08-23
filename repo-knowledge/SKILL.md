---
name: repo-knowledge
description: Maintains a per-project KNOWLEDGE.md — a git-tracked, human-readable log of incidentally-discovered repo gotchas, root-causes, and dependency/environment quirks that cost real time to (re)discover and aren't already recorded anywhere findable (not in the code, not in CLAUDE.md, not in a commit message). Captures new entries proactively whenever a debugging session, incident, or piece of tribal knowledge clears a deliberate capture bar (redundant/surprising/costly/recurring), and explicitly when asked to "note this in repo knowledge" or similar. References existing entries when work touches a file/area one covers, mechanically checking the entry still holds before relying on it. Also runs an occasional judgment-drift review to prune stale or never-used entries. Use this whenever you resolve a non-obvious bug, hit a surprising quirk in a dependency/build/test/environment setup, are asked to check or review repo knowledge, are asked whether existing docs (README, CLAUDE.md/AGENTS.md, a troubleshooting guide/runbook, or their docs-folder equivalents) contain gotchas that should move into repo knowledge, or are about to work in an area of the repo that has a recorded entry.
---

# Repo knowledge

**Skill version: 1.0.0.** `session-start.md`'s version check compares `KNOWLEDGE.md`'s
`Feature check:` stamp against this number. `changelog.md` holds what shipped at each version and
the versioning policy. Read it only when that check finds a gap, not on every run.

A place for the "why"-shaped facts that cost someone real time to figure out but don't live
anywhere else in the repo — not derivable from reading the code, not covered by `CLAUDE.md`
(which documents the repo as designed, not gotchas discovered along the way), and not reliably
captured in commit messages (commit quality varies by author, so "it's probably in git blame"
isn't a safe assumption). This skill is project-agnostic: everything project-specific lives in
`KNOWLEDGE.md` inside that project, not in this skill.

This file covers Steps 1-3, the steady-state reference/capture/removal loop. Four files live
alongside it. `session-start.md` is a second core file, the other three are companions:

- `session-start.md` — Step 0 (find `KNOWLEDGE.md`, or defer to `setup.md` to bootstrap it).
  **Not optional** — read it every run, right after this intro, before Step 1. Split out purely to
  keep this file's common-case read focused on the reference/capture/removal loop.
- `setup.md` — the one-time-per-project bootstrap: creating `KNOWLEDGE.md`, the `CLAUDE.md`
  pointer, and the doc-migration scan. Read only the first time `session-start.md` finds no
  `KNOWLEDGE.md` yet — never on later runs.
- `review.md` — the occasional judgment-drift review/prune pass. Read it when `KNOWLEDGE.md`'s
  `Last reviewed:` date says it's due (see `session-start.md`), or when the user explicitly asks
  to review/prune repo knowledge.
- `changelog.md` — what each skill version changed, for telling an existing `KNOWLEDGE.md` what
  it is missing. Read it only when `session-start.md`'s version check finds its `Feature check:`
  behind the current skill version.

## The knowledge file

Each project that uses this skill has its own `KNOWLEDGE.md`, one per project — where "project"
means the directory containing its own code, not necessarily the overall repo root, since a repo
can hold several independent projects each with their own knowledge. **`session-start.md` Step 0
resolves where that file actually lives** (project root, the project's own docs directory, or
`.claude/`); don't assume a path here. This is the single source of truth for this kind of fact —
don't keep it split across multiple files or duplicated into `CLAUDE.md`.

Format:

```markdown
# Repo Knowledge

Last reviewed: <YYYY-MM-DD>
Feature check: v<X.Y.Z>

## Entries

### <Short title>
<Free-text: what happens, why it's non-obvious, how to avoid/resolve it>
- Evidence: `path/or/symbol/or command` — what to check to confirm this is still true
- Captured: <YYYY-MM-DD> — <what surfaced it, one line: incident, debugging session, PR>
- Last referenced: <YYYY-MM-DD> (referenced: <N>)
- Status: active | needs-review

## Declined
- **<Short title>** (<YYYY-MM-DD>) — one-line reason it was declined.
```

- **Entries** is a flat list — no category headers. Grouping can be added later if the file grows
  enough to need it; don't invent a taxonomy ahead of real data.
- **Evidence** is what makes an entry mechanically checkable: a file path, a function/symbol name,
  a config key, or a command. It's what Step 1's staleness check and `review.md`'s mechanical pass
  both key off. An entry without a checkable Evidence line is a weaker candidate for capture in
  the first place (see Step 2).
- **Last referenced** and **referenced: N** exist for two reasons at once: they're a usage/success
  signal (is this file actually earning its keep) and a curation signal (entries with a zero count
  are prune candidates in `review.md`, independent of whether they've gone factually stale).
- **Status: needs-review** is set by Step 1's mechanical check when Evidence no longer resolves —
  a flag for a human to look at, never a silent deletion.
- **Last reviewed:** at the top drives `review.md`'s occasional judgment-drift prompt — same
  mechanism as `next-improvement`'s Goals staleness date.
- **`Feature check:`** is a skill-version stamp: the skill version last disclosed to this file.
  `session-start.md` owns it (backfill, compare, bump after disclosure). Nothing in Steps 1-3
  reads or writes it.
- **No archive section for removed entries.** The file is git-tracked, so a removed entry is fully
  recoverable via `git log`/`git blame` — don't build a second history mechanism for something git
  already gives for free.
- **Declined** is append-only history, never deleted from. It holds capture *proposals the user
  explicitly turned down*, not candidates the capture bar itself filtered out before ever
  reaching the user (those aren't logged anywhere; that's the capture bar doing its job, not a
  decline). Distinct from removed entries (which have git history) because a declined proposal was
  never written anywhere, so without this there'd be nothing to check before re-proposing the same
  thing later. An entry that eventually gets captured after an earlier decline doesn't retroactively
  remove that old `Declined` line — it stays as-is, same as `next-improvement`'s `Rejected` (see
  Step 2). Whatever gets written here is still subject to the same secrets/PII rule as entries.

**Hard rules by step, so a review can check none have gone missing.** Scope: rules that fail
*silently* if skipped — gates (including must-ask obligations), the secrets/PII prohibition, and
surfaces alike, since all three break without anything visibly going wrong (a leaked credential
surfaces long after the fact, an unasked question never gets asked, an unsaid version gap stays
unsaid). The **Kind** column marks which: **gate** (show, then wait for
an answer), **surface** (say it, no answer needed), **prohibition** (never do it). It deliberately
does not list every-run behaviour whose omission shows up on its own — referencing an entry when
work touches its area, running an entry's mechanical check before relying on it. Absence from this
table does not mean optional.

| Step | Kind | Hard rule |
|---|---|---|
| 0 (setup.md) | gate | Propose creating `KNOWLEDGE.md`, migration candidates, and the CLAUDE.md pointer in one message, and wait for confirmation before writing/moving anything |
| 0 (setup.md) | gate | Ask whether there's anywhere else worth checking, don't assume the curated list is exhaustive |
| 0 (session-start.md) | gate | If the file exists but is malformed, ask the user rather than silently rewriting |
| 0 (session-start.md) | surface | Surface a `Feature check:` version gap, including a missing stamp, walked as `0.0.0` |
| 0 (session-start.md) | surface | Surface an unexpectedly-ahead `Feature check:` stamp rather than resolving it either way |
| 2 | gate | Show the proposed new entry (or edit to an existing one) and wait for confirmation before writing it |
| 2 | prohibition | Never write secrets, credentials, or PII into an entry or a Declined line — ask if uncertain |
| 3 | gate | Confirm before removing an entry for staleness (a failed mechanical check alone isn't enough) |
| review.md | gate | Present prune/needs-review candidates and wait for confirmation before removing anything |

*Update this table in the same edit whenever a hard rule is added, removed, or moved.* It's a
mirror of the steps, not independent prose, so it's the one place to check rather than several
scattered cross-references.

**Whenever two or more options are presented for the user to pick from, number them `1.`, `2.`,
`3.`… in a single sequential list**, whatever label each carries. Sites in this skill: migration
candidates at Step 0, prune/needs-review candidates in `review.md`, several entries surfaced at
once. A label explains an option; a number is what the user can say back ("go with 2") to pick
one unambiguously. A single unambiguous recommendation with nothing else to choose between doesn't
need one. This applies at every such point in this skill, including any added later.

## Step 0: Find/bootstrap the knowledge file

Read `session-start.md` and follow it before continuing. It covers finding `KNOWLEDGE.md`
(deferring to `setup.md` to bootstrap it if missing), the malformed-file case, and checking
whether a judgment-drift review is due. Once it says to, continue to Step 1 below.

## Step 1: Reference existing knowledge

When current work touches a file, module, command, or area that an existing entry's **Evidence**
overlaps with, surface that entry. Don't let the same ground get rediscovered.

Before relying on it, mechanically check the Evidence pointer still resolves. Resolves means: the
file/symbol still exists; the command still runs the way it's described; the config key still
exists. This is the staleness check, and it's deliberately event-triggered rather than a full sweep
of every entry every session: only check the entries actually relevant to what's being touched
right now, when they're about to be relied on.

- If the pointer still resolves: use the entry. Then bump `Last referenced:` to today and
  increment the reference count.
- If it doesn't:
  - Mark `Status: needs-review` inline and say so plainly in the session.
  - Don't silently keep trusting it, and don't silently drop it either (see Step 3 for what
    happens next).
  - Don't bump `Last referenced:` or the count. A broken pointer wasn't actually a usable
    reference, and counting it would inflate the usage signal past what it means (see the
    knowledge-file notes above on what the count is for).
- If an entry is already marked `needs-review` from an earlier session, re-run the check rather
  than assuming the flag is still accurate. It may have been fixed (Evidence updated, or the
  underlying thing restored) without anyone clearing the flag. Re-checking is cheap. Don't nag
  about the same flag more than once per session: surface it, then move on.
- If more than one relevant entry needs a decision from the user in the same pass (e.g. two
  touched entries both flagged `needs-review`), number them in one list (the numbering rule
  above).
- Evidence **pointing outside the current checkout** (another repo — common for cross-repo
  entries) can't be checked from here at all. Treat it as "unreachable isn't resolved" and say
  so, rather than passing, failing, or silently skipping it.
- Evidence that's a **side-effectful command** (a migration, a deploy): check only that it's
  still defined/reachable (e.g. still present in `package.json`/a `Makefile`). Never actually run
  it to verify.

## Step 2: Capture new knowledge

Two ways in: proactively, whenever something surfaces mid-session that clears the bar below (a
debugging session resolves with a non-obvious root cause, a dependency/build/test/environment
quirk trips something up); and explicitly, when asked to note something in repo knowledge.

**Apply the capture bar before proposing anything.** This is what keeps the file from filling
with noise:

1. **Redundancy test.** Two checks, both before proposing anything new:
   - Findable via `git blame`/`git log`/a quick grep on the relevant code in under a minute? If
     yes, skip it — the information already exists, checking for it beats assuming it's there.
     This holds regardless of whether the relevant commit message was any good; commit quality
     varies by author, so "check if it's actually findable right now" is the test, not "should a
     commit message have covered this."
   - Already recorded in `KNOWLEDGE.md`, in substance, under a different title or wording? If a
     candidate is genuinely the same fact as an existing entry (or a refinement of it — a broader
     case, an updated workaround, Evidence that's moved), don't propose a duplicate. Propose an
     **edit to the existing entry** instead, and say what's changing and why. If it's a
     genuinely distinct fact that merely touches the same area, a new entry is fine — the test is
     substance, not just topical overlap.
2. **Surprise test.** Would a competent developer already familiar with this codebase still be
   caught out by this? Filters out things that only felt like an insight in the moment of
   discovery.
3. **Cost-to-rediscover.** How much time or pain did finding this take? A five-minute "oh" doesn't
   need an entry; a half-day debugging session or an incident does. Higher cost lowers the bar.
4. **Recurrence likelihood.** Structural and likely to bite someone else again, or a genuine
   one-off? One-offs are weak candidates even when they were painful.

**Check Declined before proposing.** If a candidate closely resembles something already in
`Declined`, don't silently re-propose it or silently suppress it — read the recorded reason and
judge whether it still applies. A timing reason ("not sure yet, wait and see") can go stale; a
substance reason ("too narrow to be useful," "not actually surprising") usually doesn't. When
genuinely unsure, it's fine to re-propose with a note ("this was declined before for X — has that
changed?").

If it clears the bar:
- Propose a concise entry (title, description, Evidence, Captured) and wait for confirmation
  before writing anything. This is one of the skill's hard rules (see the table above): capture
  is a recommendation, not a decision.
- If more than one candidate clears the bar in the same pass, number them in one list (the
  numbering rule above).
- Match `KNOWLEDGE.md`'s existing format and voice for whatever gets added.
- **If declined, add it to `Declined` with the reason given** (or your best summary of it if
  terse) rather than just dropping it. That's what makes the check above work next time.

**Never write secrets, credentials, or PII into an entry or a `Declined` line.** If a capture
candidate, or the reason for declining one, touches something sensitive (an internal URL, a
credential, customer data specifics), say so explicitly and ask how to phrase it safely. Don't
write the sensitive detail verbatim. This is a hard rule, not a judgment call to skip under time
pressure.

## Step 3: Removal

Three triggers, and only these three — removal is never time-based or automatic:

- **A fix supersedes the entry.**
  - When a change fixes the root cause an entry describes, remove the entry as part of that same
    change.
  - Mention it in the session rather than doing it invisibly; low-stakes given git history, but
    still a change worth naming.
  - **After fixing a root cause, check `KNOWLEDGE.md` for a matching entry before moving on.**
    Don't rely solely on Step 1 having already surfaced it. A root-cause fix often lands in a
    different file than the entry's Evidence points at (Evidence tends to record where the symptom
    showed up, not necessarily where the eventual fix happens), so Step 1's file-overlap check can
    miss it entirely. The mechanical check in Step 1 only verifies a pointer still resolves, not
    that the behavior it describes is still true, so a genuinely-fixed bug won't surface itself on
    its own.
- **The mechanical check fails and the user confirms it's actually gone.** Step 1 marking
  `Status: needs-review` isn't enough on its own (a failed pointer check could mean the thing
  moved, not that it's resolved). Confirm with the user before removing.
- **Surfaced as a prune candidate during `review.md`.** Never-referenced or long-stale entries get
  surfaced there, not removed on sight; see `review.md` for how that's presented.
