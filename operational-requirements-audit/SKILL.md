---
name: operational-requirements-audit
description: Audits a repo/service against Findmypast's Operational Requirements (ORs) — the org-wide standards for testing, dashboards, databases, deployment, developer experience, documentation, logging, monitoring/alerting, resilience, and SLOs — and produces a per-OR compliance report (Met / Partial / Not Met / N/A / Unverifiable from repo) backed by concrete evidence from the codebase. The OR text is bundled with this skill (extracted from Discourse), not re-derived from memory, so verdicts are grounded in the actual current wording. Use this whenever asked to audit, review, or check a service/repo against operational requirements, ORs, "service standards", readiness for production, or similar; also use it when asked about a single specific OR (e.g. "does this service meet the backups OR?") rather than running the full set.
---

# Findmypast Operational Requirements Audit

Findmypast's Operational Requirements (ORs) are org-wide standards every service is expected to
meet — covering testing, dashboards, databases, deployment, developer experience, documentation,
logging/instrumentation, monitoring/alerting, resilience, and SLOs. They're maintained as Discourse
topics; this skill carries a point-in-time export of them in `references/operational-requirements.md`
so an audit doesn't depend on live access to Discourse or on your own memory of what an OR says
(wording matters — always read the bundled text, don't paraphrase from recollection).

**Hard rules by step, so a review can check none have gone missing.** Scope: rules that fail
*silently* if skipped — where the report would look entirely normal with the rule broken. Crediting
a verdict to the repo's own README instead of verifying it, or quoting a secret value into a
citation, both produce a report that reads fine. Three rows are wait-for-the-user gates. Rules that
fail visibly are deliberately absent — "every verdict cites at least one evidence path" (Step 3)
isn't here, since breaking it yields obviously unsupported verdicts. Reading the bundled OR text
rather than working from memory isn't listed either: it's the premise of the skill, not a rule
inside it. Absence from this table doesn't mean optional.

| Step | Hard rule |
|---|---|
| 1 | If the repo holds more than one independently-deployed service, ask which service(s) are in scope rather than auditing the whole repo as one undifferentiated thing |
| 3 | Treat the repo's own README/TSG/docs as claims, not proof — verify against actual config/code before crediting a verdict to them |
| 3 | Never quote a secret/credential value into an evidence citation — cite the file/line/key instead |
| 4 | For a narrow, single-OR question, answer conversationally by default; only write the report file for a full (or explicitly multi-OR) audit, or if asked |
| 4 | Show the summary table and wait for confirmation before writing the report file |
| 4 | If a report file of the same name already exists, say so explicitly before overwriting it |

*Update this table in the same edit whenever a hard rule is added, removed, or moved.*

## Step 1: Confirm scope

Work out which repo/service is being audited (current working directory if that's clearly what's
meant, git repo or not; otherwise ask) and whether the user wants a full audit (all ORs) or just a
subset (e.g. "just check the database ORs" or "does this meet the backups requirement?"). For a
partial request, only investigate and report on the ORs actually asked about — don't pad the report
with the rest, and don't force a written report file for a single quick question (see Step 4).

If the repo is a monorepo holding several independently-deployed services (common in Findmypast
repos — check for multiple deployment manifests, separate `Dockerfile`s, or a services/apps-style
top-level layout), ORs apply per-service, not per-repo: a top-tier-only OR like database failover
might apply to one service and not another in the same checkout. List the discovered services as
a numbered choice and ask which are in scope, rather than guessing or silently auditing everything
as one blob — fold this into the same scope question as full-vs-subset above, one check-in rather
than two. Whatever's chosen, the
eventual report (if one is written) lands at that scope's own root — the repo root for a
whole-repo/single-service repo, or the specific service's subdirectory when scoped to one service
within a monorepo.

**Check for a prior audit first.** If a report from an earlier run already exists at that location
but doesn't match the per-OR table structure in Step 4 (hand-edited, partial, an older format) —
a different failure mode from "no prior report" — don't feed it into the re-verify step as if it
were valid: say what was found and ask whether to re-derive from scratch or attempt to re-verify
it anyway. Otherwise, treat its verdicts as a starting hypothesis, not a rubber stamp — cheaply
re-check whether each cited evidence path still exists and still says what it did, the same
"mechanical check" discipline as re-grounding any stored judgement. Verdicts whose evidence still
holds can be carried forward without re-deriving them from scratch; anything whose evidence has
moved, changed, or disappeared
needs a fresh look. This keeps repeat audits fast and consistent instead of silently drifting from
run to run — but only applies when a prior report is actually found; don't go looking for one that
isn't there, and always do a full fresh investigation if the user explicitly asks for one.

## Step 2: Read the bundled ORs

Read `references/operational-requirements.md` in full before auditing anything. It's organized by
category, each entry carrying the requirement's own text (first-post-only — Discourse reply/
discussion content is intentionally excluded, since that's debate, not the requirement itself).
Treat this file as the source of truth for wording; don't rely on background knowledge of what an
OR "generally" says, since requirements get refined over time and the specific phrasing (e.g.
"only *if* your service uses a database", "*if* top-tier service") drives whether something is
even applicable.

**Check the file's actual age before relying on it** — don't lean on "if it looks out of date" as
the only signal, that's a soft heuristic easy to skip past. Run `git log -1 --format=%ai --
references/operational-requirements.md` (from this skill's own install directory) once per audit;
if it's been more than ~12 months since the last extraction, say so explicitly alongside the
report as a caveat on every verdict, rather than silently trusting text that's plausibly stale —
this is a cheap, mechanical check, not a judgment call, so it costs nothing to run every time. If
the audit *also* surfaces something that reads as out of date relative to current Findmypast
practice, say that too; see "Keeping the ORs current" below.

## Step 3: Investigate each OR with real evidence

For every OR in scope, actually search the target repo — don't guess from the OR title alone. Each
verdict needs at least one concrete piece of evidence (a file path, a CI job name, a config key) or
it isn't a verdict yet, it's a guess.

**Applicability first.** Several ORs are conditional ("if your service uses a database", "if
top-tier service"). Check the precondition before investigating compliance — e.g. glance for a
database driver/connection string/ORM/migrations folder before auditing any Database OR. If the
precondition doesn't hold, the verdict is **N/A**, with a one-line reason citing what you checked
(e.g. "no DB driver, connection string, or migrations folder found in `src/`").

**Where to look**, as a starting point (not exhaustive — follow what the repo actually contains):

| Category | Typical evidence locations |
|---|---|
| Automated Testing | test directories, CI pipeline config (build/deploy steps that run tests and fail the build), feature files (`.feature`) for BDD/Gherkin |
| Dashboards | a `grafana/`, `dashboards/`, or `monitoring/` folder; dashboard JSON/config committed to the repo; SLO doc referencing a dashboard link |
| Databases | migration tooling/config, CI steps invoking migrations, ORM setup, backup/restore docs in a TSG, HA/replica config |
| Deployment and Release | CI/CD pipeline definition (Teamcity/GitHub Actions/etc config), Helm/deployment manifests, feature-flag/LaunchDarkly usage in code and README |
| Developer Experience | README "getting started"/local dev section, `docker-compose.yml`, `.vscode/launch.json` or similar debug config, setup scripts |
| Documentation | `README.md`, a TSG/troubleshooting doc, `docs/` folder |
| Logging and Instrumentation | logging library setup, structured/JSON log config, Prometheus metrics instrumentation, tracing header propagation, Istio sidecar annotation in deployment manifests |
| Monitoring and Alerting | Prometheus alert rule files, health/liveness probe config in deployment manifests, `/health` or `/_health` style endpoints in code |
| Resilience and Stability | replica count / HPA config in deployment manifests, circuit-breaker or retry logic, Istio fault-injection test setup |
| Service Level Objectives | an `SLO.md` or equivalent, dashboards/alerts that reference defined thresholds |

**Depth over speed.** This is a "deep per-OR investigation" audit, not a keyword-existence check —
grep for evidence, then open the actual file to confirm it does what the OR requires (e.g. finding
a `dashboards/` folder isn't enough; check it actually renders the business metrics the OR asks
for). For a large/monorepo target where this would mean auditing many independent services,
consider parallelizing the investigation with the Explore agent (one per category or per service),
then synthesize their findings yourself into the single report in Step 4 — don't let subagents
write the report directly, since the verdicts need to be reconciled against the exact OR wording
you read in Step 2.

**Claims aren't proof.** A README or TSG that *asserts* compliance ("we have automated backups",
"critical alerts page on-call") isn't itself evidence — it's the repo's own claim about itself, and
claims get verified, not credited at face value. Look for the actual mechanism the prose describes
(the CI step, the alert rule, the config) before crediting a verdict to it. If the docs claim
something the code doesn't back up, that's a finding worth surfacing on its own (the docs are
stale, or the claim was never true) — don't quietly resolve it either direction.

**Assign one of five verdicts per OR:**
- **Met** — clear evidence the requirement is satisfied.
- **Partial** — some evidence, but a real gap (e.g. unit tests exist and run in CI, but nothing
  stops the pipeline on failure).
- **Not Met** — investigated, found no evidence.
- **N/A** — precondition doesn't hold; say what you checked to establish that.
- **Unverifiable from repo** — a real, distinct outcome, not a fallback for "didn't look hard
  enough." A number of ORs describe things that live entirely outside version control — a Grafana
  dashboard's actual content, whether a VictorOps/Slack alert really pages someone, whether Spanners
  actually runs a quarterly restore test, whether the ops team's centralized DB backups actually
  cover this service. If the repo has no artifact that could confirm or deny it either way, say
  that plainly and name what would need checking outside the repo (a Grafana link, an ops-team
  contact, a PagerDuty/VictorOps config) rather than forcing it into Not Met — collapsing "couldn't
  check" into "failed" makes the report actively misleading, not just incomplete.

If you're genuinely unsure whether something clears the bar (e.g. a TSG exists but you can't judge
whether an outside engineer could follow it), say so as a caveat on the verdict rather than forcing
a confident Met/Not Met — a false-confident audit is worse than a flagged uncertainty.

**Never quote a secret into an evidence citation.** If the evidence for a verdict happens to be a
config file that also contains a credential, connection string, or token, cite the file/line/key
that establishes the verdict (e.g. "`config/database.yml:12` — connection string configured") and
leave the actual secret value out of the report entirely.

## Step 4: Report the findings

**A single narrow question doesn't need a file.** If Step 1 established the ask was about one OR
(or a couple), just answer conversationally — verdict, reasoning, evidence — the same rigor as
below, just not packaged as a standing report. Offer to write it to a file if the user wants a
persistent record, but don't create one unasked; a one-line answer buried in a new file is more
friction than help. Skip the rest of this step in that case.

For a full (or explicitly multi-OR) audit: once every OR in scope has a verdict, show the summary
table (below) in the conversation and wait for confirmation before writing anything to disk — the
verdicts are judgment calls, and it's cheap to let the user flag a disagreement or an OR you
misjudged before it's committed to a file. If a report file of the same name already exists at the
target location, say so explicitly as part of that same message (one check-in, not two) rather than
raising it separately.

Once confirmed, write `OPERATIONAL_REQUIREMENTS_AUDIT.md` at the audited scope's root (see Step 1
for repo-root vs. service-subdirectory), using this structure:

```markdown
# Operational Requirements Audit — <repo/service name>

Generated: <YYYY-MM-DD>
Scope: <all ORs | the specific subset audited>

## Summary

| OR | Category | Verdict |
|---|---|---|
| <requirement title> | <category> | Met / Partial / Not Met / N/A / Unverifiable from repo |
...

## Details

### <category>

#### <requirement title> — <Verdict>
<1-3 sentence reasoning>
- Evidence: `<path>` — <what it shows>
- Evidence: `<path>` — <what it shows>
```

Keep the per-OR reasoning tight — the evidence bullets carry the weight, the prose just explains
what they mean for this verdict. Group details by category in the same order as the reference file
so the report is easy to cross-check against it.

## Keeping the ORs current

`references/operational-requirements.md` is a snapshot, not a live feed — Findmypast's Discourse
ORs can change (new requirements added, wording refined) after this was extracted. If asked to
refresh it, or if you have reason to think it's stale: re-export the relevant Discourse topics as
HTML ("Save Page As", first post is what matters) into a folder, then run

```
python scripts/extract_ors.py <path_to_html_export_folder> references/operational-requirements.md
```

This regenerates the bundled reference from scratch — it's deterministic and re-derives everything
from the HTML, so there's no manual merge step. Sanity-check the diff before treating it as final:
the script warns on stderr if a page's first post couldn't be found (usually means the page was
only partially saved — the `_files` asset folder exists but the `.html` itself is missing).
