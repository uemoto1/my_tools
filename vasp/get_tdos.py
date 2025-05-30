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
    with open("tdos_spin%d.txt" % (js+1), "w") as fh:
        print(fh.name)
        for r in elem_spin:
            fh.write(r.text + "\n")

for js in range(ISPIN):
    dat = np.loadtxt("tdos_spin%d.txt" % (js+1))
    dat[:, 0] -= efermi
    name = "tdos_ef0_spin%d.txt" % (js+1)
    print(name)
    np.savetxt(name, dat, header="Energy-EF[eV] DoS[1/eV]")
        
