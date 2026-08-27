"""Compute the per-skill facts the standards files' censuses describe, and print every
paragraph in CONVENTIONS.md and DESIGN_PHILOSOPHY.md that names a skill. Facts, not
verdicts: diff the two halves by reading, the same contract as check-vocabulary.py and
check-hard-rules.py."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).parent
STANDARDS = ["CONVENTIONS.md", "DESIGN_PHILOSOPHY.md"]
KEBAB = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")


def read(path):
    return path.read_text(encoding="utf-8")


def skill_facts(skill_dir):
    text = read(skill_dir / "SKILL.md")
    readme = skill_dir / "README.md"
    readme_text = read(readme) if readme.exists() else ""
    # rglob so companions in references/ count too; a changelog quoting a phrase can
    # false-positive, which the facts-not-verdicts contract tolerates.
    all_text = "".join(read(p) for p in skill_dir.rglob("*.md")).lower()
    return {
        "hard-rules table + update line": "Update this table" in text,
        "numbered-choices copy": "number them" in text,
        "README present": readme.exists(),
        "README ## Cost": bool(re.search(r"^## Cost\b", readme_text, re.M)),
        "version line": "**Skill version:" in text,
        "changelog.md": (skill_dir / "changelog.md").exists(),
        "counter shape": ("reset to 0" in all_text or "force-reset" in all_text),
        "config paths": sorted(set(re.findall(r"(?:~/)?\.claude/[\w.-]+\.md", text))),
    }


def paragraphs(text):
    """Yield (start_lineno, section, paragraph_text) per blank-line-separated block."""
    section, start, buf = "(top)", None, []
    for lineno, line in enumerate(text.splitlines() + [""], 1):
        if line.startswith("## "):
            section = line[3:].strip()
        if line.strip():
            if start is None:
                start = lineno
            buf.append(line)
        elif buf:
            yield start, section, "\n".join(buf)
            start, buf = None, []


def main():
    skills = sorted(p.parent for p in ROOT.glob("*/SKILL.md"))
    names = {s.name for s in skills}

    print("== Computed facts, one row per skill ==")
    for s in skills:
        f = skill_facts(s)
        flags = ", ".join(k for k, v in f.items() if v is True)
        missing = ", ".join(k for k, v in f.items() if v is False)
        print(f"{s.name}")
        print(f"  has:     {flags or '-'}")
        print(f"  lacks:   {missing or '-'}")
        print(f"  configs: {', '.join(f['config paths']) or '-'}")

    unknown = set()
    for fname in STANDARDS:
        text = read(ROOT / fname)
        unknown |= set(KEBAB.findall(text)) - names
        print()
        print(f"== {fname} paragraphs naming a skill, by section ==")
        for start, section, para in paragraphs(text):
            if any(f"`{n}`" in para for n in names):
                print(f"{start:4} [{section}]")
                for line in para.splitlines():
                    print(f"       {line.strip()}")

    print()
    print("== Backticked kebab names that are not current skill folders ==")
    print("(rename/deletion check - most are ordinary terms, read them, do not count them)")
    print("  " + (", ".join(sorted(unknown)) or "-"))

    print()
    print("Read the halves against each other. A claim the facts contradict is the")
    print("finding. The script passes no verdicts.")


if __name__ == "__main__":
    main()
