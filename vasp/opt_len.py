import argparse
import scipy.optimize
import shutil
import numpy as np
import sys
import subprocess

parser = argparse.ArgumentParser(description="Optimize the lattice length")
parser.add_argument('command', nargs="*")
parser.add_argument("-a", "--optimize-a", dest="a", action="store_true", default=False)
parser.add_argument("-b", "--optimize-b", dest="b", action="store_true", default=False)
parser.add_argument("-c", "--optimize-c", dest="c", action="store_true", default=False)
parser.add_argument("-e", "--epsilon", dest="e", default=1e-2, type=float)
parser.add_argument("-n", dest="n", default=100, type=int)

args = parser.parse_args()

if not (args.a or args.b or args.c):
    sys.exit(-1)

log = open("opt.log", "w")

icount = 0

def func(var):
    global icount
    global vec_a, vec_b, vec_c
    # Backup present poscar file:
    shutil.copy("POSCAR", f"POSCAR.opt{icount:03d}")
    if icount > 0:
        shutil.copy("CONTCAR", "POSCAR")
    # Read original poscar
    with open("POSCAR", "r") as fh:
        poscar = fh.readlines()
    # Prepare new state
    var_list = list(var)
    state = ""
    if args.a:
        a = var_list.pop(0)
        state += f"|a|={a:12.6f}, "
        vec_a = vec_a / np.linalg.norm(vec_a) * a
    if args.b:
        b = var_list.pop(0)
        state += f"|b|={b:12.6f}, "
        vec_b = vec_b / np.linalg.norm(vec_b) * b
    if args.c:
        c = var_list.pop(0)
        state += f"|c|={c:12.6f}, "
        vec_c = vec_c / np.linalg.norm(vec_c) * c
    # Write POSCAR file
    # Write POSCAR file
    with open("POSCAR", "w") as fh:
        fh.write(poscar[0])
        fh.write(poscar[1])
        fh.write("%12.6f %12.6f %12.6f\n" % tuple(vec_a))
        fh.write("%12.6f %12.6f %12.6f\n" % tuple(vec_b))
        fh.write("%12.6f %12.6f %12.6f\n" % tuple(vec_c))
        fh.writelines(poscar[5:])
    # Execute VASP
    subprocess.run(args.command)
    # Read total energy
    with open("OUTCAR", "r") as fh:
        for line in fh:
            if "TOTEN" in line:
                tmp = line.split("=")[1]
                energy = float(tmp.split()[0])
    # Count up iteration number
    icount += 1
    log.write(f"step={icount:6d}: {state} energy={energy:.6f}\n")
    log.flush()
    return energy


with open("POSCAR", "r") as fh:
    poscar = fh.readlines()
vec_a = np.fromstring(poscar[2], sep=" ", dtype=float)
vec_b = np.fromstring(poscar[3], sep=" ", dtype=float)
vec_c = np.fromstring(poscar[4], sep=" ", dtype=float)
var = []
if args.a:
    var.append(np.linalg.norm(vec_a))
if args.b:
    var.append(np.linalg.norm(vec_b))
if args.c:
    var.append(np.linalg.norm(vec_c))
var = tuple(var)

scipy.optimize.minimize(func, var,
                        #method="Nelder-Mead",
                        method="Powell",
                        options={'ftol': args.e,
                                 'disp': True,
                                 'maxfev': args.n})

log.close()



