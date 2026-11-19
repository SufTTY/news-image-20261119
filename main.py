#!/usr/bin/env python3
import os, shutil
SRC = os.path.join(os.path.dirname(__file__), "entry.png")
def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    if os.path.getsize(dst) > 1048576: raise SystemExit("entry exceeds 1 MiB")
main()
