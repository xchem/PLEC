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

dirname = f'{os.path.dirname(os.getcwd())}/{target}_complexes/'
print(dirname)

PLEC = {}
PLEC_semi = {}

for bit in os.listdir(dirname):

    if len(os.listdir(f'{dirname}/{bit}')) > 2:
        lig_coms = []
        prot_coms = []


        for filename in sorted(os.listdir(f'{dirname}/{bit}')):

            if 'prot' in filename:
                prot_coms.append(get_com(filename))
            elif 'lig' in filename:
                lig_coms.append(get_com(filename))

        ligs = dp_means(lig_coms, 1.6)
        prots = dp_means(prot_coms, 1.6)

        id_pairs = []
        for i in range(len(ligs.dataClusterId)):
            id_pairs.append(f'{ligs.dataClusterId[i]}__{prots.dataClusterId[i]}')

        PLEC[bit] = len(set(id_pairs))

        xtals = set([i.split('_')[0] for i in os.listdir(f'{dirname}/{bit}')])

        semi_clusters = 0
        for xtal in xtals:
            lig_coms = []
            prot_coms = []


            for filename in sorted(os.listdir(f'{dirname}/{bit}')):

                if 'prot' in filename and xtal in filename:
                    prot_coms.append(get_com(filename))
                elif 'lig' in filename and xtal in filename:
                    lig_coms.append(get_com(filename))

        
            ligs = dp_means(lig_coms, 1.6)
            prots = dp_means(prot_coms, 1.6)

            id_pairs = []
            for i in range(len(ligs.dataClusterId)):
                id_pairs.append(f'{ligs.dataClusterId[i]}__{prots.dataClusterId[i]}')

            semi_clusters += len(set(id_pairs))

        PLEC_semi[bit] = semi_clusters
    
    else:
        PLEC[bit] = 1
        PLEC_semi[bit] = 1

    json.dump(PLEC, open(f'PLECs/{target}_PLEC.json', 'w'))
    json.dump(PLEC_semi, open(f'PLECs/{target}_PLEC_semi.json', 'w'))