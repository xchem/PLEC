from pymol import cmd
import json
import os
import argparse
import math

def extend_save(filepath, moltype, atom, depth, num, bit):
    struc = filepath.split('/')[-1].split('.')[0]
    cmd.reinitialize()
    cmd.load(filepath)
    cmd.select('root', f'index {atom}')
    coords = cmd.get_coords('root', 1)
    cmd.select('ext', f'root extend {depth}')
    cmd.save(f'{dirname}/{bit}/{struc}_{moltype}{num}.pdb', 'ext')
    return coords[0]

def dist(a, b):
    return math.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])**2 +
        (a[2]-b[2])**2
    )

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

lig = args["lig_path"]
prot = args["prot_path"]
target = args["target"]
struc = os.path.split(lig)[-1].split('.')[0]

bits = json.load(open(f'bits/{struc}.json', 'r'))

dirname = f'{os.path.dirname(os.getcwd())}/{target}_complexes'
print(dirname)
if not os.path.isdir(dirname):
    os.mkdir(dirname)

for bit in bits:
    num = 0
    for pair in bits[bit]:

        if not os.path.isdir(f'{dirname}/{bit}'):
            os.mkdir(f'{dirname}/{bit}')
            
        lig_atom = pair[0]
        lig_depth = pair[1]
        prot_atom = pair[2]
        prot_depth = pair[3]

        lig_pos = extend_save(lig, 'lig', lig_atom, lig_depth, num, bit)
        prot_pos = extend_save(prot, 'prot', prot_atom, prot_depth, num, bit)

        num += 1

        d = dist(lig_pos, prot_pos)
        if d > 6.1:
            raise ValueError

    
print('complexes generated')