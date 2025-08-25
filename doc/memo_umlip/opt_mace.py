import ase.io, ase.optimize
import mace.calculators 

potential = mace.calculators.mace_mp(
    model="medium-mpa-0",       # MACE-MPA0
    device="cuda",              # or "cpu"
    default_dtype="float64",
)
atoms = ase.io.read("input.cif") 
atoms.calc = potential
dyn = ase.optimize.BFGS(atoms)
dyn.run(fmax=0.01)

ase.io.write("output.cif", atoms)
# ase.io.write("CONTCAR", atoms, sort=True)

