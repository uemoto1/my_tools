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
for js in range(ISPIN):
    name = "band_ef0_spin%d.txt" % (js+1)
    print(name)
    np.savetxt(name, dat[js, :, :, 0], header="row(kpoint) col(klength, eigen)", fmt="%.6f")



[w35010@wisteria05 band]$ cat get_proj.py 
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
        elem_set_kpoint = elem_set_spin.find("./set[@comment='kpoint %d']" % (js+1))
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

