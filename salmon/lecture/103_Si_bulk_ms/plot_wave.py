#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

dat = np.loadtxt("Si_wave.data")

plt.figure(figsize=[5, 5])
plt.plot(dat[:, 1-1]*0.0242, dat[:, 4-1]*51.4, "-b", label="$E_z^{inc}$")
plt.plot(dat[:, 1-1]*0.0242, dat[:, 7-1]*51.4, "-r", label="$E_z^{ref}$")
plt.xlim([0.0, None])
plt.ylim([None, None])
plt.xlabel("Time $t$ [fs]")
plt.ylabel("Field amplitude $E$ [V/Ang.]")
plt.legend()
plt.tight_layout()
plt.savefig("plot_wave.png")
plt.show()

