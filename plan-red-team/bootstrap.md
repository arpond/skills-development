# First-use setup

Read this only when Step 0 found no config file at `~/.claude/plan-red-team-presets.md`. The job
here: let the user adopt starter presets, then create that file so this never runs again. A
config with zero presets is a valid outcome — the panel gate then offers only derived rosters.

## Step 1 — Offer the bundled presets

Read `references/preset-library.md`. Present each bundled preset as a numbered option: its task
type name, its `Matches:` line, and its angles (name plus a shortened persona). Multi-select —
the user can pick several, all, or none. Make the none case explicit as its own numbered option:

> N. None — derive a fresh roster per plan, every run

Say what adoption means: chosen presets are copied into a personal config file the user owns and
can edit. Unchosen ones stay available to adopt later. Say the file's exact path. Presets are a
starting point, not a commitment — the panel gate always offers a derived roster too, whatever
is adopted here.

Also state the derivation default, because a default the user never saw is not a default.
Derived rosters come from three blind deriver subagents, merged on convergence, before every
panel that is not a re-run. Both settings (`Blind derivation: on`, `Derivers: 3`) land in the file, are
independently editable, and can be changed here if the user objects to the cost.

## Step 2 — Confirm the write

**This is a gate, indexed in `SKILL.md`'s hard-rules table.** Show the exact content the config
file will hold — the adopted entries verbatim from the library, under this header:

```markdown
# plan-red-team presets

Preset rosters, one per task type, read by plan-red-team on every run. A matching
preset is offered verbatim at its panel gate. Edit freely. Each entry is a `##`
heading naming the task type, then a `Matches:` line, then one angle per bullet
as `<name>: <attack focus> | Persona: <one sentence>`. The settings lines below
govern blind roster derivation.

Blind derivation: on
Derivers: 3
```

The header holds no example entry, deliberately: a literal placeholder entry would parse as a
preset. The settings lines carry whatever was agreed in Step 1, not always these defaults, and
adopted entries follow beneath them.

If the user declines the write entirely, write nothing. Continue this run derived-only, and say
that setup will offer again next run — with no file there is nowhere to record the refusal.

Wait for confirmation before writing. If the user picked none, the file still gets written with
the header alone. An existing empty config is what stops this setup re-firing on every run.

## Step 3 — Continue

Write the file and confirm it landed. Then return to `SKILL.md` Step 1. Do not re-read the
library this run; the adopted presets are now in the config Step 2 just wrote.
