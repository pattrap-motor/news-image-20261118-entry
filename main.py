#!/usr/bin/env python3
"""Entry program: copy the bundled entry.png to the output directory.

Standard library only, no network, deterministic: both runs write the
same bytes, because the file is copied byte for byte. The image itself
is drawn by draw.py (run it first to regenerate entry.png).
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
    sys.exit(0)
