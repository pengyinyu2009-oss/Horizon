#!/usr/bin/env python3
"""Atomically exchange two existing paths on Linux or macOS."""

from __future__ import annotations

import ctypes
import os
import sys
from pathlib import Path

EXCHANGE_FLAG = 2
AT_FDCWD = -100


def atomic_exchange(left: Path, right: Path) -> None:
    if not left.exists() or not right.exists():
        raise FileNotFoundError("both exchange paths must already exist")
    if left.stat().st_dev != right.stat().st_dev:
        raise OSError("atomic exchange requires both paths on the same filesystem")

    libc = ctypes.CDLL(None, use_errno=True)
    left_bytes = os.fsencode(left)
    right_bytes = os.fsencode(right)

    if hasattr(libc, "renameat2"):
        result = libc.renameat2(
            AT_FDCWD,
            ctypes.c_char_p(left_bytes),
            AT_FDCWD,
            ctypes.c_char_p(right_bytes),
            EXCHANGE_FLAG,
        )
    elif hasattr(libc, "renamex_np"):
        result = libc.renamex_np(
            ctypes.c_char_p(left_bytes),
            ctypes.c_char_p(right_bytes),
            EXCHANGE_FLAG,
        )
    else:
        raise OSError("platform does not expose an atomic path-exchange primitive")

    if result != 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno), f"{left} <-> {right}")


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} LEFT RIGHT", file=sys.stderr)
        return 2
    atomic_exchange(Path(sys.argv[1]), Path(sys.argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
