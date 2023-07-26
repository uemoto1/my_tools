#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import sys
import re

root = ET.parse('vasprun.xml').getroot()

ISPIN = int(root.find(".//i[@name='ISPIN']").text)
print("# ISPIN = %s" % ISPIN)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi=%f" % efermi)

elem_set = root.find("./calculation/dos/total/array/set")
for js in range(ISPIN):
    elem_spin = elem_set.find("./set[@comment='spin %d']" % (js+1))
    with open("tdos_spin%d.txt" % (js+1)) as fh:
        print(fh.name)
        for r in elem_spin:
            fh.write(r.text + "\n")

for js in range(ISPIN):
    dat = np.loadtxt("tdos_spin%d.txt" % (js+1))
    dat[:, 0] -= efermi
    np.savetxt("tdos_ef0_spin%d.txt" % (js+1), dat)
        
# if "-x" in sys.argv:
#     import matplotlib.pyplot as plt
#     xmin = np.amin(tdos[0, :, 0])
#     xmax = np.amax(tdos[0, :, 0])
#     ymax = np.amax(tdos[:, :, 1])
#     plt.plot(tdos[0, :, 0], +tdos[0, :, 1], "-k")
#     plt.xlim([xmin, xmax])
#     if ispin == 1:
#         plt.plot([0, 0], [0, ymax], "--k")
#         plt.ylim([0, ymax])
#     else: # ispin == 2
#         plt.plot(tdos[1, :, 0], -tdos[1, :, 1], "-k")
#         plt.plot([xmin, xmax], [0, 0], "--k")
#         plt.plot([0, 0], [-ymax, ymax], "--k")
#         plt.ylim([-ymax, ymax])
#     plt.xlabel("Energy [eV]")
#     plt.ylabel("DoS [1/eV]")
#     plt.show()
