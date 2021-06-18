# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:03:12 2021
@author: Brian Hu
"""
import json
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
sys.path.append("C:\\Users\\Brian Hu\\Documents\\GitHub\\eda")

import numpy as np
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

from enum import Enum
from flask import request, jsonify, Flask, Blueprint, g

from utils import pd_read_data, pd_write_data, get_file_list, FileExtension, delete_data, HIDE_DISPLAY_PREFIX

from src.time_frequency_analysis.TFA import TimeFrequencyAnalyze 

'''
time = np.arange(0,1,1/100)
tfa = TimeFrequencyAnalyze(data = np.sin(2 * np.pi * 20 * time),time = time)
payload = tfa.FFT()
#payload.loc["spectrum"]
#payload.loc["frequency"]
'''

########################################################################
fs = 256
time = np.arange(0,2,1 / fs)
intervals = np.array([[i if 0.2 < i < 0.6 else 0 for i in np.arange(0,2,1/fs)],
             [i if 0.9 < i < 1.4 else 0 for i in np.arange(0,2,1/fs)]])
freq = [20,80]
pd_data = np.zeros(shape = len(time))
for i in range(len(freq)) :
    pd_data += np.sin(2 * np.pi * freq[i] * intervals[i])


##########################################################################

#HIDE_DISPLAY_PREFIX = '_'
FFT_PREFIX = HIDE_DISPLAY_PREFIX + "FFT" + '_'
DWT_PREFIX = HIDE_DISPLAY_PREFIX + "DWT" + '_'
CWT_PREFIX = HIDE_DISPLAY_PREFIX + "CWT" + '_'
EEMD_PREFIX = HIDE_DISPLAY_PREFIX + "EEMD" + '_'
SUCCESS_MESSAGE = 'Success'

class ReturnConst(Enum):
    MESSAGE = 'message'
    CODE = 'code'
    DATA = 'data'

def get_model_result_file(prefix):
    try:
        payload = request.get_json()
        workdir = payload["data"]["workdir"]
        filename = payload["data"]["filename"]
        message = SUCCESS_MESSAGE
        all_file_list = get_file_list(workdir, ignore_prefix=False, prefix=HIDE_DISPLAY_PREFIX)
        file_name = prefix + filename
        file_list = list()
        pd_data_list = list()
        for file in all_file_list:
            if file_name in file:
                file_list.append(file)
        for file in file_list:
            pd_data = pd_read_data(workdir, file, FileExtension.CSV.value)
            pd_data_list.append(pd_data)
    except Exception as e:
        message = repr(e)
    return pd_data_list, message

def get_model_delete_file(prefix):
    try:
        payload = request.get_json()
        workdir = payload["data"]["workdir"]
        filename = payload["data"]["filename"]
        message = SUCCESS_MESSAGE
        all_file_list = get_file_list(workdir, ignore_prefix=False, prefix=HIDE_DISPLAY_PREFIX)
        del_file_name = prefix + filename
        file_list = []
        for file in all_file_list:
            if del_file_name in file:
                file_list.append(file)
            for del_file in file_list:
                delete_data(workdir, del_file)
    except Exception as e:
        message = repr(e)
    return message

def get_workdir_filename():
    payload = request.get_json() # payload : dict()
    message = SUCCESS_MESSAGE
    workdir = payload["data"]["workdir"]
    filename = payload["data"]["filename"]
    ext = payload["data"]["ext"]
    return message, payload, workdir, filename, ext

app = Flask(__name__)

@app.route('/preprocess/tfa/fft', methods=["GET"])
def get_tfa_fft():
    pd_data_list, message = get_model_result_file(FFT_PREFIX) # pd_list,dataframe
    return {"message:" : message,
            "spectrum" : pd_data_list[0].to_dict(),
            "frequency" : pd_data_list[1].to_dict()}

@app.route('/preprocess/tfa/fft', strict_slashes=False, methods=['POST']) 
def ask_tfa_fft():
    try:
        message, payload, workdir, filename, ext = get_workdir_filename()
        # return jsonify({"workdir: ": workdir,
        #                 "filename: ": filename}) # --> receive json
        '''
        pd_data = pd_read_data(workdir, filename, ext)
        '''
        '''
        
        if "time" not in payload["args"]:
            time = None
        if "fs" not in payload["args"]:
            fs = None
        '''    
        tfa = TimeFrequencyAnalyze(pd_data, fs=fs, time=time)
        pd_spectrum, pd_frequency = tfa.FFT()
        
        dataframe_list = [pd_spectrum, pd_frequency]
        #return jsonify(pd_frequency)
        for count, value in enumerate(dataframe_list):
            pd_write_data(value, workdir, FFT_PREFIX + filename + "{} {}".format("_res_", count), ext)
    
    except Exception as e:
        message = repr(e)    
    return {ReturnConst.MESSAGE.value: message}

@app.route('/preprocess/tfa/fft', strict_slashes=False, methods=['DELETE'])
def delete_fft():
    message = get_model_delete_file(FFT_PREFIX)
    return {ReturnConst.MESSAGE.value: message}


@app.route('/preprocess/tfa/dwt', methods=["GET"])
def get_tfa_dwt():
    pd_data_list, message = get_model_result_file(DWT_PREFIX) # pd_list,dataframe
    return {"message:" : message,
            "coefficients" : pd_data_list[0].to_dict(),
            "time" : pd_data_list[1].to_dict()}

@app.route('/preprocess/tfa/dwt', strict_slashes=False, methods=['POST']) 
def ask_tfa_dwt():
    try:
        message, payload, workdir, filename, ext = get_workdir_filename()
        '''
        pd_data = pd_read_data(workdir, filename, ext)
        '''
        '''
        if "time" not in payload["args"]:
            time = None
        if "fs" not in payload["args"]:
            fs = None
        '''  
        tfa = TimeFrequencyAnalyze(pd_data, fs=fs, time=time)
        pd_coeffs, pd_time = tfa.DWT()
        
        dataframe_list = [pd_coeffs, pd_time]
        for count, value in enumerate(dataframe_list):
            pd_write_data(value, workdir, DWT_PREFIX + filename + "{} {}".format("_res_", count), ext)
    
    except Exception as e:
        message = repr(e)    
    return {ReturnConst.MESSAGE.value: message}

@app.route('/preprocess/tfa/dwt', strict_slashes=False, methods=['DELETE'])
def delete_dwt():
    message = get_model_delete_file(DWT_PREFIX)
    return {ReturnConst.MESSAGE.value: message}

@app.route('/preprocess/tfa/cwt', methods=["GET"])
def get_tfa_cwt():
    pd_data_list, message = get_model_result_file(CWT_PREFIX) # pd_list,dataframe
    return {"message:" : message,
            "spectrogram" : pd_data_list[0].to_dict(),
            "frequency" : pd_data_list[1].to_dict(),
            "time": pd_data_list[2].to_dict()}

@app.route('/preprocess/tfa/cwt', strict_slashes=False, methods=['POST']) 
def ask_tfa_cwt():
    try:
        message, payload, workdir, filename, ext = get_workdir_filename()
        '''
        pd_data = pd_read_data(workdir, filename, ext)
        '''
        '''
        if "time" not in payload["args"]:
            time = None
        if "fs" not in payload["args"]:
            fs = None
        '''    
        tfa = TimeFrequencyAnalyze(pd_data, fs=fs, time=time)
        pd_spectrogram, pd_frequencies, pd_time = tfa.CWT()
        
        dataframe_list = [pd_spectrogram, pd_frequencies, pd_time]
        for count, value in enumerate(dataframe_list):
            pd_write_data(value, workdir, CWT_PREFIX + filename + "{} {}".format("_res_", count), ext)
    
    except Exception as e:
        message = repr(e)    
    return {ReturnConst.MESSAGE.value: message}

@app.route('/preprocess/tfa/cwt', strict_slashes=False, methods=['DELETE'])
def delete_cwt():
    message = get_model_delete_file(CWT_PREFIX)
    return {ReturnConst.MESSAGE.value: message}


@app.route('/preprocess/tfa/eemd', methods=["GET"])
def get_tfa_eemd():
    pd_data_list, message = get_model_result_file(EEMD_PREFIX) # pd_list,dataframe
    return {"message:" : message,
            "IMF" : pd_data_list[0].to_dict(),
            "time" : pd_data_list[1].to_dict()}


@app.route('/preprocess/tfa/eemd', strict_slashes=False, methods=['POST']) 
def ask_tfa_eemd():
    try:
        message, payload, workdir, filename, ext = get_workdir_filename()
        '''
        pd_data = pd_read_data(workdir, filename, ext)
        '''
        '''
        if "time" not in payload["args"]:
            time = None
        if "fs" not in payload["args"]:
            fs = None
        '''    
        tfa = TimeFrequencyAnalyze(pd_data, fs=fs, time=time)
        pd_IMF, pd_time = tfa.EEMD()
        
        dataframe_list = [pd_IMF, pd_time]
        for count, value in enumerate(dataframe_list):
            pd_write_data(value, workdir, EEMD_PREFIX + filename + "{} {}".format("_res_", count), ext)
    
    except Exception as e:
        message = repr(e)    
    return {ReturnConst.MESSAGE.value: message}

@app.route('/preprocess/tfa/eemd', strict_slashes=False, methods=['DELETE'])
def delete_eemd():
    message = get_model_delete_file(EEMD_PREFIX)
    return {ReturnConst.MESSAGE.value: message}

'''
if __name__ == "__main__": 
    app.run(debug = True, use_reloader = False)
'''
app.run(debug = True, use_reloader = False)