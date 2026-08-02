# operational-requirements-audit

Audits a repo/service against Findmypast's Operational Requirements (ORs) — org-wide standards
covering testing, dashboards, databases, deployment, developer experience, documentation,
logging/instrumentation, monitoring/alerting, resilience, and SLOs — and produces a per-OR
compliance report (Met / Partial / Not Met / N/A / Unverifiable from repo) backed by concrete
evidence from the codebase.

The OR text itself is bundled with the skill (`references/operational-requirements.md`), extracted
from Discourse pages saved as HTML, rather than re-derived from memory each time — wording matters,
and requirements get refined over time, so the audit reads the actual current text instead of
guessing from a requirement's title.

Files:
- `SKILL.md` — the audit workflow: confirm scope, read the bundled ORs, investigate each one with
  real evidence (grep/read the repo, not keyword guessing), then write a structured report.
- `references/operational-requirements.md` — the bundled OR text, one entry per requirement, grouped
  by category. Regenerate with `scripts/extract_ors.py` when the source Discourse export refreshes.
- `scripts/extract_ors.py` — parses a folder of Discourse pages saved as HTML (one OR per page) and
  extracts each page's title and first post (the requirement definition — later Discourse replies
  are discussion, not part of the requirement, and are intentionally excluded) into the bundled
  reference file.

## What it writes

- **`OPERATIONAL_REQUIREMENTS_AUDIT.md`** — the report, at the root of whatever was audited: the
  repo root, or a service subdirectory if the repo holds several independently-deployed services
  and you scoped the audit to one.

**Only for a full or explicitly multi-OR audit, or if you ask.** A narrow "does this service meet
the backups OR?" is answered in the conversation and writes nothing. The summary table is shown and
confirmed before the file is written, and if a report of the same name already exists you're told
so in that same message rather than finding out afterwards.

Nothing else is written — no changes to the audited code, and nothing outside the repo.

## Requires

Nothing beyond local file read/search (Read/Grep/Glob) to investigate the target repo. Refreshing
the bundled ORs requires Python 3 (standard library only, no extra packages) and a fresh HTML export
from Discourse.

## When it triggers

- "Audit this repo against the operational requirements."
- "Does this service meet the ORs?"
- "Check whether this meets the backups OR." (a single-OR request — only that one gets investigated
  and reported on)
- "Is this service production-ready per Findmypast's service standards?"

## Keeping the ORs current

The bundled reference is a snapshot, not a live feed. When Findmypast's Discourse ORs change, re-save
the affected topics as HTML ("Save Page As" — only the first post matters, later replies are
discussion) into a folder, then run:

```
python scripts/extract_ors.py <path_to_html_export_folder> references/operational-requirements.md
```

This regenerates the whole file deterministically from the HTML — no manual merging. The script
warns on stderr if a page's first post couldn't be found, which usually means the page was only
partially saved (the `_files` asset folder exists but the `.html` file itself doesn't).
