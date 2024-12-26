#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

dat = np.loadtxt("Si_RT_Ac/Si_Ac_000000.data")
hx_m = 189.036

plt.figure(figsize=[6, 3])
plt.plot(dat[:, 1-1]*hx_m*0.0529, dat[:, 9-1]*51.4, "-b", label="E")
plt.xlim([-1200, 1200])
plt.ylim([None, None])
plt.xlabel("Position $x$ [nm]")
plt.ylabel("$E_z$ [eV]")
plt.legend()
plt.tight_layout()
plt.savefig("plot_ms_ez.png")
plt.show()

