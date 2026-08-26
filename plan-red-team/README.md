# plan-red-team

Reviews a plan or proposal with a panel of blind adversarial subagents. Each agent attacks from
one angle, in its own persona, and none sees another's output. Blindness is the point. A single
reviewer anchors on its first framing and softens toward the author. Independent agents cannot
converge, so their agreements mean something. After the panel, a cross-perspective agent attacks
the interactions between findings. A separate aggregator then passes a verdict on every finding,
with reasons. The main thread relays that report and adds its own labeled commentary. It does
not judge alone, because it often wrote the plan under review.

Angles come from two sources. The skill always derives a roster to fit the plan in front of it.
Derivation is blind too. Three deriver subagents each propose angles from the plan text alone,
and the merge marks the angles they converge on. The main thread does not pick the angles for a
plan it may have written. The user can also keep preset rosters for task types they review
often, and a matching preset is always offered verbatim beside the derived one. No panel agent
spawns until the user confirms the roster, the cost, and the output target at a single gate.

Files:

- `SKILL.md` — the whole run: config, plan resolution, roster options, the panel gate, both
  waves, aggregation, delivery. Read on every invocation.
- `bootstrap.md` — first-use setup. Read only when no config file exists yet.
- `references/preset-library.md` — bundled starter presets. Read at setup, or when you ask to
  adopt more later.

## Cost

Expensive by design. One run spawns the roster size plus two subagents, so usually five to
seven. Each gets the full plan text. When the plan targets the current repo, the wave agents
also get read-only repo access and spend tokens verifying claims against code. Roster derivation
adds three more small spawns before the gate. Those are cheap — plan text in, an angle list out
— and the setup gate confirms that default. Turn it off in the config file, say "skip
derivation" for one run, or re-run a previous panel, which skips it by itself. The panel gate
states the panel's spawn count before it runs, and you control the roster size there. There is
no cheap path. For a quick solo critique, ask for one instead of this skill.

## What it writes

- `~/.claude/plan-red-team-presets.md` — the config file that holds your preset rosters and the
  two derivation settings. Created at first use, after you confirm its exact content. Later preset additions and edits are each
  shown and confirmed first.
- A report file, only when you pick that output target at the gate. Default placement is beside
  the plan file. An existing file at that path is surfaced, never overwritten silently.

Nothing else. By default the report arrives in chat and no project file is touched. Nothing
leaves the machine.

## Requires

- The ability to spawn subagents (the Agent tool in Claude Code). Without it the skill cannot
  run at all — the panel is the mechanism, not a preference.
- Nothing else beyond local file read and write. Repo access for agents is optional and applies
  only when the plan targets a codebase.

## When it triggers

- "Red-team this plan" / "attack this proposal"
- "Have a panel tear this apart" / "review this from multiple perspectives"
- "Stress-test this design with blind reviewers"
- "Poke holes in this migration plan"

It is not for interviewing the user about their own thinking, and not for a quick solo critique.
Both are cheaper asks that need no panel.

## Example

```
User: Red-team docs/auth-migration-plan.md

Claude: [reads config, finds the "Software design plan" preset matches, derives an
  alternative roster, then gates]

  Attacking: docs/auth-migration-plan.md (verbatim). Agents get read-only repo access —
  the plan claims the session store is already tokenised, which they can verify.

  Roster options:
  1. Preset "Software design plan", verbatim (recommended) — Security, Operations,
     Scalability, Simplicity, Data integrity (5 angles, personas as saved)
  2. Same preset, adapted — Scalability re-aimed at the token-refresh hot path
  3. Derived (3 blind derivers) — Security (3 of 3), Data integrity (2 of 3), Operations,
     plus a Rollout-sequencing angle one deriver proposed
  Output:
  4. Report in chat
  5. Report file beside the plan

  Panel spawns: roster + cross + aggregator = 7 for options 1–2, 6 for option 3.

User: 1 and 4

Claude: [spawns 5 blind agents in parallel, then the cross agent, then the aggregator;
  relays the report]

  # Red-team review — auth-migration-plan
  Panel: 5 angles + cross · 2026-08-26
  ## Verdict summary
  2 Critical, 3 Major, 4 Minor endorsed. The dual-write window is the load-bearing
  weakness: three angles converged on it independently. ...
  ## Main-thread commentary
  This plan was drafted in this session, so weigh my pushback accordingly. I agree with
  the dual-write finding and would fix it before anything else. I would push back on ...
```
