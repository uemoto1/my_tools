#!/usr/bin/env python3
# import optparse
import xml.etree.ElementTree as ET
import numpy as np
import sys
import os

root = ET.parse('vasprun.xml').getroot()

ISPIN = int(root.find(".//i[@name='ISPIN']").text)
print("# ISPIN = %s" % ISPIN)

NBANDS = int(root.find(".//i[@name='NBANDS']").text)
print("# NBANDS = %d" % NBANDS)

efermi = float(root.find(".//i[@name='efermi']").text)
print("# efermi = %f" % efermi)

natom = int(root.find(".//atoms").text)
print("# natom = %d" % natom)

nkpoint = len(root.findall(".//varray[@name='kpointlist']/"))
print("# nkpoint = %d" % nkpoint)

elem_array = root.find("./calculation/projected/array")
field = []
for item in elem_array.findall("./field"):
    field.append(item.text)
nfield = len(field)

if not os.path.isdir("proj_band"):
    os.mkdir("proj_band")

elem_set = elem_array.find("./set")
for js in range(ISPIN):
    elem_set_spin = elem_set.find("./set[@comment='spin%d']" % (js+1))
    for jk in range(nkpoint):
        elem_set_kpoint = elem_set_spin.find("./set[@comment='kpoint %d']" % (js+1))
        for jb in range(NBANDS):
            elem_set_band = elem_set_kpoint.find("./set[@comment='band %d']" % (jb+1))
            with open("proj_band/spin%d_k%03d_band%03d.txt" % (js+1, jk+1, jb+1), "w") as fh:
                print(fh.name)
                fh.write("# " + " ".join(field) + "\n")
                for r in elem_set_band:
                    fh.write(r.text + "\n")

buf = np.empty([ISPIN, nkpoint, NBANDS, natom, nfield])
for js in range(ISPIN):
    for jk in range(nkpoint):
        for jb in range(NBANDS):
            buf[js, jk, jb, :, :] = np.loadtxt("proj_band/spin%d_k%03d_band%03d.txt" % (js+1, jk+1, jb+1))

if not os.path.isdir("proj_ion"):
    os.mkdir("proj_ion")

for js in range(ISPIN):
    for jatom in range(natom):
        for jfield in range(nfield):
            name = "proj_ion/ion%03d_%s_spin%d.txt" % (jatom, field[jfield].strip(), js+1)
            print(name)
            np.savetxt(name, buf[js, :, :, jatom, jfield], comment="row(kpoint) col(band)" fmt="%.3f")



# elem_set = elem_array.find("./set/")
# for js in range(ISPIN):
    
# "./calculation/projected/eigenvalues/array/set/set[@comment='sp
#     ...: in 1']/set[@comment='kpoint 1']/"

# elem_set1 = root.find("calculation/projected/eigenvalues/array/set")
# for elem_set_spin in elem_set1:
#     comment = elem_set_spin.attrib["comment"]
#     iispin1 = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
#     for elem_set_kpoint in elem_set_spin:
#         comment = elem_set_kpoint.attrib["comment"]
#         ik1 = int(re.sub(r"kpoint\s*(\d+)", r"\1", comment))
#         for n, r in enumerate(elem_set_kpoint):
#             tmp = r.text.split()
#             band[iispin1-1, ik1-1, n] = float(tmp[0]) - efermi


# elem_field = root.findall("calculation/projected/array/field")
# nfield = len(elem_field)

# proj = np.zeros([ispin, nk, nbands, natom, nfield])

# elem_set1 = root.find("calculation/projected/array/set")
# for elem_set_spin in elem_set1:
#     comment = elem_set_spin.attrib["comment"]
#     iispin1 = int(re.sub(r"spin\s*(\d+)", r"\1", comment))
#     for elem_set_kpoint in elem_set_spin:
#         comment = elem_set_kpoint.attrib["comment"]
#         ik1 = int(re.sub(r"kpoint\s*(\d+)", r"\1", comment))
#         for elem_set_band in elem_set_kpoint:
#             comment = elem_set_band.attrib["comment"]
#             iband1 = int(re.sub(r"band\s*(\d+)", r"\1", comment))
#             for n, r in enumerate(elem_set_band):
#                 tmp = r.text.split()
#                 proj[iispin1-1, ik1-1, iband1-1, n, :] = np.array(tmp, dtype=float)

# xk = np.zeros([nk])
# for ik in range(1, nk):
#     xk[ik] = xk[ik-1] +  np.linalg.norm(
#         np.dot(kpoint[ik], [vec_b1, vec_b2, vec_b3])
#         - np.dot(kpoint[ik-1], [vec_b1, vec_b2, vec_b3])
#     )

# buff = np.zeros([nk, nbands+1])
# for iion1 in range(1, natom+1):
#     for ifield in range(nfield):
#         tag = elem_field[ifield].text.replace(" ", "")
#         for iispin1 in range(1, ispin+1):
#             name = "proj%03d_%s_spin%d.txt" % (iion1, tag, iispin1)
#             buff[:, 0] = xk[:]
#             buff[:, 1:] = proj[iispin1-1, :, :, iion1-1, ifield]
#             np.savetxt(name, buff, fmt="%+12.6e")
#             print("# Generated %s" % name)

#         for iispin1 in range(1, ispin+1):
#             name = "proj%03d_%s_spin%d.txt" % (iion1, tag, iispin1)
#             buff[:, 0] = xk[:]
#             buff[:, 1:] = proj[iispin1-1, :, :, iion1-1, ifield]
#             np.savetxt(name, buff, fmt="%+12.6e")
#             print("# Generated %s" % name)


# for i0 in range(ispin):
#     name = "band_spin%d.txt" % (i0+1)
#     buff = np.zeros([nk, nbands+1])
#     buff[:, 0] = xk[:]
#     buff[:, 1:] = band[i0, :, :]
#     np.savetxt(
#         name, buff,
#         header="k Energy-eV[eV]", fmt="%+12.6e"
#     )
#     print("# Generated %s" % name)

