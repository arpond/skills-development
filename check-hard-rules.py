"""For every hard-rules table row in every skill, find the prose sentence that
states it and report whether that sentence fits the 25-word cap.

This is the mechanical half of CLAUDE.md's review-loop check 2: the principle
"A rule is a sentence" scopes its cap to the sentence a reader would copy into
a hard-rules table, so each table row should have exactly such a sentence in
the prose. A row whose closest sentence is long, or whose closest sentence is
not close at all, is a rule that lives only in the index.

Usage: python check-hard-rules.py [skill-dir ...]   (default: every skill)
Matching is word-overlap, so treat the output as a locator, not a verdict.
"""
import glob
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "ste_lint", os.path.join(ROOT, "ste-writing", "scripts", "ste-lint.py"))
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)

CAP = 25
MIN_OVERLAP = 0.5   # share of the row's content words the sentence must contain
STOP = set("""a an the this that these those of for to in on at by with from as and or but if
when then than not no is are was were be been being am do does did has have had will would can
could may might must should shall it its their your our his her they we you i rather before
after any every each one two into out up own same than about over""".split())
TABLE_HEADERS = ("hard rule", "gate", "confirm", "what gets written")


def content_words(s):
    """Lowercased, stop-words dropped, crudely stemmed (first six letters) so
    "confirm"/"confirmation" and "surface"/"surfacing" match."""
    return {w.lower()[:6] for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", s)
            if len(w) > 3 and w.lower() not in STOP}


def table_rows(text):
    """Rule text of each row in every table whose header names hard rules."""
    rows, in_table = [], False
    for line in text.split("\n"):
        if not line.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not in_table:
            if any(h in line.lower() for h in TABLE_HEADERS):
                in_table = "header"
            continue
        if in_table == "header":
            in_table = True          # the |---| separator line
            continue
        if cells and cells[-1]:
            rows.append(cells[-1])
    return rows


def prose_sentences(skill_dir):
    out = []
    for f in sorted(glob.glob(os.path.join(skill_dir, "**", "*.md"), recursive=True)):
        if os.path.basename(f) == "README.md":
            continue
        text = lint.strip_code(open(f, encoding="utf-8").read(), keep_inline=True)
        for line_no, block in lint.unwrap_blocks(text):
            if block.lstrip().startswith("|"):
                continue
            for s in lint.split_sentences(block):
                out.append((os.path.relpath(f, ROOT), line_no, s, lint.rule_words(s)))
    return out


def check(skill_dir):
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return
    rows = table_rows(open(skill_md, encoding="utf-8").read())
    if not rows:
        return
    sents = prose_sentences(skill_dir)
    print(f"== {os.path.basename(skill_dir)}: {len(rows)} rows")
    flagged = 0
    for row in rows:
        rw = content_words(row)
        best = (0.0, None)
        for f, line_no, s, n in sents:
            sw = content_words(s)
            if not sw:
                continue
            # Overlap coefficient: a short rule sentence shouldn't lose to a
            # row that carries extra qualifiers, nor vice versa.
            score = len(rw & sw) / min(len(rw), len(sw)) if rw else 0.0
            if score > best[0] or (score == best[0] and best[1] and n < best[1][3]):
                best = (score, (f, line_no, s, n))
        score, hit = best
        row_n = lint.rule_words(row)
        problems = []
        if row_n > CAP:
            problems.append(f"row itself {row_n}w")
        if hit is None or score < MIN_OVERLAP:
            problems.append(f"no close sentence (best overlap {score:.2f})")
        elif hit[3] > CAP:
            problems.append(f"closest sentence {hit[3]}w at {hit[0]}:{hit[1]}")
        if problems:
            flagged += 1
            print(f"  FLAG  {row[:90]}")
            for p in problems:
                print(f"        - {p}")
            if hit:
                print(f"        ~ {hit[2][:110]}")
    print(f"   {len(rows) - flagged} ok, {flagged} flagged")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    targets = sys.argv[1:] or sorted(
        d for d in glob.glob(os.path.join(ROOT, "*")) if os.path.isdir(d)
        and os.path.exists(os.path.join(d, "SKILL.md"))
        and os.path.basename(d) != "ste-writing")
    for t in targets:
        check(t)
