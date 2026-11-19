"""Entrypoint for the news-image-20261118 entry (standard library only).

The image is drawn at build time by draw.py and shipped in this repository
as entry.png. This program copies it to the output directory the kit's
environment provides, so both graded runs write byte-identical files.
"""

import hashlib
import os
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(source, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_MAGIC):
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    with open(target, "wb") as fh:
        fh.write(data)
    copied = open(target, "rb").read()
    if len(copied) != len(data) or \
            hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
        print("error: copied file differs from the source", file=sys.stderr)
        return 1
    print("wrote", target, len(copied), "bytes, sha256",
          hashlib.sha256(copied).hexdigest()[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
