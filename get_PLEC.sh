#! /bin/bash

source ~/miniconda3/etc/profile.d/conda.sh

conda activate oddt_pull
python PLEC.py -l $1 -p $2 -t $3
conda deactivate

conda activate pymol
python generate_complexes.py -l $1 -p $2 -t $3
conda deactivate

