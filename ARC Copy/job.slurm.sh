#! /bin/bash
# ================================================
#SBATCH --job-name=sumo_test

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4gb
#SBATCH --time=0-168:00:00

# Specify a partiton if you want it.
#    #SBATCH --partition=parallel

# ================================================
# Run your commands here.
echo "Working directory: `pwd`."

module load sumo
module load python/anaconada3-2018.12

python main.py

echo "Job is done on `date`."