"""Compute the per-skill facts CONVENTIONS.md's censuses describe, and print every
census line that names a skill beside them. Facts, not verdicts: diff the two halves
by reading, the same contract as check-vocabulary.py and check-hard-rules.py."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).parent


def read(path):
    return path.read_text(encoding="utf-8")


def skill_facts(skill_dir):
    text = read(skill_dir / "SKILL.md")
    readme = skill_dir / "README.md"
    readme_text = read(readme) if readme.exists() else ""
    all_text = "".join(read(p) for p in skill_dir.glob("*.md"))
    return {
        "hard-rules table + update line": "Update this table" in text,
        "numbered-choices copy": "number them" in text,
        "README ## Cost": bool(re.search(r"^## Cost\b", readme_text, re.M)),
        "version line": "**Skill version:" in text,
        "changelog.md": (skill_dir / "changelog.md").exists(),
        "counter shape": ("reset to 0" in all_text or "force-reset" in all_text),
        "config paths": sorted(set(re.findall(r"~/\.claude/[\w.-]+\.md", text))),
    }


def main():
    skills = sorted(p.parent for p in ROOT.glob("*/SKILL.md"))
    names = [s.name for s in skills]

    print("== Computed facts, one row per skill ==")
    for s in skills:
        f = skill_facts(s)
        flags = ", ".join(k for k, v in f.items() if v is True)
        missing = ", ".join(k for k, v in f.items() if v is False)
        print(f"{s.name}")
        print(f"  has:     {flags or '-'}")
        print(f"  lacks:   {missing or '-'}")
        print(f"  configs: {', '.join(f['config paths']) or '-'}")

    print()
    print("== CONVENTIONS.md lines naming a skill, by section ==")
    section = "(top)"
    conventions = read(ROOT / "CONVENTIONS.md")
    for lineno, line in enumerate(conventions.splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if any(f"`{n}`" in line for n in names):
            print(f"{lineno:4} [{section}] {line.strip()}")

    print()
    print("Read the two halves against each other. A census line asserting something")
    print("the facts above contradict is the finding. The script passes no verdicts.")


if __name__ == "__main__":
    main()
