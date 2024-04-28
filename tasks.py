def general_task(task_type, Process_Folder_Names, partitioned_csv_filenames, container):

    import time

    print(f"Starting task {task_type}")
    # Simulate a long-running task
    time.sleep(2)
    
    #if task_type == 0:
    #    # Task 0 logic
    #    #result = a + b + c + d + e
    #    task_per_process(0, Process_Folder_Names, partitioned_csv_filenames, container)
    #
    #elif task_type == 1:
    #    # Task 1 logic
    #    #result = a - b - c - d - e
    #    task_per_process(1, Process_Folder_Names, partitioned_csv_filenames, container)
    #
    #elif task_type == 2:
    #    # Task 2 logic
    #    #result = a * b * c * d * e
    #    task_per_process(2, Process_Folder_Names, partitioned_csv_filenames, container)
    #elif task_type == 3:
    #    # Task 3 logic
    #    #result = (a + b + c + d + e) / 5
    #    task_per_process(3, Process_Folder_Names, partitioned_csv_filenames, container)
    
    # Directly pass the task_type to your function
    task_per_process(task_type, Process_Folder_Names, partitioned_csv_filenames, container)
    
    print(f"Task {task_type} completed with success!")

def task_per_process(ii, Process_Folder_Names, partitioned_csv_filenames, container):

    from run_GLM_for_parallel import run_GLM_for_parallel
    import pandas as pd
    import subprocess

    DATA_AND_GLM_FOLDER_URL = Process_Folder_Names[ii]
    #original_nml_filename = DATA_AND_GLM_FOLDER_URL + 'glm3_original_SA.nml'
    new_nml_filename = DATA_AND_GLM_FOLDER_URL + 'glm3.nml'
    exe_path = DATA_AND_GLM_FOLDER_URL + 'glm'
    working_directory = DATA_AND_GLM_FOLDER_URL
    #GroundObs_FileName = 'WQ_GroundMeasurements/Alton_Raw_WaterTemperature_at_WTW_2012-2022.xlsx'
    #GroundObs_FileUrl = DATA_AND_GLM_FOLDER_URL + GroundObs_FileName
    df_sim_csv_folder_url = DATA_AND_GLM_FOLDER_URL + 'RESULTS/' # prepare folder for each parallel process

    csv_url = partitioned_csv_filenames[ii]
    X_df = pd.read_csv(csv_url)
    #print(X_df)
    array_X = X_df.iloc[:, 1:].values
    #print(array_X)
    X_id = list(X_df.iloc[:, 0].values)

    params_multi = array_X

    # Print the matrix
    #print(params_multi)

    # Initialise empty list in which error codes are to be recorded
    rtn_code_rec = list()

    # Initialise empty dataframes in which OF and X values are to be recorded
    # List of column names
    #F_column_names = ['max_err', 'mae', 'mape', 'mse', 'ssr', 'msle', 'rmse', 'rmsle', 'r', 'r2', 'nse', 'kge']
    X_column_names = container.params_label

    # Create empty X and F DataFrames with specified column names
    X_df = pd.DataFrame(columns=X_column_names)
    #F_df = pd.DataFrame(columns=F_column_names)

    # Now give permissions before the execution of glm for linux
    command = ['chmod', '+x', exe_path]

    # Execute the command
    subprocess.run(command, check=True)

    # Run the "run_GLM" function for the number of parameter sets
    for i in range(params_multi.shape[0]):
        X_list = params_multi[i].tolist()
        #OF, rtn_code = run_GLM(X_list, container, new_nml_filename, exe_path, working_directory, new_obs_df, 0)
        rtn_code = run_GLM_for_parallel(X_list, X_id[i], df_sim_csv_folder_url, container, new_nml_filename, exe_path, working_directory)
        #F_df.loc[len(F_df)] = OF
        X_df.loc[len(X_df)] = X_list
        #OF_rec.append(OF)
        rtn_code_rec.append(rtn_code)
        print(f"Process{ii} is {(i / (params_multi.shape[0]-1) * 100):.2f} % complete ...")

    df_return_code = pd.DataFrame(rtn_code_rec, columns=['return_code'])
    return_code_file_path = DATA_AND_GLM_FOLDER_URL + f"return_code_Process_{ii:03}.csv"
    df_return_code.to_csv(return_code_file_path, index=False)
    #print(rtn_code_rec)
    #print(F_df)
    #print(X_df)
    # Now write X_df and F_df to csv files
    Xcsv_file_path = DATA_AND_GLM_FOLDER_URL + f"X_Process_{ii:03}.csv"
    #Fcsv_file_path = DATA_AND_GLM_FOLDER_URL + 'F.csv'
    X_df.to_csv(Xcsv_file_path, index=False)
    print(f"X.csv has been generated at: {Xcsv_file_path}")
    #F_df.to_csv(Fcsv_file_path, index=False)
    #print(f"F.csv has been generated at: {Fcsv_file_path}")
