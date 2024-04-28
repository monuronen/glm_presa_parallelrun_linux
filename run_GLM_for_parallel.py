# create function for parallel GLM execution with new parameters
def run_GLM_for_parallel(params, X_id, df_sim_csv_folder_url, container, nml_filename, exe_path, working_directory):

    import numpy as np
    import pandas as pd
    import netCDF4 as nc
    from datetime import datetime, timedelta
    from functions import write_dict_to_NML
    from functions import create_new_datetimeindex
    from functions import integer_to_five_digit_string

    # (1) update the parameters in the dictionary
    for i in range(container.params_N):
        container.nml_dict[container.params_section[i]][container.params_name[i]][container.params_id[i]] = params[i]

    # (2) create NML file from the updated dictionary
    write_dict_to_NML(nml_filename, container.nml_dict)

    # (3) Now, run glm.exe
    import subprocess

    try:
        # Run the executable and capture its output
        result = subprocess.run(exe_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, cwd = working_directory)
    
        # Print the standard output and standard error
        print("Standard Output:", result.stdout)
        print("Standard Error:", result.stderr)
    
        # Get the return code of the process
        return_code = result.returncode
        print("Return Code:", return_code)
    
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)

    # Now define the objective function(s) here.
    #OF = 5
    # (1) This part is to define the directory of nc file ##############################################
    DATA_AND_GLM_FOLDER_URL = working_directory
    nml_dict = container.nml_dict
    nc_filename = nml_dict['output']['out_fn'][0]
    nc_filename = nc_filename[1:-1]
    nc_dir = nml_dict['output']['out_dir'][0]
    nc_dir = nc_dir[1:-1]
    nc_directory = DATA_AND_GLM_FOLDER_URL + nc_dir + '/'
    nc_read_filename = nc_directory + nc_filename + '.nc'
    #print(nc_read_filename)
    #####################################################################################################
    # 2) This part is to read variables from nc file and reshape them to proper sizes ###################
    with nc.Dataset(nc_read_filename, 'r') as file:
        # Read the 'time' variable
        time = file.variables['time'][:]
        # Read the 'units' attribute from the 'time' variable
        time_units = file.variables['time'].units
        # Read the 'temp' variable
        temp = file.variables['temp'][:]
        # Read the 'salt' variable
        #salt = file.variables['salt'][:]
        # Read the 'z' variable (layer heights)
        z = file.variables['z'][:]
        # Read number of layers
        NS = file.variables['NS'][:]

    # Extract relevant parts of the time units string
    str_time_units = time_units[12:]
    #print(str_time_units)

    # Parse the year, month, day, hour, minute, and second from the time units string
    yr = int(str_time_units[0:4])
    mn = int(str_time_units[5:7])
    dy = int(str_time_units[8:10])
    hh = int(str_time_units[11:13])
    mm = int(str_time_units[14:16])
    ss = int(str_time_units[17:19])

    # Create a datetime object using the parsed values
    dt = datetime(yr, mn, dy, hh, mm, ss)
    #print(dt)

    # Add the 'time' values to the datetime object
    time = np.array(time)
    dt1 = [dt + timedelta(hours=t) for t in time]
    dt1 = pd.DatetimeIndex(dt1)
    Nt = len(time)

    _, Nz, _, _ = temp.shape
    #print(Nz)

    # Reshape 'temp', 'salt' and 'z' variables into [Nz,Nt] shape
    temp = np.array(temp.reshape(Nt, Nz))
    temp = np.transpose(temp)
    #salt = np.array(salt.reshape(Nt, Nz))
    #salt = np.transpose(salt)
    z = np.array(z.reshape(Nt, Nz))
    z = np.transpose(z)

    # Determine the lake water surface height (height of the top of the top layer from the lake bottom)
    z_LakeSurf = [z[NS[i]-1, i] for i in range(NS.shape[0])]
    z_LakeSurf = np.array(z_LakeSurf)
    #####################################################################################################
    # (3) Now establish an equally spaced grid coordinates ##############################################
    # having Nz rows (equally-spaced heights in meters) and Nt columns (timestamps in hours)

    # Define inputs
    depth_resolution = 0.05 # in meters
    maxH = 30  # max height in meters to be illustrated in the heatmap

    # First create the z-axis (equally spaced heights)
    z_grid = np.arange(0, maxH + depth_resolution, depth_resolution)

    # Create a mesh grid (X and Y) that will be used by griddedinterpolant and heatmapping process
    gt = np.arange(0, Nt)
    gz = z_grid
    X, Y = np.meshgrid(gt, gz) # X and Y grids will be used by griddedinterpolant (data extraction at certain depth)
    Nx = Y.shape[0]
    x_z_grid = Y # x_z_grid will be used during heatmap generation

    # Make all cells below the first lagrangian layer and above the water surface level NaN
    z_vec_mat = np.tile(z_LakeSurf, (Nx, 1))
    z_1_mat = np.tile(z[0, :], (Nx, 1))
    x_z_grid[x_z_grid > z_vec_mat] = np.nan
    x_z_grid[x_z_grid < z_1_mat] = np.nan
    #####################################################################################################
    # (4) CREATION OF NEW TIME INDEX ####################################################################
    # Now establish hourly timeseries in compliance with the ncfile's hourly frequency
    #Start_Date = date(2012, 1, 1)  # Beginning of the period of analysis (YYYY,M,D)
    Start_Date = dt1[0]             # Beginning of the period of analysis (YYYY,M,D)
    #End_Date = date(2022, 12, 31)  # End of the period of analysis (YYYY,M,D)
    End_Date = dt1[-1]              # End of the period of analysis (YYYY,M,D)
    TimeStepLength = 'Hourly'       # 'Monthly' or 'Daily' or 'Hourly'
    HowManyDays = 0                 # Enter a +integer if TimeStepLength is 'Daily'
    HowManyHours = 1                # Enter a +integer if TimeStepLength is 'Hourly'

    DateIndex1, DateIndex2 = create_new_datetimeindex(Start_Date, End_Date, TimeStepLength, HowManyDays, HowManyHours)

    # Now make sure new datetime time index and dt index of nc file are identical.
    if not DateIndex1.equals(dt1):
        raise('date_time_indexes of nc file and user-created one are not identical')
    #####################################################################################################
    # (5) Now transform lagrangian structured temperature information to uniform grid ###################
    temp_grid = x_z_grid * 1e6 # for error detection
    # #### OPTION 1: BUT IT TAKES TOO LONG (DON'T USE!!) ###############################

    # ####################################################################################
    # #### OPTION 2: VERY FAST (USE THIS!!) ###########################################
    # Precompute indices and slices
    id_Zwater = np.arange(0, np.max(NS))
    z_sliced = z[id_Zwater, :]
    temp_sliced = temp[id_Zwater, :]

    # Iterate over columns of x_z_grid
    for j in range(Nt):
        # Extract z_current and temp_current
        z_current = z_sliced[:, j]
        temp_current = temp_sliced[:, j]

        # Find indices where x_z_grid is not NaN
        valid_indices = ~np.isnan(x_z_grid[:, j])

        # Interpolate valid elements
        temp_grid[valid_indices, j] = np.interp(x_z_grid[valid_indices, j], z_current, temp_current)

        # Assign NaN to invalid elements
        temp_grid[~valid_indices, j] = np.nan
    #####################################################################################################
    # (5.1) plot heatmap of the uniformly gridded information (if necessary) ############################

    #####################################################################################################
    # (6) Now extract user-selected variable timeseries at a given height ###############################
    # height from the lake bottom (6.41 mAOD) in meters (this should be list!!!)
    query_heights = [14.6 - 6.41, 16 - 6.41, 10000]
    N_qh = len(query_heights)

    # Now we will query temperature values at the specified height with 2 options
    ########### OPTION 1: with standard interpolation ###########################
    # Preallocate an array filled with NaN values with specified shape
    shape = (Nt,N_qh)  # Shape of the array
    temp_at_query_height = np.full(shape, np.nan)
    # Preallocate the simulation results dataframe
    df_sim = pd.DataFrame({'StDate': DateIndex1, 'EndDate': DateIndex2})
    for j in range(N_qh):
        # Define a column title that includes variable name and query height
        if query_heights[j] > np.max(z_LakeSurf):
            column_title = "temp_SURFACE"
            temp_LakeSurf = [temp[NS[i]-1, i] for i in range(NS.shape[0])]
            temp_LakeSurf = np.array(temp_LakeSurf)
            df_sim[column_title] = temp_LakeSurf
        else:
            column_title = f"temp_{str(query_heights[j])}"
            # Query temperature at specified height for every timestep
            for t in range(Nt):
                # If the query height is larger than all water heights from the lake bottom
                # throughout the whole simulation period, this means the user queried
                # the temperature of the surface.
                # Let's take surface temp query height as 10 cm below the water surface level
                #if query_heights[j] > np.max(z_LakeSurf):
                #    query_heights[j] = z_LakeSurf[t] - 0.1
                temp_at_query_height[t,j] = np.interp(query_heights[j], gz, temp_grid[:,t])

            # Now store queried temp into a dataframe for simulated variables
            # df_sim = pd.DataFrame({'DateTime': dt1, 'Data': temp_at_query_height})
            # df_sim = pd.DataFrame({'StDate': DateIndex1, 'EndDate': DateIndex2, 'Simulated': temp_at_query_height})
            df_sim[column_title] = temp_at_query_height[:,j]
    

    str_X_id = integer_to_five_digit_string(X_id)

    df_sim_csv_filename = f"df_sim_{str_X_id}.csv"
    df_sim_csv_url = df_sim_csv_folder_url + df_sim_csv_filename
    df_sim.to_csv(df_sim_csv_url, index=False)
    #############################################################################

    return return_code
