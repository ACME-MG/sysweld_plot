
#%% Import libraries
import os
import h5py
#%% Function
def import_file(path,file_name):
    """
    This script imports the required results file.

    Required arguments:
        path: path to results file
        file_name: name of results file
    Returns:
        file: imported results file
    """
    home_path=os.getcwd() #get current path
    os.chdir(path) #change to path to results file
    file = h5py.File(file_name, 'r') #Read data from file
    os.chdir(home_path) #change back to original path
    print('File imported')

    return file 