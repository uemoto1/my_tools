#!/usr/bin/env python3

magmom_table = {
    "Fe": "2.9",
    "Pd": "0.3",
    "C": "0.0",
}

with open("POSCAR") as fh:
    line = fh.readlines()
    title = line[0].strip()
    element_list = line[5].split()
    natom_list = line[6].split()

with open("INCAR") as fh:
    print(fh.name)
    line = fh.readlines()

with open("INCAR.backup", "w") as fh:
    print(fh.name)
    fh.writelines(line)

tmp = ["MAGMOM="]
for element, natom in zip(element_list, natom_list):
    val = magmom_table[element]
    tmp += [f"{natom}*{val}"]
magmom_line = " ".join(tmp)

for i in range(len(line)):
    if line[i].startswith("MAGMOM"):
        line[i] = f"{magmom_line}\n"

with open("INCAR", "w") as fh:
    print(fh.name)
    fh.writelines(line)

