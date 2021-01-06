from means import dp_means
from rdkit import Chem
import json
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-t",
    "--target", required=True,
    )


args = vars(parser.parse_args())
target = args["target"]

def get_cofm(mol):
    m = mol.GetConformers()[0]
    x = sum([int(i[0]) for i in m.GetPositions()])
    y = sum([int(i[1]) for i in m.GetPositions()])
    z = sum([int(i[2]) for i in m.GetPositions()])
    num = len(m.GetPositions()[0])
    return x/num, y/num, z/num


PLEC = {}

dirname = f'{os.getcwd()}/{target}_complexes/'

for bit in os.listdir(dirname):

    lig_coms = []
    prot_coms = []

    for filename in sorted(os.listdir(f'{dirname}/{bit}')):
        if 'lig' in filename:
            mol = Chem.MolFromPDBFile(f'{dirname}/{bit}/{filename}')
            lig_coms.append(get_cofm(mol))

        elif 'prot' in filename:
            mol = Chem.MolFromPDBFile(f'{dirname}/{bit}/{filename}')
            prot_coms.append(get_cofm(mol))
  

    ligs = dp_means(lig_coms, 1.6)
    prots = dp_means(prot_coms, 1.6)

    id_pairs = []
    for i in range(len(ligs.dataClusterId)):
        id_pairs.append(f'{ligs.dataClusterId[i]}__{prots.dataClusterId[i]}')

    PLEC[bit] = len(set(id_pairs))

json.dump(PLEC, open('PLEC.json', 'w'))