#%% Import libraries
import os
import h5py
#%% 
def import_file(path, file_name):
    """
    This script imports the required results file.

    Required arguments:
        path (string):      path to results file, e.g. 'C:/Users/...'
        file_name (string): name of results file
    Returns:
        file (HDF5 group):  imported results file
    """
    home_path=os.getcwd() #get current path
    os.chdir(path) #change to path to results file
    file = h5py.File(file_name, 'r') #Read data from file
    os.chdir(home_path) #change back to original path
    print('File imported')

    return file 
