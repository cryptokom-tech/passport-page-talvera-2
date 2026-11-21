#!/usr/bin/env python3
"""Entry for make.fun bounty the-passport-page-of-a-countr-2-20261121-0318.

Writes the bundled invented passport spread to /output/entry.png.

The image is the Republic of Talvera passport spread: a data page with an
engraved profile portrait of Mara Ilse Selvane (licensed deep-sea fisher,
Port Talvera), bilingual fields and a machine-readable zone with correct
check digits; and a visa page with a Korvath visa sticker, entry/exit
stamps from three neighbouring countries, and the harbourmaster condition
stamp. Every date agrees (issued 14 JAN 2025, travel FEB-MAY 2025, home
03 MAY 2025) and the 40-taler fee matches the visa and the fee stamp.

Standard library only. No network. The program copies the bundled PNG
byte for byte after verifying it, so both grading runs write identical
bytes.
"""

import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_bundled_png():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    if not os.path.isfile(path):
        fail("bundled entry.png not found next to main.py")
    with open(path, "rb") as fh:
        data = fh.read()
    return data


def verify_png(data):
    """Check signature, IHDR dimensions, size cap and IEND trailer."""
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the %d-byte limit"
             % (len(data), MAX_BYTES))
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        fail("entry.png is not a PNG (bad signature)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        fail("entry.png is %dx%d, over the %dx%d limit"
             % (width, height, MAX_DIM, MAX_DIM))
    if width <= 0 or height <= 0:
        fail("entry.png has invalid dimensions %dx%d" % (width, height))
    if data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != b"IEND":
        fail("entry.png is truncated (no IEND chunk)")
    return width, height


def main():
    data = read_bundled_png()
    width, height = verify_png(data)
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        fail("written /output/entry.png does not match the bundle")
    print("wrote /output/entry.png: %dx%d, %d bytes"
          % (width, height, len(data)))


if __name__ == "__main__":
    main()
