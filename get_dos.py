#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import re

tree = ET.parse('vasprun.xml')

root = tree.getroot()

element_efermi = root.find("calculation/dos/i[@name='efermi']")
efermi = float(element_efermi.text)
print("# efermi=%12.6f" % efermi)

element_set1 = root.find("calculation/dos/total/array/set")
for element_set_spin in element_set1:
    comment = element_set_spin.attrib["comment"]
    ispin = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
    with open("tdos_spin%d.txt" % ispin, "w") as fh:
        fh.write("# Energy-EF (eV), Total DoS (1/eV)\n")
        for r in element_set_spin:
            tmp = r.text.split()
            energy = float(tmp[0]) - efermi
            dos = float(tmp[1])
            fh.write("%+12.6f %10.3e\n" % (energy, dos))
        print("# generated %s" % fh.name)

element_field = root.findall("calculation/dos/partial/array/field")

header = "# Energy-EF"
for item in element_field[1:]:
    header += " " + item.text.strip()

element_set1 = root.find("calculation/dos/partial/array/set")
for element_set_ion in element_set1:
    comment = element_set_ion.attrib["comment"]
    iion = int(re.sub(r"ion\s*(\d+)", r"\1", comment))
    for element_set_spin in element_set_ion:
        comment = element_set_spin.attrib["comment"]
        ispin = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
        with open("pdos%03d_spin%d.txt" % (iion, ispin), "w") as fh:
            fh.write(header + "\n") 
            for r in element_set_spin:
                tmp = r.text.split()
                energy = float(tmp[0]) - efermi
                fh.write("%+12.6f" % energy)
                for i in range(1, len(tmp)):
                    fh.write(" %10.3e" % float(tmp[i]))
                fh.write("\n")
        print("# generated %s" % fh.name)


            
