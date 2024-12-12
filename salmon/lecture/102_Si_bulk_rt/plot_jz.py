#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

dat = np.loadtxt("Si_rt.data")

plt.figure(figsize=[5, 5])
plt.plot(dat[:, 1-1]*0.0242, -dat[:, 16-1], "-b", label="j")
plt.xlim([0, None])
plt.ylim([None, None])
plt.xlabel("Time $t$ [fsec]")
plt.ylabel("Current density")
plt.legend()
plt.tight_layout()
plt.savefig("plot_jz.png")
plt.show()


