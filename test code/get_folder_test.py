# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:30:54 2021

@author: Brian Hu
"""
import os
TEMP_FOLDER = os.path.join(os.getcwd(), 'temp_folder')

def get_folder_path(workdir):
    if workdir is None:
        raise ValueError
    if type(workdir) is not str:
        raise TypeError
    if workdir == '' or workdir == '/':
        raise ValueError
    folder_path = os.path.join(TEMP_FOLDER, workdir)
    return folder_path


def get_file_list(folder_name, ignore_prefix=True, prefix='_'):
    folder = get_folder_path(folder_name) # folder是現在工作路徑+temp_folder+folder_name
    #folder = folder_name
    print(folder)
    files = filter(lambda x: os.path.isfile(os.path.join(folder, x)), os.listdir(folder))
    files = list(files)
    files = [f for f in files if not f.startswith('.')]
    if ignore_prefix:
        files = [f for f in files if not f.startswith(prefix)]
    return files

print(get_folder_path("ubuntu-20.04-base"))

'''
import os, sys
path = "C:\\Users\\Brian Hu\\Documents\\Virtual Machines\\ubuntu-20.04-base"
dirs = os.listdir(path) # dirs是檔名
# ospath.isfile是檢查路徑+檔名是否是檔案，因此需要在檔名前加紹路徑
files = filter(lambda x: os.path.isfile(os.path.join(path, x)), os.listdir(path))
print(list(files))

for file in dirs:
   print (file)
'''

#f = get_file_list("C:/Users/Brian Hu/Documents/GitHub/eda/src")
