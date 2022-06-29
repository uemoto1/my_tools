#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import re
import sys

tree = ET.parse('vasprun.xml')

root = tree.getroot()

ispin = int(root.find(".//i[@name='ISPIN']").text)
print("# ispin=%d" % ispin)

nedos = float(root.find(".//i[@name='NEDOS']").text)
print("# nedos=%f" % nedos)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi=%f" % efermi)

natom = int(root.find(".//atoms").text)
print("# natom=%d" % natom)

data = np.zeros([nedos, 1+ispin])

element_field = root.findall("calculation/dos/partial/array/field")
nfield = len(element_field)

if nfield > 0:
    data = np.zeros([natom, nfield-1, nedos, ispin+1])
    
    element_set1 = root.find("calculation/dos/partial/array/set")
    for element_set_ion in element_set1:
        comment = element_set_ion.attrib["comment"]
        ion = int(re.sub(r"ion\s*(\d+)", r"\1", comment))
        for element_set_spin in element_set_ion:
            comment = element_set_spin.attrib["comment"]
            i = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
            for n, r in enumerate(element_set_spin):
                tmp = r.text.split()
                data[ion-1, :, n, 0] = float(tmp[0]) - efermi
                for j in range(1, len(tmp)):
                    data[ion-1, j-1, n, i] = float(tmp[j])

    for ion0 in range(natom):
        for ifield0 in range(nfield-1):
            tag = element_field[ifield0+1].text.strip()
            name = "pdos%03d_%s.txt" % (ion0+1, tag)
            np.savetxt(
                name, data[ion0, ifield0, :, :], 
                header="# Energy-EF[eV] DoS[1/eV]", fmt="%+12.6e"
            )
            print("# Generate %s" % name)


