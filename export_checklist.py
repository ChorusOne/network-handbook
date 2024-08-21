#!/usr/bin/env python3
# Copyright 2024 Chorus One, licensed CC BY-NC-SA 4.0.
"""
export_checklist.py -- Export all recommendations as Markdown checklist.
"""

from collections import defaultdict
from typing import Dict, Iterable, List, NamedTuple, Optional

import textwrap
import os
import sys


class Recommendation(NamedTuple):
    chapter: str
    file: str
    id: str
    priority: int
    title: str

    def get_url(self) -> str:
        slug = self.file.removeprefix("src/").removesuffix(".md")
        return f"https://handbook.chorus.one/{slug}.html#{self.id}"


def list_md_files() -> Iterable[str]:
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".md"):
                yield os.path.join(root, file)


def list_recommendations(fname: str) -> Iterable[Recommendation]:
    chapter: Optional[str] = None

    with open(fname, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.startswith("# "):
                chapter = line[2:].strip()

            if line.startswith("#### "):
                try:
                    # Recommendation lines are of the form `#### Title {.prio # #id}\n".
                    title = line.removeprefix("#### ")
                    title, meta = title.rsplit("{", maxsplit=1)
                    meta = meta.strip().removesuffix("}")
                    prio_str, id_str = meta.split(" ", maxsplit=1)
                    assert prio_str.startswith(
                        ".p"
                    ), "Recommendation line must end in `{.pN #id}`."
                    assert id_str.startswith(
                        "#"
                    ), "Recommendation line must end in `{.pN #id}`."
                    assert chapter is not None, "Must have # chapter title before ####."

                    yield Recommendation(
                        chapter=chapter,
                        file=fname,
                        id=id_str[1:],
                        priority=int(prio_str[2:]),
                        title=title.strip(),
                    )

                except Exception as exc:
                    print(f"Error in {fname} at line {i + 1}:", file=sys.stderr)
                    print(f"{i + 1} | {line}", end="", file=sys.stderr)
                    print(f"Error: {exc}", file=sys.stderr)
                    sys.exit(1)


def main() -> None:
    by_priority: Dict[int, List[Recommendation]] = defaultdict(lambda: [])
    out_fname = "checklist.md"

    for fname in sorted(list_md_files()):
        # In the intro we list the priority categories, they are not themselves
        # recommendations.
        if fname == "src/node-software/intro.md":
            continue

        for rec in list_recommendations(fname):
            by_priority[rec.priority].append(rec)

    with open(out_fname, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(
            """
            # Checklist

            This checklist summarizes the recommendations in all the chapters.
            The main purpose of this page is to have a markdown checklist that
            we can copy into an issue for internal due diligence processes. It
            is not part of the book itself. Rebuild with `export_checklist.py`.
            """
        ).strip())
        f.write("\n\n")

        for priority, recommendations in sorted(by_priority.items()):
            f.write(f"## P{priority}\n")

            chapter = ""
            for rec in recommendations:
                if rec.chapter != chapter:
                    f.write(f"\n#### {rec.chapter}\n")
                    chapter = rec.chapter

                f.write(f" - [ ] [{rec.title}]({rec.get_url()})\n")

            f.write("\n")

    print(f"Checklist written to {out_fname}.")


if __name__ == "__main__":
    main()
