from means import dp_means
import json
import os
import argparse
from pymol import cmd

parser = argparse.ArgumentParser()

parser.add_argument(
    "-t",
    "--target", required=True,
    )


args = vars(parser.parse_args())
target = args["target"]

def get_com(filename):
    cmd.reinitialize()
    cmd.load(f'{dirname}/{bit}/{filename}')
    return cmd.centerofmass()

dirname = f'{os.getcwd()}/{target}_complexes/'

PLEC = {}

for bit in os.listdir(dirname):

    lig_coms = []
    prot_coms = []


    for filename in sorted(os.listdir(f'{dirname}/{bit}')):

        try:
            if 'prot' in filename:
                prot_coms.append(get_com(filename))
            elif 'lig' in filename:
                lig_coms.append(get_com(filename))

            
        except IndexError:
            print(bit, filename)
    

    ligs = dp_means(lig_coms, 1.6)
    prots = dp_means(prot_coms, 1.6)

    id_pairs = []
    for i in range(len(ligs.dataClusterId)):
        id_pairs.append(f'{ligs.dataClusterId[i]}__{prots.dataClusterId[i]}')

    PLEC[bit] = len(set(id_pairs))

json.dump(PLEC, open('PLEC.json', 'w'))