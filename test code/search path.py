import os 
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
from utils import get_folder_path, get_file_path, pd_read_data, get_file_list

workdir = "temp"
filename = "tablw.csv."
ext = "csv"

all_file = get_file_list("temp", ignore_prefix=False, prefix='_')

#pd_read = get_file_path(workdir, filename)

#print(pd_read_data(workdir, filename, ext))