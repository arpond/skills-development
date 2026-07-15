---
name: repo-knowledge
description: Maintains a per-project KNOWLEDGE.md — a git-tracked, human-readable log of incidentally-discovered repo gotchas, root-causes, and dependency/environment quirks that cost real time to (re)discover and aren't already recorded anywhere findable (not in the code, not in CLAUDE.md, not in a commit message). Captures new entries proactively whenever a debugging session, incident, or piece of tribal knowledge clears a deliberate capture bar (redundant/surprising/costly/recurring), and explicitly when asked to "note this in repo knowledge" or similar. References existing entries when work touches a file/area one covers, mechanically checking the entry still holds before relying on it. Also runs an occasional judgment-drift review to prune stale or never-used entries. Use this whenever you resolve a non-obvious bug, hit a surprising quirk in a dependency/build/test/environment setup, are asked to check or review repo knowledge, or are about to work in an area of the repo that has a recorded entry.
---

# Repo knowledge

A place for the "why"-shaped facts that cost someone real time to figure out but don't live
anywhere else in the repo — not derivable from reading the code, not covered by `CLAUDE.md`
(which documents the repo as designed, not gotchas discovered along the way), and not reliably
captured in commit messages (commit quality varies by author, so "it's probably in git blame"
isn't a safe assumption). This skill is project-agnostic: everything project-specific lives in
`KNOWLEDGE.md` inside that project, not in this skill.

This file covers Steps 1-3, the steady-state reference/capture/removal loop. Two companion files
live alongside it:

- `session-start.md` — Step 0 (find or bootstrap `KNOWLEDGE.md`). **Not optional** — read it every
  run, right after this intro, before Step 1. Split out purely to keep this file's common-case
  read focused on the reference/capture/removal loop.
- `review.md` — the occasional judgment-drift review/prune pass. Read it when `KNOWLEDGE.md`'s
  `Last reviewed:` date says it's due (see `session-start.md`), or when the user explicitly asks
  to review/prune repo knowledge.

## The knowledge file

Each project that uses this skill has its own `KNOWLEDGE.md` at that project's root (i.e. the
directory containing its own code, not necessarily the overall repo root — a repo can hold several
independent projects, each with their own knowledge). This is the single source of truth for this
kind of fact — don't keep it split across multiple files or duplicated into `CLAUDE.md`.

Format:

