#!/usr/bin/env python3
# import optparse
import xml.etree.ElementTree as ET
import numpy as np
import re
import sys

root = ET.parse('vasprun.xml').getroot()

ispin = int(root.find(".//i[@name='ISPIN']").text)
print("# ispin=%d" % ispin)

nbands = int(root.find(".//i[@name='NBANDS']").text)
print("# nbands=%d" % nbands)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi=%f" % efermi)

elem_rec_basis = root.find(".//varray[@name='rec_basis']")
vec_b1 = 2 * np.pi * np.array(elem_rec_basis[0].text.split(), dtype=float)
vec_b2 = 2 * np.pi * np.array(elem_rec_basis[1].text.split(), dtype=float)
vec_b3 = 2 * np.pi * np.array(elem_rec_basis[2].text.split(), dtype=float)
print("# vec_b1=%f, %f, %f" % tuple(vec_b1))
print("# vec_b2=%f, %f, %f" % tuple(vec_b2))
print("# vec_b3=%f, %f, %f" % tuple(vec_b3))

elem_kpointlist = root.find(".//varray[@name='kpointlist']")
kpoint = []
for v in elem_kpointlist:
    kpoint.append(np.array(v.text.split(), dtype=float))
nk = len(kpoint)
print("# nk=%d" % nk)

band = np.zeros([ispin, nk, nbands])

elem_set1 = root.find("calculation/eigenvalues/array/set")
for elem_set_spin in elem_set1:
    comment = elem_set_spin.attrib["comment"]
    iispin1 = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
    for elem_set_kpoint in elem_set_spin:
        comment = elem_set_kpoint.attrib["comment"]
        ik1 = int(re.sub(r"kpoint\s*(\d+)", r"\1", comment))
        for n, r in enumerate(elem_set_kpoint):
            tmp = r.text.split()
            band[iispin1-1, ik1-1, n] = float(tmp[0]) - efermi

xk = np.zeros([nk])
for ik in range(1, nk):
    xk[ik] = xk[ik-1] +  np.linalg.norm(
        np.dot(kpoint[ik], [vec_b1, vec_b2, vec_b3])
        - np.dot(kpoint[ik-1], [vec_b1, vec_b2, vec_b3])
    )

for i0 in range(ispin):
    name = "band_spin%d.txt" % (i0+1)
    buff = np.zeros([nk, nbands+1])
    buff[:, 0] = xk[:]
    buff[:, 1:] = band[i0, :, :]
    np.savetxt(
        name, buff,
        header="k Energy-eV[eV]", fmt="%+12.6e"
    )
    print("# Generated %s" % name)


if "-x" in sys.argv:
    import matplotlib.pyplot as plt
    xmax = np.amax(xk)
    ymin = np.amin(band[:, :, 0])
    ymax = np.amin(band[:, :, -1])
    if ispin == 1:
        plt.plot(xk[:], band[0, :, :], "-k")
    else: # ispin == 2
        plt.plot(xk[:], band[0, :, :], "-r")
        plt.plot(xk[:], band[1, :, :], "-b")
    plt.plot([0, xmax], [0, 0], "--k")
    plt.xlim([0, xmax])
    plt.ylim([ymin, ymax])
    plt.show()