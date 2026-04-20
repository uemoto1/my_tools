#!/usr/bin/env python3
import shutil

magmom_table = {
    "Fe": "2.9",
    "Pd": "0.3",
    "C": "0.0",
}

shutil.copy("INCAR", "INCAR.backup")

with open("POSCAR") as fh:
    lines = fh.readlines()
    title = lines[0].strip()
    element_list = lines[5].split()
    natom_list = lines[6].split()

with open("INCAR") as fh:
    incar_lines = fh.readlines()

tmp = ["MAGMOM="]
for element, natom in zip(element_list, natom_list):
    val = magmom_table[element]
    tmp.append(f"{natom}*{val}")
magmom_line = " ".join(tmp)

found = False
for i, l in enumerate(incar_lines):
    if l.strip().startswith("MAGMOM"):
        incar_lines[i] = magmom_line + "\n"
        found = True
        break

if not found:
    incar_lines.append(magmom_line + "\n")

with open("INCAR", "w") as fh:
    fh.writelines(incar_lines)