```markdown
# Repo Knowledge

Last reviewed: <YYYY-MM-DD>

## Entries

### <Short title>
<Free-text: what happens, why it's non-obvious, how to avoid/resolve it>
- Evidence: `path/or/symbol/or command` — what to check to confirm this is still true
- Captured: <YYYY-MM-DD> — <what surfaced it, one line: incident, debugging session, PR>
- Last referenced: <YYYY-MM-DD> (referenced: <N>)
- Status: active | needs-review
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
- **No archive section.** The file is git-tracked, so a removed entry is fully recoverable via
  `git log`/`git blame` — don't build a second history mechanism for something git already gives
  for free.

**Hard rules by step, so a review can check none have gone missing:**

| Step | Hard rule |
|---|---|
| 0 (session-start.md) | Confirm with the user before creating `KNOWLEDGE.md` for the first time |
| 0 (session-start.md) | If the file exists but is malformed, ask the user rather than silently rewriting |
| 2 | Show the proposed new entry (or edit to an existing one) and wait for confirmation before writing it |
| 2 | Never write secrets, credentials, or PII into an entry — ask if uncertain |
| 3 | Confirm before removing an entry for staleness (a failed mechanical check alone isn't enough) |
| review.md | Present prune/needs-review candidates and wait for confirmation before removing anything |

*Update this table in the same edit whenever a hard rule is added, removed, or moved* — it's a
mirror of the steps, not independent prose, so it's the one place to check rather than several
scattered cross-references.

## Step 0: Find/bootstrap the knowledge file

Read `session-start.md` and follow it before continuing — it covers finding or bootstrapping
`KNOWLEDGE.md`, including the malformed-file case, and checking whether a judgment-drift review is
due. This is the one companion file that's read every run, not gated behind a trigger condition;
see the intro above for why it's split out. Once it says to, continue to Step 1 below.

## Step 1: Reference existing knowledge

When current work touches a file, module, command, or area that an existing entry's **Evidence**
overlaps with, surface that entry rather than letting the same ground get rediscovered.

Before relying on it, mechanically check the Evidence pointer still resolves — does the file/
symbol still exist, does the command still run the way it's described, does the config key still
exist. This is the staleness check, and it's deliberately event-triggered rather than a full sweep
of every entry every session: only check the entries actually relevant to what's being touched
right now, when they're about to be relied on.

- If the pointer still resolves: use the entry, then bump `Last referenced:` to today and
  increment the reference count.
- If it doesn't: mark `Status: needs-review` inline and say so plainly in the session — don't
  silently keep trusting it, and don't silently drop it either (see Step 3 for what happens next).
  Don't bump `Last referenced:` or the count in this case — a broken pointer wasn't actually a
  usable reference, and counting it would inflate the usage signal past what it means (see the
  knowledge-file notes above on what the count is for).
- If an entry is already marked `needs-review` from an earlier session, re-run the check rather
  than assuming the flag is still accurate — it may have been fixed (Evidence updated, or the
  underlying thing restored) without anyone clearing the flag. Re-checking is cheap; don't nag
  about the same flag more than once per session, though — surface it, then move on.
- **Evidence that points outside the current checkout** (a path or symbol in a different repo —
  common for entries describing a cross-repo relationship) can't be mechanically checked from
  here. Treat that as "unreachable isn't resolved," not a pass or a fail: say plainly that this
  entry's Evidence isn't checkable from this repo, and use it with that caveat rather than either
  silently trusting it or wrongly flagging it `needs-review` for a check that was never possible.
- **For Evidence that's a command with side effects** (a migration, a deploy, anything
  non-idempotent), "check it still resolves" means confirming the command is still defined/
  reachable (e.g. the script still exists in `package.json`/a `Makefile`/CI config) — never
  actually run it just to verify an entry.

## Step 2: Capture new knowledge

Two ways in: proactively, whenever something surfaces mid-session that clears the bar below (a
debugging session resolves with a non-obvious root cause, a dependency/build/test/environment
quirk trips something up); and explicitly, when asked to note something in repo knowledge.

**Apply the capture bar before proposing anything** — this is what keeps the file from filling
with noise:

1. **Redundancy test.** Two checks, both before proposing anything new:
   - Findable via `git blame`/`git log`/a quick grep on the relevant code in under a minute? If
     yes, skip it — the information already exists, checking for it beats assuming it's there.
     This holds regardless of whether the relevant commit message was any good; commit quality
     varies by author, so "check if it's actually findable right now" is the test, not "should a
     commit message have covered this."
   - Already recorded in `KNOWLEDGE.md`, in substance, under a different title or wording? If a
     candidate is genuinely the same fact as an existing entry (or a refinement of it — a broader
     case, an updated workaround, Evidence that's moved), don't propose a duplicate: propose an
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

If it clears the bar, propose a concise entry (title, description, Evidence, Captured) and wait
for confirmation before writing anything — this is one of the skill's hard rules (see the table
above): capture is a recommendation, not a decision. Match `KNOWLEDGE.md`'s existing format and
voice for whatever gets added.

**Never write secrets, credentials, or PII into an entry.** If a capture candidate touches
something sensitive (an internal URL, a credential, customer data specifics), say so explicitly
and ask how to phrase it safely rather than writing the sensitive detail verbatim. This is a hard
rule, not a judgment call to skip under time pressure.

## Step 3: Removal

Three triggers, and only these three — removal is never time-based or automatic:

- **A fix supersedes the entry.** When a change fixes the root cause an entry describes, remove
  the entry as part of that same change. Mention it in the session rather than doing it invisibly
  — low-stakes given git history, but still a change worth naming.
- **The mechanical check fails and the user confirms it's actually gone.** Step 1 flagging
  `Status: needs-review` isn't enough on its own (a failed pointer check could mean the thing
  moved, not that it's resolved) — confirm with the user before removing.
- **Surfaced as a prune candidate during `review.md`.** Never-referenced or long-stale entries get
  raised there, not removed on sight; see `review.md` for how that's presented.
