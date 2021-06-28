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

class PreprocessTfaCwt(Resource):

    def get(self):
        try:
            pd_data_list, message = get_model_result_file(CWT_PREFIX) # pd_list,dataframe
            return {"message:" : message,
                    "spectrogram" : pd_data_list[0].to_dict(),
                    "frequency" : pd_data_list[1].to_dict(),
                    "time": pd_data_list[2].to_dict()}, 200, None
        except Exception as e:
            return repr(e) 

    def post(self):

        return {'message': 'something'}, 200, None

    def delete(self):

        return {'message': 'something'}, 200, None