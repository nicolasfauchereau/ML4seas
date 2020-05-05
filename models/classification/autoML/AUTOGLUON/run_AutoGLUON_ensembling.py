#!/home/nicolasf/anaconda3/envs/ML/bin/python

import os
import sys
import pathlib
from subprocess import call

# define the current working directory, hard coded

pwd = pathlib.Path.home() / 'research' / 'Smart_Ideas' / 'code' / 'models' / 'classification' / 'autoML' / 'AUTOGLUON'


# define the conda environment to use

conda_env = 'ML'

# define the executables for papermill and nbconvert

papermill = f'/home/nicolasf/anaconda3/envs/{conda_env}/bin/papermill'

# input notebook

input_notebook = './AutoGLUON_ensembling.ipynb'

# PARAMETERS

# GCM

GCM = 'CMCC'

region_names = ['NNI','WNI','ENI','NSI','WSI','ESI']
var_name = 'TMEAN' # target variable name
target_type = 'cat3_categories'
skpca = True
standardized = False
shuffle = True

# now loop

for region_name in region_names:
    print(f"\n\nprocessing {region_name}\n\n")
    output_notebook = f"./AutoGLUON_ensembling_{GCM}_{region_name}_{var_name}_{target_type}.ipynb"
    cmd = f"{papermill} {input_notebook} {output_notebook} -p GCM {GCM} -p var_name {var_name} -p target_type {target_type} -p region_name {region_name} -p skpca True -p standardized False -p shuffle True"
    print(f"\n\nnow running {cmd}\n\n")
    r = call(cmd, shell=True)
    if pathlib.Path(output_notebook).exists():
        print(f"\n\nsuccessfully created {output_notebook}\n\n")
    else:
        print(f"\n\nunable to find {output_notebook}\n\n")