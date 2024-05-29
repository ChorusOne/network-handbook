#!/usr/bin/env python3
# Copyright 2024 Chorus One, licensed CC BY-NC-SA 4.0.
"""
export_checklist.py -- Export all recommendations as Markdown checklist.
"""

from typing import Iterable, NamedTuple, Optional

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
        return f"https://handbook.chorus.one/{slug}.html#{id}"


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
                    assert prio_str.startswith(".p"), "Recommendation line must end in `{.pN #id}`."
                    assert id_str.startswith("#"), "Recommendation line must end in `{.pN #id}`."
                    assert chapter is not None, "Must have # chapter title before ####."

                    yield Recommendation(
                        chapter=chapter,
                        file=fname,
                        id=id_str[1:],
                        priority=int(prio_str[2:]),
                        title=title.strip(),
                    )

                except Exception as exc:
                    print(f"Error in {fname} at line {i + 1}:")
                    print(f"{i + 1} | {line}", end="")
                    print(f"Error: {exc}")
                    sys.exit(1)


def main() -> None:
    for fname in list_md_files():
        if fname == "src/node-software/intro.md":
            # In the intro we list the priority categories, they are not
            # themselves recommendations.
            continue

        for rec in list_recommendations(fname):
            print(rec)


if __name__ == "__main__":
    main()
