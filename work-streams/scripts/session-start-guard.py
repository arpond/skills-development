"""SessionStart guard for the work-streams skill.

Registered as a Claude Code SessionStart hook. Prints one line naming the active
streams for the current repo, which the harness injects as session context — or
prints nothing when there is nothing to say. Deterministic and best-effort: any
missing or unreadable piece means silence, never an error. The skill itself owns
all real handling (malformed files, strays, mismatches) when it is invoked.

The config path honours WORK_STREAMS_CONFIG so tests and sandboxes can redirect
it away from the real home directory.
"""

import json
import os
import re
import sys


def frontmatter(path):
    """First frontmatter block of a manifest, or '' on any problem."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(4096)
    except OSError:
        return ""
    parts = head.split("---")
    return parts[1] if len(parts) >= 2 else ""


def main():
    cfg_path = os.environ.get("WORK_STREAMS_CONFIG") or os.path.expanduser(
        "~/.claude/work-streams-config.md"
    )
    try:
        with open(cfg_path, encoding="utf-8") as f:
            cfg = f.read()
    except OSError:
        return
    m = re.search(r"^base:\s*(.+?)\s*$", cfg, re.M)
    if not m:
        return
    base = os.path.expanduser(m.group(1))
    if not os.path.isdir(base):
        return

    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    cwd = payload.get("cwd") or os.getcwd()
    slug = os.path.basename(os.path.normpath(cwd)).lower()
    cwd_key = os.path.normcase(os.path.realpath(cwd))

    found = []
    try:
        projects = os.listdir(base)
    except OSError:
        return
    for proj in projects:
        proj_dir = os.path.join(base, proj)
        if not os.path.isdir(proj_dir):
            continue
        try:
            streams = os.listdir(proj_dir)
        except OSError:
            continue
        for stream in streams:
            if stream == "archive":
                continue
            manifest = os.path.join(proj_dir, stream, "stream.md")
            if not os.path.isfile(manifest):
                continue
            fm = frontmatter(manifest)
            repo_lines = re.findall(r"^\s*-\s*(.+?)\s*$", fm, re.M)
            repos_match = any(
                os.path.normcase(os.path.realpath(os.path.expanduser(r))) == cwd_key
                for r in repo_lines
            )
            if not (repos_match or proj == slug):
                continue
            updated = re.search(r"^updated:\s*(\S+)", fm, re.M)
            found.append((updated.group(1) if updated else "?", stream))

    if not found:
        return
    found.sort(reverse=True)
    shown = ", ".join(f"{name} (updated {date})" for date, name in found[:5])
    more = f" and {len(found) - 5} more" if len(found) > 5 else ""
    print(
        f"work-streams: active stream(s) for this repo: {shown}{more}. "
        "Offer to resume one, or to wrap up if the last session here did not."
    )


if __name__ == "__main__":
    main()
