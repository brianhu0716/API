# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 18:35:12 2021

@author: Brian Hu
"""
import sys
import os

sys.path.append("C:/Users/Brian Hu/Documents/GitHub/eda/src/time_frequency_analysis")
sys.path.append("C:/Users/Brian Hu/Documents/GitHub/eda/api")
os.chdir("C:/Users/Brian Hu/Desktop")

from TFA import TimeFrequencyAnalyze
import numpy as np
from enum import Enum
import pandas as pd

class FileExtension(Enum):
    CSV = 'csv'
    JSON = 'json'
    PARQUET = 'parquet'
    PICKLE = 'pkl'
    
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


def get_file_path(workdir, filename):
    folder_path = get_folder_path(workdir)
    filepath = os.path.join(folder_path, filename)
    return filepath

def pd_write_data(pd_data, workdir, filename, ext, **kwargs):
    filepath = get_file_path(workdir, filename)
    if ext == FileExtension.CSV.value:
        if 'index' in kwargs:
            kwargs.pop('index')
        pd_data.to_csv(filepath, index=False, **kwargs)
    elif ext == FileExtension.JSON.value:
        pd_data.to_json(filepath, **kwargs)
    elif ext == FileExtension.PARQUET.value:
        pd_data.to_parquet(filepath, **kwargs)
    elif ext == FileExtension.PICKLE.value:
        pd_data.to_pickle(filepath, **kwargs)
    else:
        raise ValueError

########################## FFT ###############################
HIDE_DISPLAY_PREFIX = '_'
FFT_PREFIX = HIDE_DISPLAY_PREFIX + "fft"

time = np.arange(0,1,1/100)
tfa = TimeFrequencyAnalyze(data = np.sin(2 * np.pi * 20 * time),time = time)
pd_spectrum, pd_frequency = tfa.FFT()

dataframe_list = [pd_spectrum, pd_frequency]
filename = "result"
workdir = "pd_write_data"
for count, value in enumerate(dataframe_list):
    pd_write_data(value, workdir, FFT_PREFIX + filename + "{} {}".format("_res_", count), ext=FileExtension.CSV.value)

########################## CWT ###############################

HIDE_DISPLAY_PREFIX = '_'
CWT_PREFIX = HIDE_DISPLAY_PREFIX + "cwt"


time = np.arange(0,1,1/100)
tfa = TimeFrequencyAnalyze(data = np.sin(2 * np.pi * 20 * time),time = time)
pd_spectrogram, pd_frequencies, pd_time = tfa.CWT()

'''
for index,row in pd_result.iterrows():
    print(index,row)
'''
filename = "result"
workdir = "pd_write_data"
dataframe_list = [pd_spectrogram, pd_frequencies, pd_time]
name = ["spectrogram","frequency","time"]
for count, value in enumerate(dataframe_list):
    pd_write_data(value, workdir, CWT_PREFIX + filename + "_" + name[count], ext = FileExtension.CSV.value)

########################## DWT #################################
HIDE_DISPLAY_PREFIX = '_'
DWT_PREFIX = HIDE_DISPLAY_PREFIX + "dwt"


time = np.arange(0,1,1/100)
tfa = TimeFrequencyAnalyze(data = np.sin(2 * np.pi * 20 * time),time = time)
pd_coeffs, pd_csv, pd_coeffs_csv = tfa.DWT(levels=4)


filename = "dwtresult"
workdir = "pd_write_data"
'''
dataframe_list = [pd_cA, pd_cD]

for count, value in enumerate(dataframe_list):
    print("count" ,count)
    print(value)
    pd_write_data(value, workdir, DWT_PREFIX + filename + "{} {}".format("_res_", count), ext = FileExtension.CSV.value)
'''
########################### EEMD #############################
HIDE_DISPLAY_PREFIX = '_'
EEMD_PREFIX = HIDE_DISPLAY_PREFIX + "eemd"


time = np.arange(0,1,1/100)
tfa = TimeFrequencyAnalyze(data = np.sin(2 * np.pi * 20 * time),time = time)
pd_IMF, pd_time = tfa.EEMD()


filename = "eemdresult"
workdir = "pd_write_data"
dataframe_list = [pd_IMF, pd_time]

for count, value in enumerate(dataframe_list):
    #print("count" ,count)
    #print(value)
    pd_write_data(value, workdir, EEMD_PREFIX + filename + "{} {}".format("_res_", count), ext = FileExtension.CSV.value)


############################# random forest ########################
HIDE_DISPLAY_PREFIX = '_'
RF_PREFIX = HIDE_DISPLAY_PREFIX + "rf"

metric_list = ['F1', 'Recall', 'Accuracy']
metric_score = [0.6, 0.67, 0.6]
pd_metric = pd.DataFrame({"metric": metric_list, "score": metric_score}).round(4)
#pd_metric = pd.DataFrame({"metric": metric_list, "score": metric_score},orient="index")

for index,row in pd_metric.iterrows():
    print(index,row)

filename = "rf_result"
workdir = "pd_write_data"
dataframe_list = [pd_metric]

for count, value in enumerate(dataframe_list):
    print("count" ,count)
    print(value)
    pd_write_data(value, workdir, RF_PREFIX + filename + "{} {}".format("_res_", count), ext = FileExtension.CSV.value)
