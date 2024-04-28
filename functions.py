def nash_sutcliffe_efficiency(observed, simulated):
    import numpy as np
    """
    Calculate Nash-Sutcliffe Efficiency (NSE).

    Parameters:
        observed (array-like): Array of observed values.
        simulated (array-like): Array of simulated values.

    Returns:
        float: Nash-Sutcliffe Efficiency (NSE) value.
    """
    obs_mean = np.mean(observed)
    numerator = np.sum((observed - simulated) ** 2)
    denominator = np.sum((observed - obs_mean) ** 2)
    nse = 1 - (numerator / denominator)
    return nse

def kling_gupta_efficiency(true_values, predicted_values):
    import numpy as np
    """
    Calculate Kling–Gupta Efficiency (KGE) between true and predicted values.

    Parameters:
        true_values (array-like): Array of true (observed) values.
        predicted_values (array-like): Array of predicted values.

    Returns:
        float: Kling–Gupta Efficiency (KGE) value.
    """
    # Calculate mean and standard deviation of true and predicted values
    mean_true = np.mean(true_values)
    mean_pred = np.mean(predicted_values)
    std_true = np.std(true_values)
    std_pred = np.std(predicted_values)

    # Calculate correlation coefficient (r)
    r = np.corrcoef(true_values, predicted_values)[0, 1]

    # Calculate bias ratio (β)
    beta = mean_pred / mean_true

    # Calculate variability ratio (γ)
    gamma = std_pred / std_true

    # Calculate Kling–Gupta Efficiency (KGE)
    kge = 1 - np.sqrt((r - 1)**2 + (beta - 1)**2 + (gamma - 1)**2)

    return kge

def sum_of_squared_residuals(true_values, predicted_values):

    import numpy as np
    """
    Calculate the sum of squared residuals (SSR) between true and predicted values.

    Parameters:
        true_values (array-like): Array of true (observed) values.
        predicted_values (array-like): Array of predicted values.

    Returns:
        float: Sum of squared residuals (SSR) value.
    """
    # Convert input arrays to numpy arrays
    true_values = np.array(true_values)
    predicted_values = np.array(predicted_values)
    
    # Calculate residuals (difference between true and predicted values)
    residuals = true_values - predicted_values
    
    # Calculate sum of squared residuals
    ssr = np.sum(residuals ** 2)
    
    return ssr

def write_dict_to_NML(output_NMLfilename, dictionary):
    ''' This function writes the information stored in a dictionary into an .nml file.
        output_NMLfilename : [string] user-defined file name of the output i.e. 'glm.nml'
        dictionary         : [dict]   dictionary variable that stores all GLM input NML file '''
    with open(output_NMLfilename, "w") as file:
        for section_name, section_data in dictionary.items():
            file.write(f"!-------------------------------------------------------------------------------\n")
            file.write(f"! {section_name}\n")
            file.write(f"!-------------------------------------------------------------------------------\n")
            file.write(f"&{section_name}\n")
            
            for key, value in section_data.items():
                if len(value) == 1:
                    file.write(f"   {key} = {value[0]}\n")
                else:
                    formatted_value = ", ".join(str(val) for val in value)
                    file.write(f"   {key} = {formatted_value}\n")
            
            file.write("/\n\n")
    
    print(f'File "{output_NMLfilename}" has been generated.')

def dict_2_prettytbl_general(dictionary):
    
    ''' This function displays the information stored in a dictionary in pretty table format.
        table_gen          : [table]  output general pretty table object
        dictionary         : [dict]   dictionary variable that stores all GLM input NML file '''
    
    from prettytable import PrettyTable
    
    # Create a table object
    table_gen = PrettyTable()

    # Set column names (dictionary keys)
    table_gen.field_names = ["Key", "Value"]

    # Add data to the table
    for key, value in dictionary.items():
        table_gen.add_row([key, value])

    # Print the table
    print(table_gen)
    #print(variables.items())
    return table_gen


def dict_2_prettytbl_sub(dictionary):
    
    ''' This function displays the information stored in a dictionary in pretty table format.
        table_sub          : [table]  output general pretty table object
        dictionary         : [dict]   dictionary variable that stores all GLM input NML file '''
    
    from prettytable import PrettyTable
    
    # Iterate through the main dictionary and create tables for each inner dictionary
    for inner_dict_name, inner_dict_data in dictionary.items():
        table_sub = PrettyTable()
        table_sub.field_names = ["Key", "Value"]
    
        for key, value in inner_dict_data.items():
            table_sub.add_row([key, value])
    
        print(f"Table for {inner_dict_name}:")
        print(table_sub)
        print()  # Add a blank line between tables

