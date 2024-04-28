This folder is created for

## (Section 1) LOAD PACKAGES

## (Section 2) ENTER THE URL OF MAIN FOLDER and DEFINE THE NUMBER OF PARALLEL PROCESSES ##############################
''' MAIN_FOLDER should contain the following files:
     - Main.py (this file)
     - manage_dirs.py
     - run_GLM_for_parallel.py
     - tasks.py
     - functions.py
     - X.csv (Parameter values sampled by Salib sampling)
     - GLM_AND_DATA_ORIGINAL_ubuntu.rar '''

MAIN_FOLDER = '/home/monen/PreSA_parallel_process/'
N_processes = 4

## (Section 3) DELETE PROCESS FOLDERS CREATED DURING THE PREVIOUS RUN OF THIS SCRIPT

## (Section 4) EXTRACT GLM_AND_DATA_ORIGINAL.RAR AND MAKE COPY OF EXTRACTED FOLDER FOR EACH PROCESS

## (Section 5) PARTITION X.CSV INTO PARTITIONED CSV FILES

## (Section 6) CREATE STARTING NML DICTIONARY FROM ORIGINAL NML FILE

## (Section 7) DEFINITION OF DECISION VARIABLES                                                                                                                                                                                                  import sys                                                                                                                                                                                                                                                                                                              # INPUTS-------------------------------------------------------------------------------------------------------                                             # what are the group titles of the decision variables in glm3.nml file (must be a list and order is important!)                                             #params_section = ['mixing','mixing','mixing','mixing','mixing','mixing','meteorology','meteorology','meteorology','meteorology','light','inflow','inflow',>params_section = ['mixing','mixing','mixing','mixing','mixing','mixing']                                                                                    # what are the names of the decision variables in glm3.nml file (must be a list and order is important!)                                                    #params_name = ['coef_mix_KH','coef_mix_hyp','coef_mix_conv','coef_mix_turb','coef_wind_stir','coef_mix_shear','wind_factor','ce','ch','cd','Kw','coef_inf_>params_name = ['coef_mix_KH','coef_mix_hyp','coef_mix_conv','coef_mix_turb','coef_wind_stir','coef_mix_shear']                                              # In glm3.nml file some of the parameters may have multiple values (i.e. light_extc = 1.0, 0.5, 2.0, 4.0  ! Comma-separated list of light extinction coeffi># So, what are the indexes of the decision variables in glm3.nml file (must be a list and order is important!)

# what are the group titles of the decision variables in glm3.nml file (must be a list and order is important!)
params_section = ['mixing','mixing','mixing','mixing','mixing','mixing']

# what are the names of the decision variables in glm3.nml file (must be a list and order is important!)
params_name = ['coef_mix_KH','coef_mix_hyp','coef_mix_conv','coef_mix_turb','coef_wind_stir','coef_mix_shear']

# In glm3.nml file some of the parameters may have multiple values (i.e. light_extc = 1.0, 0.5, 2.0, 4.0  ! Comma-separated list of light extinction coefficients for each waveband)
# So, what are the indexes of the decision variables in glm3.nml file (must be a list and order is important!)
params_id = [0, 0, 0, 0, 0, 0]

## (Section 8) STORE ALL NECESSARY INFORMATION FOR UPDATING PARAMS AND RUNNING GLM ##################################
