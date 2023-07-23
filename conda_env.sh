#! /bin/sh
#conda update -n base -c defaults conda
#conda deactivate
conda remove --name pycom --all
conda env create -f conda.yml
conda activate pycom
