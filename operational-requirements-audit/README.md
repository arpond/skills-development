# operational-requirements-audit

Audits a repo or service against Findmypast's Operational Requirements (ORs). These are org-wide
standards that cover testing, dashboards, databases, deployment, developer experience,
documentation, logging and instrumentation, monitoring and alerting, resilience, and SLOs. It
produces a per-OR compliance report (Met / Partial / Not Met / N/A / Unverifiable from repo)
backed by concrete evidence from the codebase.

The OR text itself is bundled with the skill (`references/operational-requirements.md`), extracted
from Discourse pages saved as HTML, not re-derived from memory each time. Wording matters, and
requirements get refined over time, so the audit reads the current text instead of a guess from a
requirement's title.

Files:
- `SKILL.md` — the audit workflow: confirm scope, read the bundled ORs, investigate each one with
  real evidence (grep and read the repo, not keyword guessing), then write a structured report.
- `references/operational-requirements.md` — the bundled OR text, one entry per requirement,
  grouped by category. Regenerate it with `scripts/extract_ors.py` when the source Discourse
  export refreshes.
- `scripts/extract_ors.py` — parses a folder of Discourse pages saved as HTML (one OR per page)
  and extracts each page's title and first post into the bundled reference file. The first post
  is the requirement definition. Later Discourse replies are discussion, not part of the
  requirement, and the script deliberately excludes them.

## Cost

**The most expensive skill in this repo, for a full audit.** No MCP calls or external services,
but it reads the whole bundled OR reference and then investigates each requirement against the
target repo separately. That is a grep and a read per OR, across about 10 categories, because a
verdict without a cited file path is not a verdict. Expect real exploration time on a repo of any
size, and a long conversation turn before the summary appears.

**A single-OR question is cheap.** It reads that one requirement's text and investigates only
that. "Does this meet the backups OR?" is a small fraction of a full run. So ask narrowly when you
only care narrowly, instead of a full run to read one row of the result.

## What it writes

- **`OPERATIONAL_REQUIREMENTS_AUDIT.md`** — the report, at the root of the audited target: the
  repo root, or a service subdirectory if the repo holds several independently deployed services
  and you scoped the audit to one.

**Only for a full or explicitly multi-OR audit, or if you ask.** The skill answers a narrow "does
this service meet the backups OR?" in the conversation and writes nothing. It shows and confirms
the summary table before it writes the file. If a report of the same name already exists, it says
so in that same message, not afterwards.

It writes nothing else: no changes to the audited code, and nothing outside the repo.

## Requires

Nothing beyond local file read and search (Read/Grep/Glob) to investigate the target repo. A
refresh of the bundled ORs needs Python 3 (standard library only, no extra packages) and a fresh
HTML export from Discourse.

## When it triggers

- "Audit this repo against the operational requirements."
- "Does this service meet the ORs?"
- "Check whether this meets the backups OR." (a single-OR request: the skill investigates and
  reports only that one)
- "Is this service production-ready per Findmypast's service standards?"

## Example: full audit

```
You: Audit this repo against the operational requirements.

Claude: [invokes operational-requirements-audit]
        This repo has two independently-deployed services — `search-api/` and
        `indexer/` (separate Dockerfiles and pipeline definitions). Auditing
        both as one thing would blur verdicts that differ between them.
        Which do you want: search-api, indexer, or both separately?

You: search-api.

Claude: [reads references/operational-requirements.md in full, then investigates
         each OR against search-api/ — grep and read, not keyword guessing]

        Audit of search-api against all ORs:

        | OR | Category | Verdict |
        |---|---|---|
        | Unit and integration tests | Testing | Met |
        | Service dashboard | Dashboards | Partial |
        | Backups and restore | Databases | N/A |
        | Structured logging | Logging | Met |
        | Alerting on SLO burn | Monitoring | Not Met |
        | Documented runbook | Documentation | Unverifiable from repo |
        ... (10 categories)

        Two worth flagging before I write this up:

        - "Backups" is N/A, not a failure — no DB driver, connection string,
          or migrations folder anywhere in search-api/. It reads Postgres via
          indexer's API rather than owning storage.
        - "Documented runbook" is Unverifiable rather than Not Met — README
          links to a Confluence runbook I can't reach from here. It may well
          exist and be fine; I just can't confirm it from the repo.

        Write this to search-api/OPERATIONAL_REQUIREMENTS_AUDIT.md?
        (No existing report of that name there.)

You: Yes, but the runbook does exist — mark it Met.

Claude: I'll record Met with your confirmation as the evidence, noting the
        report couldn't verify it from the repo itself — so a later re-audit
        doesn't silently downgrade it again and puzzle whoever reads it.
        [writes the report]
```

## Example: a single-OR question

```
You: Does this service meet the backups OR?

Claude: [invokes operational-requirements-audit — narrow scope, so it reads
         only that requirement and investigates only storage]

        Partial. The OR asks for backups *and* a tested restore path.

        - Evidence: `infra/rds.tf` — automated snapshots enabled, 7-day
          retention, so backups themselves are covered.
        - Evidence: no restore runbook, restore script, or restore test
          anywhere in the repo — searched infra/, scripts/, docs/, and CI.

        The gap is the restore half: an untested restore isn't a backup yet.
        Nothing written to disk for a single-OR answer — say the word if you
        want it as a file.
```

## Keeping the ORs current

The bundled reference is a snapshot, not a live feed. When Findmypast's Discourse ORs change,
re-save the affected topics as HTML into a folder ("Save Page As"). Only the first post matters.
Later replies are discussion. Then run:

```
python scripts/extract_ors.py <path_to_html_export_folder> references/operational-requirements.md
```

This regenerates the whole file deterministically from the HTML. No manual merge. The script warns
on stderr if it cannot find a page's first post. That usually means the page was only partly
saved: the `_files` asset folder exists but the `.html` file itself does not.
