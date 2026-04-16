#!/usr/bin/env python3
"""Update POSCAR with CONTCAR, saving both as numbered backups."""
import argparse
import os
from pathlib import Path
from shutil import copy, move


def find_next_index(base: str) -> int:
    idx = 0
    while Path(f"{base}.{idx}").exists():
        idx += 1
    return idx


def main():
    parser = argparse.ArgumentParser(description="Step optimizer: backup POSCAR/CONTCAR and update POSCAR")
    parser.add_argument("-n", "--prefix", default="", help="Prefix for backup files (default: no prefix)")
    args = parser.parse_args()

    if not os.path.exists("CONTCAR"):
        print("CONTCAR not found.")
        return

    prefix = f"{args.prefix}." if args.prefix else ""
    idx = find_next_index(f"{prefix}POSCAR")

    poscar_bk = f"{prefix}POSCAR.{idx}"
    contcar_bk = f"{prefix}CONTCAR.{idx}"

    print(f"{poscar_bk}")
    copy("POSCAR", poscar_bk)
    print(f"{contcar_bk}")
    copy("CONTCAR", contcar_bk)
    move("CONTCAR", "POSCAR")
    print("POSCAR updated.")


if __name__ == "__main__":
    main()
