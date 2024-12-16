#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

dat = np.loadtxt("Si_rt_energy.data")

plt.figure(figsize=[5, 5])
plt.plot(dat[:, 1-1]*0.0242, dat[:, 3-1]*27.2, "-blue", label="$E_ex$")
plt.xlim([0, None])
plt.ylim([0, None])
plt.xlabel("Time [fsec]")
plt.ylabel("Energy [eV]")
plt.legend()
plt.tight_layout()
plt.savefig("plot_energy.png")
plt.show()
