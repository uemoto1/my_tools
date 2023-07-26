#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import sys
import re

tree = ET.parse('vasprun.xml')
root = tree.getroot()

ISPIN = int(root.find(".//i[@name='ISPIN']").text)
print("# ISPIN = %s" % ISPIN)

NBANDS = int(root.find(".//i[@name='NBANDS']").text)
print("# NBANDS = %d" % NBANDS)

NEDOS = int(root.find(".//i[@name='NEDOS']").text)
print("# NEDOS=%d" % NEDOS)

natom = int(root.find(".//atoms").text)
print("# natom=%d" % natom)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi=%f" % efermi)

elem_array = root.find("./calculation/dos/partial/array")

field = ""
for item in elem_array.findall("./field"):
    field += item.text


elem_set = elem_array.find("./set")

for jion in range(natom):
    elem_set_ion = elem_set.find("./set[@comment='ion %d']" % (jion+1))
    for js in range(ISPIN):
        elem_set_spin = elem_set_ion.find("./set[@comment='spin %d']" % (js+1))
        with open("pdos_ion%03d_spin%d.txt" % (jion+1, js+1), "w") as fh:
            print(fh.name)
            fh.write("#" + field + "\n")
            for r in elem_set_spin:
                fh.write(r.text + "\n")

for jion in range(natom):
    for js in range(ISPIN):
        dat = np.loadtxt("pdos_ion%03d_spin%d.txt" % (jion+1, js+1))
        dat[:, 0] = dat[:, 0] - efermi
        np.savetxt("pdos_ef_ion%03d_spin%d.txt" % (jion+1, js+1), dat, header=field)

# elem_field = root.findall("calculation/dos/partial/array/field")
# for item in elem_field:
#     print("# projection: %s" % item.text)
# nfield = len(elem_field)

# if nfield == 0:
#     sys.stderr("#ERROR: partial DoS is not exist!")
#     sys.exit(-1)



# pdos = np.zeros([ISPIN, natom, NEDOS, nfield])
# element_set1 = root.find("calculation/dos/partial/array/set")
# for element_set_ion in element_set1:
#     comment = element_set_ion.attrib["comment"]
#     iion1 = int(re.sub(r"ion\s*(\d+)", r"\1", comment))
#     for element_set_spin in element_set_ion:
#         comment = element_set_spin.attrib["comment"]
#         iISPIN1 = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
#         for n, r in enumerate(element_set_spin):
#             tmp = r.text.split()
#             pdos[iISPIN1-1, iion1-1, n, 0] = float(tmp[0]) - efermi
#             for ifield in range(1, nfield):
#                 pdos[iISPIN1-1, iion1-1, n, ifield] = float(tmp[ifield])

# # Export pdos data
# buff = np.zeros([NEDOS, ISPIN+1])
# for iion1 in range(1, natom+1):
#     for ifield in range(1, nfield):
#         tag = elem_field[ifield].text.replace(" ", "")
#         name = "pdos%03d_%s.txt" % (iion1, tag)
#         buff[:, 0] = pdos[0, 0, :, 0]
#         for iISPIN in range(1, ISPIN):
#             buff[:, iISPIN] = pdos[iISPIN-1, iion1-1, :, ifield]
#         np.savetxt(name, buff, 
#             header="Energy-EF[eV] DoS[1/eV]", fmt="%+12.6e")
#         print("# Generated %s" % name)
        




