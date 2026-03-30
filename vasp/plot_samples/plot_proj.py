#!/usr/bin/python3

e_fermi =   -1.8209   # Modify Fermi energy
e_range_min = None
e_range_max = None
ispin = 1    # 1 or 2
# Specify target ion and orbits:
# (orbits: "s", "py", "pz", "px", "dyz", "dxy", "dz2", "dxz", "x2-y2")
target_list = [
    # (number, orbit),
    (1, "px"),
    (1, "py"),
    (1, "s"),
]
dot_scale = 30.0
dot_step = 2
dot_color = "red"
curve_color = "gray"
output = "band_proj.png"

################################################################################

import numpy as np
import matplotlib.pyplot as plt

band = np.loadtxt(f"band_spin{ispin}.txt")
kpoint_labels = np.loadtxt("kpoint_labels.txt", dtype="str")

if e_range_max is None:
    e_range_max = min(band[:, -1]) - e_fermi

# Calculate sum of projections over specified target orbitals ...
tmp = []
for i, orbit in target_list:
    tmp.append(np.loadtxt(f"proj/ion{i:03d}_{orbit}_spin{ispin}.txt"))
proj = sum(tmp) * (1.0 / len(target_list))

plt.figure(figsize=[5, 5], dpi=144)

for i in range(band.shape[1]-1):
    plt.plot(band[:, 0], band[:, i+1] - e_fermi, "-", color=curve_color)


for ik in range(0, band.shape[0], dot_step):
    for i in range(band.shape[1]-1):
        plt.plot(band[ik, 0], band[ik, i+1] - e_fermi, ".", ms=proj[ik, i]*dot_scale, color=dot_color)

plt.xlim([band[0, 0], band[-1, 0]])
plt.xlabel("Wavenumber $k$")

plt.ylim([e_range_min, e_range_max])
plt.ylabel("Energy $E-E_F$ (eV)")

k = np.array(kpoint_labels[:, 0], dtype=float)
label = list(kpoint_labels[:, -1])
plt.xticks(k, label)

plt.grid()
plt.tight_layout()
plt.savefig(output)
print(f"# Generate {output}")
plt.show()

