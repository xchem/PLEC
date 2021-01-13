import argparse
import os
import subprocess

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
    print(struc)
    lig = f'{dirname}/{struc}/{struc}_lig.pdb' ###hey
    prot = f'{dirname}/{struc}/{struc}.pdb'
    # os.system(f'bash get_PLEC.sh {lig} {prot} {target}')
    command = f'module load global/cluster && qsub ./get_PLEC.sh {lig} {prot} {target}'
    subprocess.run(command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    executable='/bin/bash')


command = f'module load global/cluster && qsub ./cluster.sh {target}'
subprocess.run(command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    executable='/bin/bash')
