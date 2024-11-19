#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
tdos = np.loadtxt("tdos_ef0_spin1.txt")

xmin = 0.9 * np.min(tdos[:, 0])
xmax = 0.9 * np.max(tdos[:, 0])
ymax = 1.1 * np.max(tdos[:, 1])

plt.figure(figsize=[5, 5])
plt.plot(tdos[:, 0], tdos[:, 1], "-k")
plt.xlabel("Energy [eV]")
plt.ylabel("DoS [1/eV]")
plt.xlim([xmin, xmax])
plt.ylim([0, ymax])
plt.savefig("tdos.png")
plt.show()
