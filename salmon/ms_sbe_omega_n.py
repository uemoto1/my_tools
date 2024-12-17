import numpy as np
import os
import scipy.signal

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-n", "--nthread", type=int, default=0)
parser.add_argument("-m",  "--max", type=int, default=10)
args = parser.parse_args()

basedir = os.path.dirname(args.input)
n_order_max = args.max

if args.nthread >= 1:
    nthread = args.nthread
else:
    nthread = int(os.environ.get("OMP_NUM_THREADS", "1"))

with open(args.input, "r") as fh:
    print(fh.name)
    for line in fh:
        tmp = line.split("=")
        if len(tmp) == 2:
            lhs = tmp[0].strip()
            rhs = tmp[1].split("!")[0].strip()

            if lhs == "omega1":
                omega1 = float(rhs.replace("d", "e"))
            if lhs == "sysname":
                sysname = rhs.replace('"', '').replace("'", "").strip()

with open(f"{basedir}/.shape.txt") as fh:
    macro = int(fh.readline())

target_list = [
    f"{basedir}/{sysname}_sbe_m/m{i:06d}/{sysname}_sbe_rt.data" 
    for i in range(1, macro+1)
]

def run(name):
    print(name)
    dat = np.loadtxt(name, dtype=float)
    t = dat[:, 1-1]
    jm_z = dat[:, 16-1]
    window = scipy.signal.blackman(len(t))
    with open(f"{name}.omega_n.txt", "w") as fh:
        print(fh.name)
        for n in range(1, 10):
            omega_n = omega1 * n
            j_freq = - sum(jm_z * np.exp(1.0j * omega_n * t) * window) * (1.0 / len(t))
            fh.write("%d %+25.15e %+25.15e %+25.15e\n" % (n, omega_n, np.real(j_freq), np.imag(j_freq)))
    return name


if nthread > 1:
    from multiprocessing import Pool
    with Pool(nthread) as p:
        p.map(run, target_list)
else:
    list(map(run, target_list))

