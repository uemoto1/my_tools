import ase.io
import mace.calculators 

potential = mace.calculators.mace_mp(
    model="medium-mpa-0",       # MACE-MPA-0
    device="cuda",              # or "cpu"
    default_dtype="float64",    # or float32
)
atoms = ase.io.read("POSCAR") 
atoms.calc = potential

energy = atoms.get_potential_energy()
print("Total energy = %f [eV]" % energy)
