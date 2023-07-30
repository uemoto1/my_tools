#!/usr/bin/env python3
# import optparse
import os
import numpy as np
import xml.etree.ElementTree as ET

print("# Loading vasprun.xml ...")
tree = ET.parse('vasprun.xml')
root = tree.getroot()

ISPIN = int(root.find(".//i[@name='ISPIN']").text)
print("# ISPIN = %s" % ISPIN)

NBANDS = int(root.find(".//i[@name='NBANDS']").text)
print("# NBANDS = %d" % NBANDS)

num_atoms = int(root.find(".//atoms").text)
print("# num_atoms = %d" % num_atoms)

num_kpoint = len(root.findall(".//varray[@name='kpointlist']/"))
print("# num_kpoint = %d" % num_kpoint)

elem_array = root.find("./calculation/projected/array")
field = []
for item in elem_array.findall("./field"):
    field.append(item.text.strip())
num_field = len(field)
print("# num_field: %d" % num_field)
print("# %s" % (", ".join(field)))

print("# Extracting projected weight ...")
dat = np.zeros([ISPIN, num_kpoint, NBANDS, num_atoms, num_field])
elem_set = elem_array.find("./set")
for js in range(ISPIN):
    elem_set_spin = elem_set.find("./set[@comment='spin%d']" % (js+1))
    for jk in range(num_kpoint):
        elem_set_kpoint = elem_set_spin.find("./set[@comment='kpoint %d']" % (jk+1))
        for jb in range(NBANDS):
            elem_set_band = elem_set_kpoint.find("./set[@comment='band %d']" % (jb+1))
            tmp = []
            for r in elem_set_band.findall("./r"):
                tmp.append(np.fromstring(r.text, sep=" ", dtype=float))
            dat[js, jk, jb, :, :] = tmp

print("# Creating output directory 'proj' ...")
if not os.path.isdir("proj"):
    os.mkdir("proj")

print("# Writing output files ...")
for js in range(ISPIN):
    for jatom in range(num_atoms):
        for jfield in range(num_field):
            name = "proj/ion%03d_%s_spin%d.txt" % (jatom+1, field[jfield].strip(), js+1)
            print(name)
            np.savetxt(name, dat[js, :, :, jatom, jfield], header="row(kpoint) col(band)", fmt="%.6f")

print("# Bye!")