def print_dict_pretty_in_sep_cols(dict):

    from prettytable import PrettyTable

    table = PrettyTable()
    
    # Adding rows to the table
    for key, values in dict.items():
        table.add_row([key] + values)

    print(table)

####################### Below 2 functions for read_csv_to_dict ###################################
# def convert_to_numeric(value):
#     try:
#         # Try to convert the value to a numeric type (int or float)
#         return int(value) if float(value) == int(value) else float(value)
#     except ValueError:
#         # If conversion fails, return the original string
#         return value

def convert_to_numeric(value):
    try:
        # Try to convert the stripped value to a numeric type (int or float)
        return int(value.strip()) if float(value.strip()) == int(value.strip()) else float(value.strip())
    except ValueError:
        # # If conversion fails, return the original stripped string
        # print(value)
        # return value.strip()
        try:
            # Try to convert the stripped value to a float
            return float(value.strip())
        except ValueError:
            # If conversion fails, return the original stripped string
            return value.strip()

def read_csv_to_dict(csv_file):
    # this function is needed when aed_zoop_pars.nml or aed_phyto_pars.nml are not nml but csv files.

    import csv
    import sys
    
    result_dict = {}
    if 'phyto' in csv_file:
        class_name = 'phyto_data'
    elif 'zoop' in csv_file:
        class_name = 'zoop_params'
    elif 'bivalve' in csv_file:
        class_name = 'bivalve_params'
    elif 'sdg' in csv_file:
        class_name = 'sdg_params'
    elif 'sed_candi' in csv_file:
        class_name = 'sed_candi_params'
    elif 'malgae' in csv_file:
        class_name = 'malgae_data'
    elif 'macrophyte' in csv_file:
        class_name = 'macrophyte_data'
    elif 'pathogen' in csv_file:
        class_name = 'pathogen_data'
    else:
        sys.exit('csv file name must include either "phyto", "zoop", "bivalve"')
    
    result_dict[class_name] = {}

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file, quotechar='"')
        
        for row in csv_reader:
            # Use the first column as the key and the rest as values in a list
            key = row[0].strip()
            # now delete quotation marks and spaces
            key = key.replace('"', '').replace("'", '').replace(" ", '')

            #values = row[1:]
            
            # Convert the values to numeric if possible
            values = [convert_to_numeric(value) for value in row[1:]]
            
            # Create the dictionary entry
            result_dict[class_name][key] = values

    return result_dict

##################################################################################################

def write_dict_to_csv(output_csv_filename, input_dict, class_name):
    # this function is needed when aed_zoop_pars.nml or aed_phyto_pars.nml are not nml but csv files.

    import csv
    
    with open(output_csv_filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)

        # Write the dictionary values to the CSV file
        for key, values in input_dict[class_name].items():
            key1 = key
            key2 = "'" + key1 + "'" # adding quotation marks in key back to csv file
            row = [key2] + values
            csv_writer.writerow(row)
            
    print(f'File "{output_csv_filename}" has been generated.')

def nml_to_numeric_dictionary(filename, prnt):
    prnt = int(prnt)
    class_name = None
    variables_str = {}

    #filename = 'C:/Users/cip22moo/Projects/PyWR/PYWR_GLM_COUPLING_TRIAL/Run_GLM_from_Python/glm_latest/glm3_original_CoR.nml'
    #filename = "glm3.nml"
    #filename = 'C:/Users/cip22moo/Projects/PyWR/PYWR_GLM_COUPLING_TRIAL/Run_GLM_from_Python/glm_latest/glm3.nml'

    with open(filename, "r") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if prnt == 1:
            print(line)
        if not line.startswith('!'):
            #cleaned_line = line.split('!', 1)[0].strip()
            line = line.split('!', 1)[0].strip()
            if line.startswith('&'):
                class_name = line[1:].split()[0]
                variables_str[class_name] = {}
            elif line.startswith('/'):
                class_name = None
            elif '=' in line and class_name is not None:
                variable_name, value = map(str.strip, line.split('='))
                variables_str[class_name][variable_name] = value
    
    if prnt == 1:
        # Print extracted class names and their variables
        for class_name, class_variables in variables_str.items():
            print(f"Class: {class_name}")
            for variable_name, value in class_variables.items():
                print(f"  {variable_name}: {value}")
    
    # Now convert string dictionary to numeric
    import copy
    variables = copy.deepcopy(variables_str)
    for outer_key, inner_dict in variables.items():
        for key, value in inner_dict.items():
            inner_dict[key] = convert_value(value)
    
    if prnt == 1:
        print(variables)

    return variables


# This function converts string dictionary values to numeric
def convert_value(value):
    elements = [element.strip() for element in value.split(",")]
    converted_elements = []
    for element in elements:
        if element.isdigit():
            converted_elements.append(int(element))
        elif "." in element and all(part.isdigit() for part in element.split(".", 1)):
            converted_elements.append(float(element))
        else:
            converted_elements.append(element)
    return converted_elements


