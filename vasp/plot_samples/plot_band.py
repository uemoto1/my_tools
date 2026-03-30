#!/usr/bin/python3

e_fermi =   -1.8209   # Modify Fermi energy
e_range_min = None    # Lower bound of y axis
e_range_max = None    # Upper bound of y axis
output = "band.png"

import numpy as np
import matplotlib.pyplot as plt

band_spin1 = np.loadtxt("band_spin1.txt")
# band_spin2 = np.loadtxt("band_spin2.txt")
kpoint_labels = np.loadtxt("kpoint_labels.txt", dtype="str")

if e_range_max is None:
    e_range_max = min(band_spin1[:, -1]) - e_fermi

plt.figure(figsize=[5, 5], dpi=144)

for n in range(1, band_spin1.shape[1]):
    plt.plot(band_spin1[:, 0], band_spin1[:, n] - e_fermi, "-r")
    # plt.plot(band_spin2[:, 0], band_spin2[:, n] - e_fermi, "-b")

plt.xlim([band_spin1[0, 0], band_spin1[-1, 0]])
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

