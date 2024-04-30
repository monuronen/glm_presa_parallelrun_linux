## (Section 1) LOAD PACKAGES #########################################################################################

import os
import patoolib
import shutil
import numpy as np
import pandas as pd
import netCDF4 as nc
import time
from datetime import datetime, timedelta, date

## (Section 2) ENTER THE URL OF MAIN FOLDER and DEFINE THE NUMBER OF PARALLEL PROCESSES ##############################
''' MAIN_FOLDER should contain the following files:
     - Main.py (this file)
     - manage_dirs.py
     - run_GLM_for_parallel.py
     - tasks.py
     - functions.py
     - X.csv (Parameter values sampled by Salib sampling)
     - GLM_AND_DATA_ORIGINAL_ubuntu.rar '''

MAIN_FOLDER = '/home/monen/repositories/glm_presa_parallelrun_linux/'
N_processes = 4

Process_Folder_Names = [f'{MAIN_FOLDER}Process_{i:03}/' for i in range(N_processes)]

## (Section 3) DELETE PROCESS FOLDERS CREATED DURING THE PREVIOUS RUN OF THIS SCRIPT #################################
from manage_dirs import find_and_delete_process_folders
find_and_delete_process_folders(MAIN_FOLDER)

## (Section 4) EXTRACT GLM_AND_DATA_ORIGINAL.RAR AND MAKE COPY OF EXTRACTED FOLDER FOR EACH PROCESS ##################
from manage_dirs import extract_rar, copy_folder, remove_folder

# User input for the RAR file, output folder for extraction, and number of copies
rar_path = MAIN_FOLDER + 'GLM_AND_DATA_ORIGINAL_ubuntu.rar'
output_folder = MAIN_FOLDER
num_copies = int(N_processes)

# Extract the RAR file
extracted_folder = extract_rar(rar_path, output_folder)

# Create copies of the resulting folder, renaming them as specified
if extracted_folder:
    copy_folder(rar_path[:-4], num_copies)

# Finally remove the extracted folder
remove_folder(rar_path[:-4])

## (Section 5) PARTITION X.CSV INTO PARTITIONED CSV FILES ############################################################

partition_input_file = MAIN_FOLDER + 'X.csv' # this is the full X samples csv file
partition_outputs_folder = MAIN_FOLDER + 'Partitioned_CSVs/'
partition_output_prefix = 'XCSV'
num_partitions = int(N_processes)

from manage_dirs import partition_csv
partitioned_csv_filenames = partition_csv(partition_input_file, partition_outputs_folder, partition_output_prefix, num_partitions)

## (Section 6) CREATE STARTING NML DICTIONARY FROM ORIGINAL NML FILE AND READ START AND STOP DATES ###################

from functions import nml_to_numeric_dictionary
# Reading original nml file
original_nml_filename = Process_Folder_Names[0] + 'glm3_original_SA.nml'
nml_dict = nml_to_numeric_dictionary(original_nml_filename, 0)

## (Section 7) DEFINITION OF DECISION VARIABLES ######################################################################

import sys

# INPUTS-------------------------------------------------------------------------------------------------------
# what are the group titles of the decision variables in glm3.nml file (must be a list and order is important!)
#params_section = ['mixing','mixing','mixing','mixing','mixing','mixing','meteorology','meteorology','meteorology','meteorology','light','inflow','inflow','inflow','inflow','inflow','inflow','inflow','inflow','inflow','inflow']
params_section = ['mixing','mixing','mixing','mixing','mixing','mixing','light','meteorology','meteorology','meteorology']
# what are the names of the decision variables in glm3.nml file (must be a list and order is important!)
#params_name = ['coef_mix_KH','coef_mix_hyp','coef_mix_conv','coef_mix_turb','coef_wind_stir','coef_mix_shear','wind_factor','ce','ch','cd','Kw','coef_inf_entrain','strm_hf_angle','strm_hf_angle','strm_hf_angle','strmbd_slope','strmbd_slope','strmbd_slope','strmbd_drag','strmbd_drag','strmbd_drag']
params_name = ['coef_mix_KH','coef_mix_hyp','coef_mix_conv','coef_mix_turb','coef_wind_stir','coef_mix_shear','Kw','ce','ch','cd']
# In glm3.nml file some of the parameters may have multiple values (i.e. light_extc = 1.0, 0.5, 2.0, 4.0  ! Comma-separated list of light extinction coefficients for each waveband)
# So, what are the indexes of the decision variables in glm3.nml file (must be a list and order is important!)
#params_id = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 2, 0, 1, 2]
params_id = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#--------------------------------------------------------------------------------------------------------------

# Now check whether the number of params_section, params_name and params_id are equal
# Otherwise, raise error

if len(params_section) == len(params_name) and len(params_name) == len(params_id):
    params_N = len(params_section)
else:
    sys.exit('"params_section", "params_name" and "params_id" must have same length"')

# Now make a label for each user-defined parameter. Labels will be displayed as column titles in X.csv
params_label = []
for i in range(params_N):
    label = params_section[i][:3].upper() + '_' + params_name[i] + '_' + str(params_id[i])
    params_label.append(label)

## (Section 8) STORE ALL NECESSARY INFORMATION FOR UPDATING PARAMS AND RUNNING GLM ##################################
class make_container():
    def __init__(self, params_section, params_name, params_id, params_N, params_label, nml_dict):
        self.params_section = params_section
        self.params_name = params_name
        self.params_id = params_id
        self.params_N = params_N
        self.params_label = params_label
        self.nml_dict = nml_dict

container = make_container(params_section, params_name, params_id, params_N, params_label, nml_dict)

## (Section 9) EXECUTE PARALLEL COMPUTING ###########################################################################
import multiprocessing

from tasks import general_task

# Start the timer
tic = time.time()

if __name__ == "__main__":

    ## Define the arguments for each task, including the task type as the first argument
    #args1 = (0, Process_Folder_Names, partitioned_csv_filenames, container)
    #args2 = (1, Process_Folder_Names, partitioned_csv_filenames, container)
    #args3 = (2, Process_Folder_Names, partitioned_csv_filenames, container)
    #args4 = (3, Process_Folder_Names, partitioned_csv_filenames, container)

    # Create arguments for each task
    args_list = [(i, Process_Folder_Names, partitioned_csv_filenames, container) for i in range(N_processes)]

    # Create and start processes
    processes = []
    #for args in [args1, args2, args3, args4]:
    for args in args_list:
        p = multiprocessing.Process(target=general_task, args=args)
        p.start()
        processes.append(p)

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("All tasks completed")

# End the timer
toc = time.time()

# Calculate the elapsed time
elapsed_time = toc - tic

print("Elapsed time:", elapsed_time / 60, "minutes")

## (Section 10) TRANSFER RESULTS FROM LINUX TO WINDOWS ###############################################
# COPY MAIN FOLDER IN LINUX TO WINDOWS DESKTOP

import subprocess
destination_folder_url = '/mnt/c/Users/cip22moo/Desktop/'
command = ['cp','-r',MAIN_FOLDER, destination_folder_url]

print(f"Copying {MAIN_FOLDER} to {destination_folder_url}. Please Wait...")

# Execute the command
subprocess.run(command, check=True)

print(f"Copy from {MAIN_FOLDER} to {destination_folder_url} is complete")
print(' ')
print('You are all done =)')
