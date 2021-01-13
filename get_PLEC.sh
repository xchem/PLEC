#! /bin/bash

#$ -cwd
#$ -j y
#$ -N PLEC
#$ -o /dls/science/users/tyt15771/interactions/PLEC/PLEC.out

source /dls/science/users/tyt15771/miniconda3/etc/profile.d/conda.sh

conda activate oddt_pull
python PLEC.py -l $1 -p $2 -t $3
BACK_PID=$!
wait $BACK_PID
conda deactivate

conda activate pymol
python generate_complexes.py -l $1 -p $2 -t $3
conda deactivate
echo 'done'

