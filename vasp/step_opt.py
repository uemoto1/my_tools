#!/usr/bin/env python3
"""Update POSCAR with CONTCAR, saving both as numbered backups."""
import argparse
import hashlib
import os
from pathlib import Path
from shutil import copy


def file_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def find_next_index(base: str) -> int:
    idx = 0
    while Path(f"{base}.{idx}").exists():
        idx += 1
    return idx


def main():
    parser = argparse.ArgumentParser(description="Step optimizer: backup POSCAR/CONTCAR and update POSCAR")
    args = parser.parse_args()

    if not os.path.exists("CONTCAR"):
        print("CONTCAR not found.")
        return

    if file_hash("POSCAR") == file_hash("CONTCAR"):
        print("POSCAR and CONTCAR are identical. Skipping.")
        return

    idx = find_next_index("POSCAR")

    for name in ("OUTCAR", "OSZICAR", "POSCAR", "CONTCAR"):
        if Path(name).exists():
            bk = f"{name}.{idx}"
            print(bk)
            copy(name, bk)

    copy("CONTCAR", "POSCAR")
    print("POSCAR updated.")


if __name__ == "__main__":
    main()
