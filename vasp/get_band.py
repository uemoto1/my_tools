#!/usr/bin/env python3
import numpy as np
import xml.etree.ElementTree as ET

tree = ET.parse('vasprun.xml')
root = tree.getroot()

ISPIN = int(root.find(".//i[@name='ISPIN']").text)
print("# ISPIN = %s" % ISPIN)

NBANDS = int(root.find(".//i[@name='NBANDS']").text)
print("# NBANDS = %d" % NBANDS)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi = %f" % efermi)

elem_rec_basis = root.find(".//varray[@name='rec_basis']")
vec_b1 = np.fromstring(elem_rec_basis[0].text, sep=" ", dtype=float)
vec_b2 = np.fromstring(elem_rec_basis[1].text, sep=" ", dtype=float)
vec_b3 = np.fromstring(elem_rec_basis[2].text, sep=" ", dtype=float)
print("# vec_b1 = (%+.3f, %+.3f, %+.3f)" % tuple(vec_b1))
print("# vec_b2 = (%+.3f, %+.3f, %+.3f)" % tuple(vec_b2))
print("# vec_b3 = (%+.3f, %+.3f, %+.3f)" % tuple(vec_b3))

elem_kpointlist = root.find(".//varray[@name='kpointlist']")
kpointlist = []
for tmp in elem_kpointlist:
    kpoint = np.fromstring(tmp.text, sep=" ", dtype=float)
    kpointlist.append(kpoint)
    print("# kpoint (%+.3f, %+.3f, %+.3f)" % tuple(kpoint))
num_kpoint = len(kpointlist)
print("# num_kpoint = %d" % num_kpoint)

# Calculate x coordinate
xlist = []
for jk in range(num_kpoint):
    vec_k = np.dot(kpointlist[jk], [vec_b1, vec_b2, vec_b3])
    if jk == 0:
        x = 0.0
    else:
        dk = np.linalg.norm(vec_k - vec_k_prev)
        x += dk
    vec_k_prev = vec_k
    xlist.append(x)
    print("# x[%d]: %.6f" % (jk, x))

print("# Extracting eigenenergy ...")
dat = np.zeros([ISPIN, num_kpoint, NBANDS, 1+1])
elem_set = root.find("./calculation/eigenvalues/array/set")
for js in range(ISPIN):
    elem_set_spin = elem_set.find("./set[@comment='spin %d']" % (js+1))
    for jk in range(num_kpoint):
        elem_set_kpoint = elem_set_spin.find("./set[@comment='kpoint %d']" % (jk+1))
        buf = []
        for r in elem_set_kpoint:
            tmp = np.fromstring(r.text, sep=" ", dtype=float)
            buf.append(tmp)
        dat[js, jk, :, :] = buf

print("# Writing output files ...")
tmp = np.zeros([num_kpoint, 1+NBANDS])
for js in range(ISPIN):
    name = "band_ef0_spin%d.txt" % (js+1)
    print(name)
    tmp[:, 0] = xlist
    tmp[:, 1:] = dat[js, :, :, 0] - efermi
    np.savetxt(name, tmp, header="row(kpoint) col(klength, eigen)", fmt="%.6f")



