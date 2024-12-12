#!/usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt

dat = np.loadtxt("dos.data")
plt.figure(figsize=[5, 5])
plt.plot(dat[:, 0] * 27.2, dat[:, 1] / 27.2, color="-blue")
plt.xlim([-7.5, 7.5])
plt.ylim([0, None])
plt.xlabel("Energy $E-E_F$ [eV]")
plt.ylabel("DoS [1/eV]")
plt.tight_layout()
plt.savefig("plot_dos.png")
plt.show()


