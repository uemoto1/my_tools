import ase.io, ase.md.npt, ase.units
import mace.calculators

potential = mace.calculators.mace_mp(
    model="medium-mpa-0", device="cuda", default_dtype="float32"
)
atoms = ase.io.read("POSCAR")
atoms.calc = potential
dyn = ase.md.npt.NPT(
    atoms,
    timestep=1.0*ase.units.fs,
    temperature_K=1000.0,
    pfactor=None,
    ttime=25.0*ase.units.fs,
    logfile="md.txt",
    trajectory="md.traj",
    loginterval=20
)
dyn.run(200)
ase.io.write("CONTCAR", atoms)

