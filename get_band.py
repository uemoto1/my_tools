#!/usr/bin/env python3
# import optparse
import xml.etree.ElementTree as ET
import numpy as np
import re

root = ET.parse('vasprun.xml').getroot()

elem_nbands = root.find(".//i[@name='NBANDS']")
nbands = int(elem_nbands.text)
print("# nbands=%d" % nbands)
elem_ispin = root.find(".//i[@name='ISPIN']")
ispin = int(elem_ispin.text)
print("# ispin=%d" % ispin)
elem_efermi = root.find(".//i[@name='efermi']")
efermi = float(elem_efermi.text)
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


elem_set1 = root.find("calculation/eigenvalues/array/set")
for elem_set_spin in elem_set1:
    comment = elem_set_spin.attrib["comment"]
    ispin = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
    with open("band_spin%d.txt" % ispin, "w") as fh:

        for elem_set_kpoint in elem_set_spin:
            comment = elem_set_kpoint.attrib["comment"]
            ik = int(re.sub(r"kpoint\s*(\d+)", r"\1", comment))

            if ik == 1:
                kl = 0.0
            else:
                kl += np.linalg.norm(
                    np.dot(kpoint[ik-1], [vec_b1, vec_b2, vec_b3])
                    - np.dot(kpoint[ik-2], [vec_b1, vec_b2, vec_b3])
                )
            fh.write("%12.6f" % kl)

            for r in elem_set_kpoint:
                tmp = r.text.split()
                fh.write(" %12.3e" % (float(tmp[0]) - efermi))
            
            fh.write("\n")

        print("# generated %s" % fh.name)
ispin=1
if True:
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, ispin, sharex=True, sharey=True)
    for i in range(ispin):
        dat = np.loadtxt("band_spin%d.txt" % (i+1))
        axes[i].plot(dat[:, 0], dat[:, 1:], "-k")
        axes[i].plot([dat[0, 0], dat[-1, 0]], [0, 0], "--b")
    plt.ylabel("Electron energy [eV]")
    plt.xlim([dat[0, 0], dat[-1, 0]])
    plt.ylim([np.amin(dat[:, 1]), np.amin(dat[:, -1])])
    plt.show()
