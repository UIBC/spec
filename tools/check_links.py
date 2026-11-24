#!/usr/bin/env python3
"""Relative-link check for this repository, offline by design.

Every reviewer complaint about a spec starts the same way: the link they
followed went nowhere. This checks the one class of link that can be checked
deterministically - relative links between files in this repository - and
deliberately leaves external URLs alone: a check that depends on somebody
else's server turns red for reasons that have nothing to do with the spec.

Run: `python tools/check_links.py` (exit 0 clean, 1 on any broken link).
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Markdown inline links and images: [text](target) and ![alt](target)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
# Reference definitions: [id]: target
REF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


def markdown_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames.sort()
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for name in sorted(filenames):
            if name.endswith((".md", ".markdown")):
                out.append(os.path.join(dirpath, name))
    return out


def is_external(target):
    return target.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:"))


def main():
    problems = []
    checked = 0
    files = markdown_files()

    for path in files:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        text = FENCE_RE.sub("", text)  # do not read code blocks as prose
        for match in list(LINK_RE.finditer(text)) + list(REF_RE.finditer(text)):
            target = match.group(1).strip()
            if is_external(target):
                continue
            checked += 1
            anchor = target.split("#", 1)[0]
            if not anchor:
                continue
            rel = anchor.replace("%20", " ")
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), rel))
            if not os.path.exists(resolved):
                line = text[: match.start()].count("\n") + 1
                problems.append(
                    f"{os.path.relpath(path, ROOT)}:{line}: target not in this repository: {target}"
                )

    if problems:
        print("LINKS FAIL")
        for p in problems:
            print("  - " + p)
        return 1

    print(f"LINKS OK - {len(files)} markdown files, {checked} relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
