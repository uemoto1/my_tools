#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

dat = np.loadtxt("Si_rt.data")

plt.figure(figsize=[5, 5])
plt.plot(dat[:, 1-1]*0.0242, dat[:, 13-1]*51.4, "-b", label="E")
plt.xlim([0, None])
plt.ylim([None, None])
plt.xlabel("Time $t$ [fsec]")
plt.ylabel("Electric field $E$ [V/Ang.]")
plt.legend()
plt.tight_layout()
plt.savefig("plot_ez.png")
plt.show()


