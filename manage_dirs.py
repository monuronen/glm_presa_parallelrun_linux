# These are the functions for managing directories for parallel processing

def find_and_delete_process_folders(directory):
    import os
    import shutil
    # List all items in the given directory
    items = os.listdir(directory)
    
    # Filter items to only include directories starting with "Process"
    process_folders = [item for item in items if os.path.isdir(os.path.join(directory, item)) and item.startswith("Process")]
    
    if process_folders:
        print("Found folders starting with 'Process':")
        for folder in process_folders:
            print(folder)
        
        # Ask the user for confirmation
        confirm = input("Do you want to delete all of these folders? [Y/N] ").upper()
        if confirm == 'Y':
            for folder in process_folders:
                shutil.rmtree(os.path.join(directory, folder))
                print(f"Deleted folder: {folder}")
            print("All specified folders have been deleted.")
        else:
            print("No folders have been deleted.")
    #else:
    #    print("No folders starting with 'Process' found.")

def extract_rar(rar_path, output_folder):
    import os
    import patoolib
    """Extracts a RAR file into the specified output directory."""
    try:
        if not os.path.isfile(rar_path):
            print(f"The file '{rar_path}' does not exist.")
            return None
        patoolib.extract_archive(rar_path, outdir=output_folder)
        print(f"Successfully extracted '{rar_path}' to '{output_folder}'")
        return output_folder
    except Exception as e:
        print(f"An error occurred while extracting '{rar_path}': {e}")
        return None

def copy_folder(src_folder, num_copies):
    import os
    import shutil
    """Creates copies of the specified folder, naming them Process_0, Process_1, etc."""
    if not os.path.isdir(src_folder):
        print(f"The directory '{src_folder}' does not exist.")
        return
    
    for i in range(num_copies):
        # Adjusted naming scheme here
        dst_folder = f"Process_{i:03}"
        try:
            shutil.copytree(src_folder, dst_folder)
            print(f"Successfully created copy: '{dst_folder}'")
        except Exception as e:
            print(f"An error occurred while copying '{src_folder}' to '{dst_folder}': {e}")

def remove_folder(folder_path):
    import os
    import shutil
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"The folder '{folder_path}' has been removed.")
        except Exception as e:
            print(f"An error occurred while removing the folder: {e}")
    else:
        print(f"The folder '{folder_path}' does not exist or is not a directory.")

def partition_csv(input_file, output_folder, output_prefix, num_partitions):

    import os
    import pandas as pd
    import time

    partitioned_csv_filenames = list()

    # Check if the output folder exists
    if not os.path.exists(output_folder):
        # If the folder does not exist, create it
        print(f'Output folder: "{output_folder}" does not exist')
        time.sleep(2)
        os.makedirs(output_folder)
        print(f'Output folder: "{output_folder}" has been created.')
        time.sleep(2)
    else:
        # If the folder exists, check if it's empty
        if os.listdir(output_folder):
            # If the folder is not empty, prompt the user to remove files
            remove_files = input(f"The folder '{output_folder}' is not empty. Do you want to remove existing files in the folder? (Y/N): ")
            if remove_files.upper() == 'Y':
                # If the user wants to remove files, delete all files under the folder
                for filename in os.listdir(output_folder):
                    file_path = os.path.join(output_folder, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                print(' ')
                print(f'All files in output folder: "{output_folder}" has been removed.')
                time.sleep(2)
            else:
                # If the user doesn't want to remove files, exit from the function
                print("Exited from the function without doing nothing.")
                return
    
    print(' ')
    print(f'Now partitioning "{input_file}" into {num_partitions} files')
    time.sleep(2)
    print(' ')

    # Read the original CSV file
    df = pd.read_csv(input_file)

    # Calculate number of rows per partition
    rows_per_partition = len(df) // num_partitions

    # Partition the DataFrame and save each partition to a separate CSV file
    for i in range(num_partitions):
        start_idx = i * rows_per_partition
        end_idx = (i + 1) * rows_per_partition if i < num_partitions - 1 else None
        partition_df = df.iloc[start_idx:end_idx]
        #output_file = os.path.join(output_folder, f'{output_prefix}_{i:03}.csv')
        output_file = output_folder + f'{output_prefix}_{i:03}.csv'
        partition_df.to_csv(output_file, index=False)
        print(f'{output_file} has been created.')
        partitioned_csv_filenames.append(output_file)

    print(' ')
    print('Partition is successful!')
    time.sleep(2)

    return partitioned_csv_filenames