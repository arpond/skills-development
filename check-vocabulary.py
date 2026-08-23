# -*- coding: utf-8 -*-
"""Grep every banned name in CONVENTIONS.md's Vocabulary table across the repo.

This is the mechanical half of CLAUDE.md's review-loop check 2, third test:
a concept named by a word in the table's right-hand column should use the
left-hand one. The table is the only source of names. The script reads it
fresh on every run and refuses to run if it cannot parse it, so a reformatted
row fails loudly instead of silently checking nothing.

Usage: python check-vocabulary.py [path ...]   (default: every tracked .md)

What it skips, per the spec's own exemptions:
- fenced code blocks (example dialogue quotes how Claude speaks)
- ste-writing/ (vendored, keeps upstream wording)
- CHANGELOG.md (a rename record legitimately names the old word)
- the Vocabulary table itself

Matching runs on unwrapped paragraphs, so a name split across a hard wrap
still hits; the line reported is where the paragraph starts. A banned name
with a parenthetical condition is still searched and each hit shows the
condition, since the script cannot apply it. The one exception is a condition
of the form "outside `dir`", which it applies by skipping that directory. A
name that is also a canonical term, or a substring of one (gate, rule,
companion file), is not searched: every hit would be the canonical use. Treat
the output as a locator, not a verdict. Pass the changed files during a
review; a whole-repo run puts common words over the floor.
"""
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(ROOT, "CONVENTIONS.md")
FLOOR = 20          # more hits than this: report the count, not the lines
SKIP_DIRS = ("ste-writing",)
SKIP_FILES = ("CHANGELOG.md",)


def fail(msg):
    print(f"check-vocabulary: {msg}", file=sys.stderr)
    sys.exit(2)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_table(text):
    """Return (terms, banned) from the Vocabulary table, or fail loudly."""
    m = re.search(r"^## Vocabulary\s*$(.*?)^## ", text, re.M | re.S)
    if not m:
        fail("no '## Vocabulary' section in CONVENTIONS.md")
    section = m.group(1)
    rows = [l for l in section.splitlines() if l.startswith("|")]
    if len(rows) < 3 or not re.match(r"\|\s*Term\s*\|\s*Means\s*\|\s*Not\s*\|", rows[0]):
        fail("Vocabulary table header is not '| Term | Means | Not |'")
    terms, banned = [], []
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) != 3:
            fail(f"row does not have three cells: {row.strip()[:60]}")
        term, _, notcol = cells
        terms.append(term)
        notcol = notcol.split("Exempt:")[0]        # exemptions are prose, not names
        for item in notcol.split(","):
            item = item.strip().strip("`").rstrip(".;")
            if not item or item.startswith("—") or item.startswith("-"):
                continue
            cond = ""
            pm = re.match(r"(.*?)\s*\((.*)\)\s*$", item)
            if pm:
                item, cond = pm.group(1).strip().strip("`"), pm.group(2).strip()
            if item:
                banned.append((item, term, cond))
    if not terms:
        fail("Vocabulary table has no rows")
    return terms, banned


def strip_table(text):
    return re.sub(r"^## Vocabulary\s*$.*?^## ", "## ", text, flags=re.M | re.S)


def strip_fences(text):
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def paragraphs(text):
    """Yield (start_line, unwrapped_text) per blank-line-separated block."""
    start, buf = None, []
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip():
            if start is None:
                start = i
            buf.append(line.strip())
        elif buf:
            yield start, " ".join(buf)
            start, buf = None, []
    if buf:
        yield start, " ".join(buf)


def tracked_md():
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        fail("git ls-files failed; pass paths explicitly")
    return [l.strip() for l in out.stdout.splitlines() if l.strip()]


def main(argv):
    spec_text = read(SPEC)
    terms, banned = parse_table(spec_text)
    canon = [t.lower() for t in terms]

    paths = argv or tracked_md()
    files = []
    for p in paths:
        rel = os.path.relpath(os.path.join(ROOT, p), ROOT).replace("\\", "/")
        if rel.split("/")[0] in SKIP_DIRS or os.path.basename(rel) in SKIP_FILES:
            continue
        text = read(os.path.join(ROOT, rel))
        if rel == "CONVENTIONS.md":
            text = strip_table(text)
        files.append((rel, list(paragraphs(strip_fences(text)))))

    total = 0
    for name, term, cond in banned:
        low = name.lower()
        overlap = [c for c in canon if (low == c and not re.match(r"outside\s", cond)) or (low != c and low in c)]
        if overlap:
            print(f"-- {name!r} (for {term}): not searched, overlaps canonical {overlap[0]!r}"
                  + (f"; condition: {cond}" if cond else ""))
            continue
        pat = re.compile(r"(?<![\w-])" + re.escape(name).replace(r"\ ", r"[\s-]+") + r"s?(?![\w-])", re.I)
        om = re.match(r"outside\s+`?([\w-]+)`?$", cond)
        skip_dir = om.group(1) if om else None
        hits = [(rel, i, para) for rel, paras in files
                if not (skip_dir and rel.split("/")[0] == skip_dir)
                for i, para in paras if pat.search(para)]
        label = f"{name!r} -> use {term!r}" + (f"  [condition: {cond}]" if cond else "")
        if not hits:
            print(f"ok {label}")
            continue
        total += len(hits)
        if len(hits) > FLOOR:
            print(f"?? {label}: {len(hits)} hits, above the floor of {FLOOR}; too common to list, needs judgement")
            continue
        print(f"!! {label}: {len(hits)} hit(s)")
        for rel, i, line in hits:
            print(f"     {rel}:{i}: {pat.sub(lambda m: m.group(0).upper(), line.strip())[:110]}")
    print(f"== {len(banned)} banned names from {len(terms)} terms, {len(files)} files, {total} hits to read")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
