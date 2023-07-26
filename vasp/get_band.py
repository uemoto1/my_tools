#!/usr/bin/env python3
# import optparse
import xml.etree.ElementTree as ET
import numpy as np
import re
import sys

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
nk = len(kpointlist)


elem_set = root.find("./calculation/eigenvalues/array/set")
for js in range(ISPIN):
    elem_set_spin = elem_set.find("./set[@comment='spin %d']" % (js+1))
    with open("eigen_spin%d.txt" % (js+1), "w") as fh:
        print(fh.name)
        for jk in range(nk):
            elem_set_kpoint = elem_set_spin.find("./set[@comment='kpoint %d']" % (jk+1))
            for r in elem_set_kpoint:
                fh.write(" " + r.text.split()[0])
            fh.write("\n")

# Calculate x coordinate
xlist = []
for jk in range(nk):
    vec_k = np.dot(kpointlist[jk], [vec_b1, vec_b2, vec_b3])
    if jk == 0:
        x = 0.0
    else:
        dk = np.linalg.norm(vec_k - vec_k_prev)
        x += dk
    vec_k_prev = vec_k
    xlist.append(x)

for js in range(ISPIN):
    buf1 = np.loadtxt("eigen_spin%d.txt" % (js+1))
    nrow, ncol = buf1.shape
    buf2 = np.empty([nrow, ncol+1])
    buf2[:, 0] = xlist
    buf2[:, 1:] = buf1[:, :] - efermi
    np.savetxt("band_spin%d.txt" % (js+1), buf2)
    print("band_spin%d.txt" % (js+1))




# if "-x" in sys.argv:
#     import matplotlib.pyplot as plt
#     xmax = np.amax(xk)
#     ymin = np.amin(band[:, :, 0])
#     ymax = np.amin(band[:, :, -1])
#     if ISPIN == 1:
#         plt.plot(xk[:], band[0, :, :], "-k")
#     else: # ISPIN == 2
#         plt.plot(xk[:], band[0, :, :], "-r")
#         plt.plot(xk[:], band[1, :, :], "-b")
#     plt.plot([0, xmax], [0, 0], "--k")
#     plt.xlim([0, xmax])
#     plt.ylim([ymin, ymax])
#     plt.show()