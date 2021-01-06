import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument(
    "-t",
    "--target", required=True,
    )

parser.add_argument(
     "-d",
    "--dir", required=True,
    )


args = vars(parser.parse_args())
target = args["target"]
dirname = args["dir"]

for struc in os.listdir(dirname):
    lig = f'{dirname}/{struc}/{struc}.sdf'
    prot = f'{dirname}/{struc}/{struc}.pdb'
    os.system(f'bash get_PLEC.sh {lig} {prot} {target}')


os.system(f'python cluster.py -t {target}')