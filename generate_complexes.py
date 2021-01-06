#! //Users/tyt15771/miniconda3/envs/pymol/bin/python

from pymol import cmd
import json
import os
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

lig = args["lig_path"]
prot = args["prot_path"]
target = args["target"]

bits = json.load(open('bits.json', 'r'))


dirname = f'{os.getcwd()}/{target}_complexes'

def extend_save(filepath, moltype, atom, depth, num, bit):
    struc = filepath.split('/')[-1].split('.')[0]
    cmd.reinitialize()
    cmd.load(filepath)
    cmd.select('root', f'index {atom}')
    cmd.select('ext', f'root extend {depth}')
    cmd.save(f'{dirname}/{bit}/{struc}_{moltype}{num}.pdb', 'ext')


for bit in bits:
    num = 0
    for pair in bits[bit]:

        if not os.path.isdir(f'{dirname}/{bit}'):
            os.mkdir(f'{dirname}/{bit}')
        lig_atom = pair[0]
        lig_depth = pair[1]
        prot_atom = pair[2]
        prot_depth = pair[3]

        extend_save(lig, 'lig', lig_atom, lig_depth, num, bit)
        extend_save(prot, 'prot', prot_atom, prot_depth, num, bit)

        num += 1


