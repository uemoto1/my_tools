#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import sys
import re

root = ET.parse('vasprun.xml').getroot()

ispin = int(root.find(".//i[@name='ISPIN']").text)
print("# ispin=%d" % ispin)

nedos = int(root.find(".//i[@name='NEDOS']").text)
print("# nedos=%d" % nedos)

natom = int(root.find(".//atoms").text)
print("# natom=%d" % natom)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi=%f" % efermi)

elem_field = root.findall("calculation/dos/partial/array/field")
nfield = len(elem_field)

if nfield == 0:
    sys.stderr("# partial DoS is not exist!")
    sys.exit(-1)

pdos = np.zeros([ispin, natom, nedos, nfield])
element_set1 = root.find("calculation/dos/partial/array/set")
for element_set_ion in element_set1:
    comment = element_set_ion.attrib["comment"]
    iion1 = int(re.sub(r"ion\s*(\d+)", r"\1", comment))
    for element_set_spin in element_set_ion:
        comment = element_set_spin.attrib["comment"]
        iispin1 = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
        for n, r in enumerate(element_set_spin):
            tmp = r.text.split()
            pdos[iispin1-1, iion1-1, n, 0] = float(tmp[0]) - efermi
            for ifield in range(1, nfield):
                pdos[iispin1-1, iion1-1, n, ifield] = float(tmp[ifield])

# Export pdos data
buff = np.zeros([nedos, ispin+1])
for iion1 in range(1, natom+1):
    for ifield in range(1, nfield):
        tag = elem_field[ifield].text.replace(" ", "")
        name = "pdos%03d_%s.txt" % (iion1, tag)
        buff[:, 0] = pdos[0, 0, :, 0]
        for iispin in range(1, ispin):
            buff[:, iispin] = pdos[iispin-1, iion1-1, :, ifield]
        np.savetxt(name, buff, 
            header="Energy-EF[eV] DoS[1/eV]", fmt="%+12.6e")
        print("# Generated %s" % name)
        




