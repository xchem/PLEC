import oddt
from oddt import fingerprints
import json
import argparse

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

ligand = next(oddt.toolkit.readfile('sdf', ligfile))
protein = next(oddt.toolkit.readfile('pdb', protfile))
protein.protein = True
info = {}
PLEC = fingerprints.PLEC(ligand, protein, 1, 5, bits_info=info, size=65536, sparse=False, count_bits=True)

bits = {}
for i in info:
    bits[str(i)] = []
    for j in range(len(info[i])):
        information = list(str(list(info[i])[j]).strip('PLEC_bit_info_record(').strip(')').split(', '))

        ligand_root = int(information[0].split('=')[1])+1
        ligand_depth = int(information[1].split('=')[1])
        protein_root = int(information[2].split('=')[1])+1
        protein_depth = int(information[3].split('=')[1])

        bits[str(i)].append([ligand_root, ligand_depth, protein_root, protein_depth])

json.dump(bits, open('bits.json', 'w'))