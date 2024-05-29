#!/usr/bin/env python3
# Copyright 2024 Chorus One, licensed CC BY-NC-SA 4.0.
"""
export_checklist.py -- Export all recommendations as Markdown checklist.
"""

from typing import Iterable

import os


def list_md_files() -> Iterable[str]:
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".md"):
                yield os.path.join(root, file)


def main() -> None:
    for f in list_md_files():
        print(f)


if __name__ == "__main__":
    main()