def transfer_data_to_newdf(Source_df, New_df, Stations, Variables, RenameNeeded, Rename_Variables, SaveToCSV, csv_file_path):
# EXTRACT GROUND OBSERVATIONS FROM THE WATER QUALITY DATASET AND
# TRANSFER EXTRACTED DATA TO A NEW DF WITH USER-GENERATED TIME INDEX
# THIS IS NEW VERSION AND 5 TIMES FASTER THAN OLDER VERSION !!! (USE THIS!!!)

# # INPUTS
# Source_df: Dataframe created by reading water quality dataset with no empty data rows
# New_df: New Dataframe to be filled with data transferred from Source_df. 
# ''' Enter variables and corresponding stations as they were written
#     in the excel files in the correct order.
    
#     Num. of stations and Num. of Variables must match.'''
# Stations = ['ALTON WATER RAW AT WORKS']
# Variables = ['TEMPERATURE C']
# ''' Name of the variables can be shortened with the following inputs.
#     * Renaming can be helpful to distinguish the same variables from
#     different stations or shorten full name of the variables
#     * Please pay attention to the order of the variables to be renamed '''
# RenameNeeded = 'Y' # Rename Needed?: 'Y' for YES or 'N' for NO 
# Rename_Variables = ['AltonWTW_RawWaterTemp']
# SaveToCSV = 'Y'    # 'Y' for YES or 'N' for NO
# csv_file_path = DATA_AND_GLM_FOLDER_URL + 'Hourly_WQ_GroundObs1.csv'

# -----------------------------------------------------------------------------
    import pandas as pd

    if RenameNeeded == 'N':
        Rename_Variables = Variables

    if len(Stations) != len(Variables) != len(Rename_Variables):
        raise Exception("Number of Stations, Variables, and Rename Variables must be equal")

    Nvar = len(Rename_Variables)

    # Extract unique dates for faster indexing
    unique_dates = Source_df['SampleEndDate'].unique()

    # Create a DataFrame with DateIndex1 and DateIndex2 columns
    new_df = pd.DataFrame({'StDate': DateIndex1, 'EndDate': DateIndex2})

    for j, (station, variable, rename_variable) in enumerate(zip(Stations, Variables, Rename_Variables)):
        id3 = Source_df['SamplePointFullName'] == station
        id4 = Source_df['MeasurableName'] == variable

        for i, (st, en) in enumerate(zip(new_df['StDate'], new_df['EndDate'])):
            id1 = Source_df['SampleEndDate'] >= st
            id2 = Source_df['SampleEndDate'] <= en
            idC = id1 & id2 & id3 & id4
            mean_value = Source_df.loc[idC, 'Value'].mean()
            new_df.loc[i, rename_variable] = mean_value

    # Save the DataFrame to a CSV file
    if SaveToCSV == 'Y':
        new_df.to_csv(csv_file_path, index=False)
        print(f"CSV file has been generated at: {csv_file_path}")
    
    return new_df

