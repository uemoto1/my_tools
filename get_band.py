#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import re

tree = ET.parse('vasprun.xml')

root = tree.getroot()

element_rec_basis = root.find("primitive_cell/structure/crystal/varray[@name='rec_basis']")
vec_b1 = np.array(element_rec_basis[0].text.split(), dtype=float) * 2.0 * np.pi
vec_b2 = np.array(element_rec_basis[1].text.split(), dtype=float) * 2.0 * np.pi
vec_b3 = np.array(element_rec_basis[2].text.split(), dtype=float) * 2.0 * np.pi
print("# vec_b1=%f, %f, %f" % tuple(vec_b1))
print("# vec_b2=%f, %f, %f" % tuple(vec_b2))
print("# vec_b3=%f, %f, %f" % tuple(vec_b3))

element_kpointlist = root.find("kpoints/varray[@name='kpointlist']")
kpoint = []
for v in element_kpointlist:
    kpoint.append(np.array(v.text.split(), dtype=float))
for k1, k2, k3 in kpoint:
    print("# k=(%f,%f,%f)" % (k1, k2, k3))

element_efermi = root.find("calculation/dos/i[@name='efermi']")
efermi = float(element_efermi.text)
print("# efermi=%f" % efermi)

element_set1 = root.find("calculation/eigenvalues/array/set")
for element_set_spin in element_set1:
    comment = element_set_spin.attrib["comment"]
    ispin = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
    with open("band_spin%d.txt" % ispin, "w") as fh:

        for element_set_kpoint in element_set_spin:
            comment = element_set_kpoint.attrib["comment"]
            ik = int(re.sub(r"kpoint\s*(\d+)", r"\1", comment))

            if ik == 1:
                kl = 0.0
            else:
                kl += np.linalg.norm(
                    np.dot(kpoint[ik-1], [vec_b1, vec_b2, vec_b3])
                    - np.dot(kpoint[ik-2], [vec_b1, vec_b2, vec_b3])
                )
            fh.write("%12.6f" % kl)

            for r in element_set_kpoint:
                tmp = r.text.split()
                fh.write(" %12.3e" % (float(tmp[0]) - efermi))
            
            fh.write("\n")

        print("# generated %s" % fh.name)

