#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261124 bounty.

The finished front-page image ships in this repository as entry.png,
beside this file. The program runs offline with the standard library
only and copies that image to the output directory as entry.png.

In the grader's container the output directory is /output; outside it,
the MAKEFUN_OUTPUT_DIR environment variable stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
