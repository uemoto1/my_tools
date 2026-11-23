#!/usr/bin/env python3
import os
import numpy as np
import ase.io, ase.mep, ase.optimize
import ase.geometry
import mace.calculators

def init_potential():
    return mace.calculators.mace_mp(
        model="medium-mpa-0",
        device="cpu", # "cpu" or "cuda" (for GPU)
        default_dtype="float32", # "float32" or "float64"
    )

initial = ase.io.read("00/POSCAR")
final = ase.io.read("12/POSCAR")
n_intermediate = 11 # Intermediate images
k = 5.0             # Spring constant (eV/Ang.^2)
fmax = 0.10         # Force threshold (eV/Ang.)
steps = 200         # Maximum optimization steps

images = [initial]
images += [initial.copy() for _ in range(n_intermediate)] 
images += [final]
neb = ase.mep.NEB(images, k=k, climb=True, parallel=True)
neb.interpolate(mic=True)
for image in images:
    image.calc = init_potential()
opt = ase.optimize.FIRE(neb)
converged = opt.run(fmax=fmax, steps=steps)
print(f"Converged: {converged}")

result = []
l = 0.0
for i in range(len(images)):
    if i > 0:
        dr = images[i].positions - images[i-1].positions
        v, d = ase.geometry.find_mic(dr, image.cell, image.pbc)
        l += np.linalg.norm(d)
    energy = images[i].get_potential_energy()
    result.append((l, energy))
    os.makedirs(f"{i:02d}", exist_ok=True)
    ase.io.write(f"{i:02d}/CONTCAR", images[i], direct=True)
    print(f"Image {i:02d}: length = {l:9.3f} Ang., energy = {energy:12.6f} eV")
np.savetxt("neb_path.txt", result, header="length(Ang.) energy(eV)")

