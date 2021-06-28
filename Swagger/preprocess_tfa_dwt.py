# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from . import Resource
from .. import schemas

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

import pandas as pd
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property


from apps.analytic_platform.utils import pd_read_data, pd_write_data, get_file_list, FileExtension, delete_data, HIDE_DISPLAY_PREFIX, get_tfa_result_file, get_workdir_filename, get_tfa_delete_file, ReturnConst

from src.time_frequency_analysis.TFA import TimeFrequencyAnalyze 

DWT_PREFIX = HIDE_DISPLAY_PREFIX + "DWT" + '_'
class PreprocessTfaDwt(Resource):

    def get(self):
        try:
            pd_data_list, message = get_tfa_result_file(DWT_PREFIX) # pd_list,dataframe
            return {"message:" : message,
                    "coefficients" : pd_data_list[0].to_dict(),
                    "time" : pd_data_list[1].to_dict()}, 200, None
        except Exception as e:
            return repr(e)


    def post(self):
        try:
            message, payload, workdir, filename, ext = get_workdir_filename()
            pd_data = pd_read_data(workdir, filename, ext)
            
            col_items = pd_data.columns
            if ("data" not in col_items) or ("time" not in col_items and "fs" not in col_items):
                raise "Error: Insufficient Information"
            if "fs" not in col_items:
                fs = None
            else:
                fs = pd.Series(pd_data["fs"]).to_numpy()[0]
            if "time" not in col_items:
                time = None
            else:
                time = pd.Series(pd_data["time"]).to_numpy()
            pd_data = pd.Series(pd_data["data"]).to_numpy()
            
            tfa = TimeFrequencyAnalyze(pd_data, fs=fs, time=time)
            pd_coeffs, pd_time = tfa.DWT()
            
            dataframe_list = [pd_coeffs, pd_time]
            for count, value in enumerate(dataframe_list):
                pd_write_data(value, workdir, DWT_PREFIX + filename + "{} {}".format("_res_", count), ext)
        except Exception as e:
            message = repr(e)    
        return {ReturnConst.MESSAGE.value: message}

    def delete(self):
        message = get_tfa_delete_file(DWT_PREFIX)
        return {ReturnConst.MESSAGE.value: message}, 200, None