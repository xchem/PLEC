import oddt
from oddt import fingerprints
import json
import argparse
import os

def get_pdb_atom(filename, coords):

    atomlines = [i for i in open(filename, 'r').readlines() if i.startswith('HETATM') or i.startswith('ATOM')]

    for line in atomlines:
        if  float(line[30:38].strip()) == round(float(coords[0]), 3) and float(line[38:46].strip()) == round(float(coords[1]), 3) and float(line[46:54].strip()) == round(float(coords[2]), 3):

            return line[6:11].strip()
  

parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--lig_path", required=True,
    )
parser.add_argument(
    "-p",
    "--prot_path", required=True,
    )

parser.add_argument(
    "-t",
    "--target", required=True,
    )

args = vars(parser.parse_args())

ligfile = args["lig_path"]
protfile = args["prot_path"]
target = args["target"]
struc = os.path.split(ligfile)[-1].split('.')[0]

ligand = next(oddt.toolkit.readfile('pdb', ligfile)) ###hey
protein = next(oddt.toolkit.readfile('pdb', protfile))
protein.protein = True
info = {}
PLEC = fingerprints.PLEC(ligand, protein, 1, 5, bits_info=info, size=65536, sparse=False, count_bits=True, distance_cutoff=6.0)

bits = {}
for i in info:
    bits[str(i)] = []
    for j in range(len(info[i])):
        information = list(str(list(info[i])[j]).strip('PLEC_bit_info_record(').strip(')').split(', '))

        ligand_root = list(ligand.atom_dict[int(information[0].split('=')[1])][1])
        ligand_depth = int(information[1].split('=')[1])
        protein_root = list(protein.atom_dict[int(information[2].split('=')[1])][1])
        protein_depth = int(information[3].split('=')[1])

        ligand_root = get_pdb_atom(ligfile, ligand_root)
        protein_root = get_pdb_atom(protfile, protein_root)
        bits[str(i)].append([ligand_root, ligand_depth, protein_root, protein_depth])

json.dump(bits, open(f'bits/{struc}.json', 'w'))