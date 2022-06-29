#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import sys
import re

tree = ET.parse('vasprun.xml')

root = tree.getroot()

ispin = int(root.find(".//i[@name='ISPIN']").text)
print("# ispin=%d" % ispin)

nedos = float(root.find(".//i[@name='NEDOS']").text)
print("# nedos=%d" % nedos)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi=%f" % efermi)

data = np.zeros([ispin, nedos, 2])

element_set1 = root.find("calculation/dos/total/array/set")
for element_set_spin in element_set1:
    comment = element_set_spin.attrib["comment"]
    i1 = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
    for n, r in enumerate(element_set_spin):
        tmp = r.text.split()
        data[i1-1, n, :] = float(tmp[0]), float(tmp[1])

        

buff = np.zeros([nedos, ispin+1])
buff[:, 0] = data[0, :, 0] - efermi
buff[:, 1] = data[0, :, 1]
buff[:, 2] = data[1, :, 1]
np.savetxt("tdos.txt", buff, 
    header="Energy-EF[eV] DoS[1/eV]", fmt="%+12.6e")
print("# Generated tdos.txt")



if "-x" in sys.argv:
    import matplotlib.pyplot as plt
    xmin = np.amin(data[0, :, 0])
    xmax = np.amax(data[0, :, 0])
    ymax = np.amax(data[:, :, 1])
    plt.plot(data[0, :, 0], +data[0, :, 1], "-k")
    plt.xlim([xmin, xmax])
    if ispin == 1:
        plt.plot([0, 0], [0, ymax], "--k")
        plt.ylim([0, ymax])
    else: # ispin == 2
        plt.plot(data[0, :, 0], -data[0, :, 1], "-k")
        plt.plot([xmin, xmax], [0, 0], "--k")
        plt.plot([0, 0], [-ymax, ymax], "--k")
        plt.ylim([-ymax, ymax])
    plt.xlabel("Energy [eV]")
    plt.ylabel("DoS [1/eV]")
    plt.show()
