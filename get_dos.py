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

# Read tdos data
tdos = np.zeros([ispin, nedos, 2])

element_set1 = root.find("calculation/dos/total/array/set")
for element_set_spin in element_set1:
    comment = element_set_spin.attrib["comment"]
    iispin1 = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
    for n, r in enumerate(element_set_spin):
        tmp = r.text.split()
        tdos[iispin1-1, n, 0] = float(tmp[0]) - efermi
        tdos[iispin1-1, n, 1] = float(tmp[1])

# Export tdos data
buff = np.zeros([nedos, ispin+1])
buff[:, 0] = tdos[0, :, 0] 
buff[:, 1] = tdos[0, :, 1]
buff[:, 2] = tdos[1, :, 1]
np.savetxt("tdos.txt", buff, 
    header="Energy-EF[eV] DoS[1/eV]", fmt="%+12.6e")
print("# Generated tdos.txt")

# Read pdos data
elem_field = root.findall("calculation/dos/partial/array/field")
nfield = len(elem_field)

if nfield > 0:
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
            



if "-x" in sys.argv:
    import matplotlib.pyplot as plt
    xmin = np.amin(tdos[0, :, 0])
    xmax = np.amax(tdos[0, :, 0])
    ymax = np.amax(tdos[:, :, 1])
    plt.plot(tdos[0, :, 0], +tdos[0, :, 1], "-k")
    plt.xlim([xmin, xmax])
    if ispin == 1:
        plt.plot([0, 0], [0, ymax], "--k")
        plt.ylim([0, ymax])
    else: # ispin == 2
        plt.plot(tdos[1, :, 0], -tdos[1, :, 1], "-k")
        plt.plot([xmin, xmax], [0, 0], "--k")
        plt.plot([0, 0], [-ymax, ymax], "--k")
        plt.ylim([-ymax, ymax])
    plt.xlabel("Energy [eV]")
    plt.ylabel("DoS [1/eV]")
    plt.show()
