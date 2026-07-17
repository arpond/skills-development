#!/usr/bin/env python3
"""Extract Findmypast Operational Requirement text from saved Discourse HTML pages.

Each OR is a single Discourse topic saved as HTML (via "Save Page As"). The
requirement definition is the topic's FIRST post only -- later posts are
discussion/replies and must be ignored. This script pulls the <title> and the
first <div class="cooked">...</div> (using a depth-tracking parser, since the
post body can contain its own nested <div> elements) and renders the post body
as plain-ish markdown.

Usage:
    python extract_ors.py <input_dir> <output_file.md>

Re-run this whenever the OR export in <input_dir> is refreshed, then re-bundle
the skill with the regenerated output file.
"""
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class TitleAndCookedExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""

        self.cooked_depth = None  # None until we've entered the first cooked div
        self.div_depth = 0
        self.cooked_done = False
        self.cooked_parts = []
        self.href_stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True

        if tag == "div":
            self.div_depth += 1
            if (
                self.cooked_depth is None
                and not self.cooked_done
                and "cooked" in (attrs.get("class") or "").split()
            ):
                self.cooked_depth = self.div_depth
                return  # don't emit the wrapper div itself

        if self.cooked_depth is not None:
            self._emit_start(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

        if self.cooked_depth is not None and tag == "div" and self.div_depth == self.cooked_depth:
            self.cooked_depth = None
            self.cooked_done = True
            self.div_depth -= 1
            return

        if self.cooked_depth is not None:
            self._emit_end(tag)

        if tag == "div":
            self.div_depth -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.cooked_depth is not None:
            self.cooked_parts.append(data)

    def _emit_start(self, tag, attrs):
        if tag == "li":
            self.cooked_parts.append("\n- ")
        elif tag in ("p", "ul", "ol", "br"):
            self.cooked_parts.append("\n")
        elif tag == "strong" or tag == "b":
            self.cooked_parts.append("**")
        elif tag == "em" or tag == "i":
            self.cooked_parts.append("_")
        elif tag == "code":
            self.cooked_parts.append("`")
        elif tag == "a":
            href = attrs.get("href") or ""
            self.href_stack.append(href)
            if href:
                self.cooked_parts.append("[")
        elif tag == "h1" or tag == "h2" or tag == "h3":
            self.cooked_parts.append("\n### ")

    def _emit_end(self, tag):
        if tag in ("p", "ul", "ol", "li"):
            self.cooked_parts.append("\n")
        elif tag == "strong" or tag == "b":
            self.cooked_parts.append("**")
        elif tag == "em" or tag == "i":
            self.cooked_parts.append("_")
        elif tag == "code":
            self.cooked_parts.append("`")
        elif tag == "a":
            href = self.href_stack.pop() if self.href_stack else ""
            if href:
                self.cooked_parts.append(f"]({href})")

    def get_cooked_text(self):
        raw = "".join(self.cooked_parts)
        raw = html.unescape(raw)
        # collapse runs of blank lines/whitespace left over from tag stripping
        raw = re.sub(r"[ \t]+\n", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def category_and_requirement(stem: str):
    # Filenames look like:
    # "<Category>_ <Requirement> - Engineering _ Service OR - Findmypast"
    stem = stem
    stem = re.sub(r"\s*-\s*Engineering\s*_\s*Service OR\s*-\s*Findmypast$", "", stem)
    if "_ " in stem:
        category, requirement = stem.split("_ ", 1)
    else:
        # A handful of OR pages have no "<Category>_ " prefix in their filename
        # (the requirement title stands alone). Categorize by hand here rather
        # than inventing a noisy "Uncategorized" bucket.
        category, requirement = "Service Level Objectives", stem

    category = category.strip()
    # Filenames are inconsistently cased (e.g. "Developer experience" vs.
    # "Developer Experience") -- normalize word-by-word so they don't split
    # into two sections in the output. Small words stay lowercase (unless
    # they're the first word) to match the house style ("... and Release").
    lowercase_words = {"and", "of", "the"}
    words = category.split(" ")
    category = " ".join(
        w if (i > 0 and w.lower() in lowercase_words) else w[:1].upper() + w[1:].lower()
        for i, w in enumerate(words)
    )
    return category, requirement.strip()


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    entries = []
    for path in sorted(input_dir.glob("*.html")):
        parser = TitleAndCookedExtractor()
        text = path.read_text(encoding="utf-8", errors="replace")
        parser.feed(text)

        category, requirement = category_and_requirement(path.stem)
        body = parser.get_cooked_text()
        if not body:
            print(f"WARNING: no cooked body found in {path.name}", file=sys.stderr)
        entries.append((category, requirement, body, path.name))

    entries.sort(key=lambda e: (e[0], e[1]))

    lines = [
        "# Findmypast Operational Requirements (bundled reference)",
        "",
        f"Extracted from {len(entries)} OR pages exported from Discourse. Each entry below is the",
        "FIRST post of the OR's Discourse thread only (the requirement definition) -- later",
        "discussion/replies in the original thread are intentionally omitted.",
        "",
        "Regenerate with `python scripts/extract_ors.py <ors_dir> references/operational-requirements.md`",
        "when the source OR export is refreshed.",
        "",
    ]

    current_category = None
    for category, requirement, body, source_file in entries:
        if category != current_category:
            lines.append(f"\n## {category}\n")
            current_category = category
        lines.append(f"### {requirement}")
        lines.append(f"<!-- source: {source_file} -->")
        lines.append("")
        lines.append(body if body else "_(no body extracted -- check source file manually)_")
        lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(entries)} ORs to {output_file}")


if __name__ == "__main__":
    main()