def create_new_obs_df_and_csv(raw_obs_df, start_time, stop_time, TimeStepLength, HowManyDays, HowManyHours, Stations, Variables, RenameNeeded, Rename_Variables, SaveToCSV, csv_file_path):

    # This function extracts ground observations from a raw water quality dataframe and
    # rearranges it into a new dataframe with an n-daily or n-hourly time index

    # While rearranging, multiple observations that fall into the same timestamp will be averaged.
    
    # This function is the new version of its kind and 5x faster than the old version !!!

    # # INPUTS
    # raw_obs_df : (df) A dataframe created by reading water quality dataset with no empty data rows
    #              i.e. "Alton_Raw_WaterTemperature_at_WTW_2012-2022.xlsx"
    # start_time : (datetime) Time that the new dataframe is commencing with
    #              i.e 2008-01-01 00:00:00
    # stop_time : (datetime) Time that the new dataframe ends
    #              i.e 2018-12-31 00:00:00
    #
    # TimeStepLength : (string) 'Monthly' or 'Daily' or 'Hourly'
    # HowManyDays : (integer) Enter a +integer if TimeStepLength is 'Daily'
    # HowManyHours : (integer) Enter a +integer if TimeStepLength is 'Hourly'
    #
    # Stations : (a list of strings) Names of the measurement location
    #              i.e. ['ALTON WATER RAW AT WORKS']
    # Variables : (a list of strings) Names of the variables to be extracted
    #              i.e. ['TEMPERATURE C']
    #            *  Note : Num. of stations and Num. of Variables must match!
    #            ** Note : Please pay attention to the order of stations and corresponding variables
    #
    # RENAMING ==> Name of the variables can be shortened with the following inputs.
    #     * Renaming can be helpful to distinguish the same variables from
    #       different stations or shorten full name of the variables
    #     * Please pay attention to the order of the order of the variables and 
    #       corresponding Rename_Variables
    #
    # RenameNeeded : (string) 'Y' for YES to allow renaming variables, otherwise 'N' for NO
    # Rename_Variables : (a list of strings) Names to update the existing variable names
    #                     i.e. ['AltonWTW_RawWaterTemp']
    #
    # SAVING NEW DATAFRAME TO CSV
    # SaveToCSV : (string) 'Y' for YES to allow saving new dataframe into a csv file, otherwise 'N' for NO
    # csv_file_path : (string) url of the csv file where the newdatframe will be saved.

    import pandas as pd
    from datetime import date

    if RenameNeeded == 'N':
        Rename_Variables = Variables

    if len(Stations) != len(Variables) != len(Rename_Variables):
        raise Exception("Number of Stations, Variables, and Rename Variables must be equal")

    Start_Date = date(start_time.year, start_time.month, start_time.day)
    End_Date = date(stop_time.year, stop_time.month, stop_time.day)

    DateIndex1, DateIndex2 = create_new_datetimeindex(Start_Date, End_Date, TimeStepLength, HowManyDays, HowManyHours)

    # Create a DataFrame with DateIndex1 and DateIndex2 columns
    new_obs_df = pd.DataFrame({'StDate': DateIndex1, 'EndDate': DateIndex2})

    for j, (station, variable, rename_variable) in enumerate(zip(Stations, Variables, Rename_Variables)):
        id3 = raw_obs_df['SamplePointFullName'] == station
        id4 = raw_obs_df['MeasurableName'] == variable

        for i, (st, en) in enumerate(zip(new_obs_df['StDate'], new_obs_df['EndDate'])):
            id1 = raw_obs_df['SampleEndDate'] >= st
            id2 = raw_obs_df['SampleEndDate'] <= en
            idC = id1 & id2 & id3 & id4
            mean_value = raw_obs_df.loc[idC, 'Value'].mean()
            new_obs_df.loc[i, rename_variable] = mean_value

    # Save the DataFrame to a CSV file
    if SaveToCSV == 'Y':
        new_obs_df.to_csv(csv_file_path, index=False)
        print(f"CSV file has been generated at: {csv_file_path}")

    return new_obs_df

def create_new_datetimeindex(Start_Date, End_Date, TimeStepLength, HowManyDays, HowManyHours):

    import pandas as pd
    #from datetime import datetime, timedelta, date

    # CREATION OF NEW TIME INDEX
    # Now establish hourly timeseries in compliance with the ncfile's hourly frequency
    # INPUTS:
    # Start_Date = date(2012, 1, 1)  # Beginning of the period of analysis (YYYY,M,D)
    # End_Date = date(2022, 12, 31)   # End of the period of analysis (YYYY,M,D)
    # TimeStepLength = 'Hourly'     # 'Monthly' or 'Daily' or 'Hourly'
    # HowManyDays = 1               # Enter a +integer if TimeStepLength is 'Daily'
    # HowManyHours = 1               # Enter a +integer if TimeStepLength is 'Hourly'

    # OUTPUTS:
    # DateIndex1: Starting time instance of the timestep
    # DateIndex1: Ending time instance of the timestep

    if TimeStepLength == 'Monthly':
        DateIndex1 = pd.date_range(Start_Date, End_Date, freq="MS", inclusive="both")
        DateIndex2 = pd.date_range(Start_Date, End_Date, freq="M", inclusive="both")
        DateIndex2 = DateIndex2 + pd.Timedelta(hours = 23, minutes = 59, seconds = 59)
    elif TimeStepLength == 'Daily':
        StepSizeStr = str(HowManyDays) + 'D'
        DateIndex1 = pd.date_range(Start_Date, End_Date, freq = StepSizeStr, inclusive="both")
        DateIndex2 = DateIndex1 + pd.Timedelta(days = HowManyDays - 1, hours = 23, minutes = 59, seconds = 59)
    elif TimeStepLength == 'Hourly':
        StepSizeStr = str(HowManyHours) + 'H'
        DateIndex1 = pd.date_range(Start_Date, End_Date, freq = StepSizeStr, inclusive="both")
        DateIndex2 = DateIndex1 + pd.Timedelta(days = 0, hours = HowManyHours - 1, minutes = 59, seconds = 59)
    
    return DateIndex1, DateIndex2

def integer_to_five_digit_string(number):
    # Check if the number has more than 5 digits
    if number > 99999 or number < 0:
        raise ValueError("The integer must be between 0 and 99999, inclusive.")
    
    # Convert to a 5-digit string with leading zeros
    return f"{number:05}"