import os
import numpy as np
import scipy.signal

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-n", "--nthread", type=int, default=0)
args = parser.parse_args()

basedir = os.path.dirname(os.path.abspath(args.input))
n_order_max = 10

if args.nthread < 1:
    args.nthread = int(os.environ.get("OMP_NUM_THREADS", "1"))

parse_float = lambda x: float(x.lower().replace("d","e"))
parse_string = lambda x: x.replace('"', '').replace("'", "").strip()
with open(args.input, "r") as fh:
    print(fh.name)
    for line in fh:
        tmp = line.split("=")
        if len(tmp) == 2:
            lhs = tmp[0].strip()
            rhs = tmp[1].split("!")[0].strip()
            if lhs == "omega1":
                omega1 = parse_float(rhs)
            if lhs == "sysname":
                sysname = parse_string(rhs)

with open(f"{basedir}/.shape.txt") as fh:
    macro = int(fh.readline())
target_list = list(range(1, macro+1))

# Perform fourier transformation at omega_n
def run(imacro):
    filepath = f"{basedir}/{sysname}_sbe_m/m{imacro:06d}/{sysname}_sbe_rt.data"
    print(filepath)
    dat = np.loadtxt(filepath, dtype=float)
    t = dat[:, 1-1]
    jm_z = dat[:, 16-1]
    nt = len(t)
    window = scipy.signal.blackman(nt)
    result = []
    for n in range(0, n_order_max+1):
        omega_n = omega1 * n
        jm_omega_n = - sum(jm_z * np.exp(1.0j * omega_n * t) * window) * (1.0 / len(t))
        result.append([n, omega_n, np.real(jm_omega_n), np.imag(jm_omega_n)])
    return result

if args.nthread > 1:
    from multiprocessing import Pool
    with Pool(args.nthread) as p:
        result_list = p.map(run, target_list)
else:
    result_list = list(map(run, target_list))

with open(f"{basedir}/jm_z_omega_n.txt", "w") as fh:
    print(fh.name)
    fh.write("imacro n omega_n re_jm_omega_n im_jm_omega_n\n")
    for imacro, result in zip(target_list, result_list):
        for n, omega_n, re_jm_omega_n, im_jm_omega_n in result:
            fh.write(f"{imacro:6d} {n:6d} {omega_n:12.6f} {re_jm_omega_n:+12.3e} {im_jm_omega_n:+12.3e}\n")



