#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
tdos1 = np.loadtxt("tdos_ef0_spin1.txt")
tdos2 = np.loadtxt("tdos_ef0_spin2.txt")

xmin = 0.9 * np.min(tdos1[:, 0])
xmax = 0.9 * np.max(tdos1[:, 0])
ymax = 1.1 * np.max([np.max(tdos1[:, 1]), np.max(tdos2[:, 1])]) 

plt.figure(figsize=[5, 5])
plt.plot(tdos1[:, 0], tdos1[:, 1], "-k")
plt.plot(tdos2[:, 0], -tdos2[:, 1], "-k")
plt.xlabel("Energy [eV]")
plt.ylabel("DoS [1/eV]")
plt.xlim([xmin, xmax])
plt.ylim([-ymax, +ymax])
plt.savefig("tdos2.png")
plt.show()
