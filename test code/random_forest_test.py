# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:40:48 2021

@author: Brian Hu
"""
import json
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
import shutil
import pandas as pd
import uuid
import logging
import numpy as np
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property
from distutils.util import strtobool
from enum import Enum
from flask import request, jsonify, Flask, Blueprint, g
from werkzeug.utils import cached_property
from flask_restplus import Api
from utils import pd_read_data, pd_write_data, get_file_list, FileExtension, delete_data, HIDE_DISPLAY_PREFIX
from sklearn.model_selection import KFold
from src.model_selection.scorer import f1_macro, recall_macro
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score
from src.feature_transformation.factory import FeatureTransformerFactory
from src.feature_transformation.constant import NumFeatTransMethod, CatFeatTransMethod
from src.dimension_reduction.factory import FeatureDimensionReductionFactory
from src.dimension_reduction.constant import DimensionModel
from src.feature_selection.factory import FeatureSelectionFactory
from src.feature_selection.constant import FeatSelectionMethod
from src.classification.factory import CLFModelFactory
from src.regression.factory import REGRModelFactory
from src.regression.constant import REGRModelName
from src.model_selection.grid_search import GridSearch
from src.classification.constant import CLFResult, CLFModelName
from src.clustering.constant import ClusterModel
from src.clustering.factory import ClusterFactory
from src.utility.utils import go_to_project_root

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

cwd = os.getcwd()
go_to_project_root()
TEMP_FOLDER = os.path.join(os.getcwd(), 'temp_folder')
os.chdir(cwd)

logging_level = logging.INFO
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # make Han characters recognizable
app_healthcheck = Flask(__name__)
app_healthcheck.config['JSON_AS_ASCII'] = False

META_PREFIX = '_meta_'
SUMMARY_PREFIX = '_summary_'


RF_PREFIX = HIDE_DISPLAY_PREFIX + CLFModelName.RF.value + '_'
DT_PREFIX = HIDE_DISPLAY_PREFIX + CLFModelName.DT.value + '_'
XGB_PREFIX = HIDE_DISPLAY_PREFIX + CLFModelName.XGBOOST.value + '_'
SVC_PREFIX = HIDE_DISPLAY_PREFIX + CLFModelName.SVC.value + '_'
ADA_PREFIX = HIDE_DISPLAY_PREFIX + CLFModelName.ADABOOST.value + '_'
KNN_PREFIX = HIDE_DISPLAY_PREFIX + CLFModelName.KNN.value + '_'
MULTI_LINEAR_PREFIX = HIDE_DISPLAY_PREFIX + REGRModelName.MLR.value + '_'
STEPWISE_PREFIX = HIDE_DISPLAY_PREFIX + REGRModelName.STEPWISE.value + '_'
RIDGE_PREFIX = HIDE_DISPLAY_PREFIX + REGRModelName.RIDGE.value + '_'
LASSO_PREFIX = HIDE_DISPLAY_PREFIX + REGRModelName.LASSO.value + '_'
LOGISTIC_PREFIX = HIDE_DISPLAY_PREFIX + REGRModelName.LOGISTIC.value + '_'
KMEANS_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.K_MEANS.value + '_'
DBSCAN_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.DBSCAN.value + '_'
OPTICS_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.OPTICS.value + '_'
AFFINITY_PROPAGATION_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.AFFINITY_PROPAGATION.value + '_'
AGGLOMERATIVE_CLUSTERING_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.AGGLOMERATIVE_CLUSTERING.value + '_'
BIRCH_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.BIRCH.value + '_'
GAUSSIAN_MIXTURE_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.GAUSSIAN_MIXTURE.value + '_'
MEAN_SHIFT_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.MEAN_SHIFT.value + '_'
MINI_BATCH_KMEANS_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.MINI_BATCH_KMEANS.value + '_'
SPECTRAL_CLUSTERING_PREFIX = HIDE_DISPLAY_PREFIX + ClusterModel.SPECTRAL_CLUSTERING.value + '_'
SUCCESS_MESSAGE = 'Success'


# Below will be moved to config
version = 'v1'
repo_tag = 'latest'
server_url = '0.0.0.0'  # server URL
server_port = '30000'


class RouteConstant(Enum):
    INIT_AND_INFO = '/init_and_info/'
    API_DOC = '/apidoc/'
    PREFIX = '/api/{version}'
    VERSION = '/version/'


class ReturnConst(Enum):
    MESSAGE = 'message'
    CODE = 'code'
    DATA = 'data'


api = Api(app,
          ui=True,
          doc='{api_doc_route}'.format(api_doc_route=RouteConstant.API_DOC.value),
          version=version,
          title='AIE Analytic Platform API',
          description='AIE Analytic Platform API Documents',
          prefix=RouteConstant.PREFIX.value.format(version=version),
          # urls must start with a leading slash, and don't end with one
          default="",
          default_label="",
          strict_slashes=False,
          )


class InvalidUsage(Exception):
    status_code = '400'

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
        # return render_template('500.htm'), 500


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

def get_workdir_filename():
    payload = request.get_json()
    message = SUCCESS_MESSAGE
    workdir = payload["data"]["workdir"]
    filename = payload["data"]["filename"]
    ext = payload["data"]["ext"]
    return message, payload, workdir, filename, ext


@app.route('/modeling/clf/random_forest', strict_slashes=False, methods=['GET'])
def get_clf_random_forest():
    pd_data_list, message = get_model_result_file(RF_PREFIX)
    return {"message": message, "data": {"res1": pd_data_list[0].to_dict(), "res2": pd_data_list[1].to_dict(),
            "res3": pd_data_list[2].to_dict(), "res4": pd_data_list[3].to_dict()}}


@app.route('/modeling/clf/random_forest', strict_slashes=False, methods=['POST'])
def fit_clf_random_forest():
    try:
        message, payload, workdir, filename, ext = get_workdir_filename()
        pd_data = pd_read_data(workdir, filename, ext)

        clf_scorers = [f1_macro, accuracy_score, recall_macro]
        cv = KFold(n_splits=payload["hyper_params"]["cross_validation"], shuffle=True, random_state=42)

        # prepare model
        clf_model = CLFModelFactory(logging_level=logging_level).create(
            CLFModelName.RF.value,
            criterion=payload["hyper_params"]["criterion"],
            n_estimators=payload["hyper_params"]["n_estimators"],
            max_depth=payload["hyper_params"]["max_depth"],
            min_samples_split=payload["hyper_params"]["min_samples_split"],
            min_samples_leaf=payload["hyper_params"]["min_samples_leaf"]
        )

        # cross-validation
        gs = GridSearch(clf_model, clf_scorers, cv, {})
        pd_scores = gs.fit(pd_data.copy(), payload["data"]["features"].copy(), payload["data"]["response"])
        pd_scores.drop(columns=['parameter'], inplace=True)

        # fit the model
        pd_metric, pd_feature_importance, confusion_matrix, x_label, y_label = \
            clf_model.execute(pd_data, pd_data, payload["data"]["features"], payload["data"]["response"],
                              CLFResult.PRED_COL.value)
        pd_feature_importance.rename(columns={0: "Feature", 1: "Feature importance"}, inplace=True)
        confusion_matrix = pd.DataFrame(confusion_matrix, columns=x_label)
        confusion_matrix.insert(0, "", y_label)

        # save as file
        dataframe_list = [pd_metric, pd_feature_importance, confusion_matrix, pd_scores]
        for count, value in enumerate(dataframe_list):
            pd_write_data(value, workdir, RF_PREFIX + filename + "{} {}".format("_res_", count), ext)

    except Exception as e:
        message = repr(e)
    return {ReturnConst.MESSAGE.value: message}

'''
@app.route('/modeling/clf/random_forest', strict_slashes=False, methods=['DELETE'])
def delete_clf_random_forest():
    message = get_model_delete_file(RF_PREFIX)
    return {ReturnConst.MESSAGE.value: message}
'''

@app.route('/feat-eng/dim/pca', strict_slashes=False, methods=['POST'])
def dim_reduction_pca():
    try:
        payload = request.get_json()
        workdir = payload["data"]["workdir"]
        input_filename = payload["data"]["input_filename"]
        new_filename = payload["data"]["output_filename"]
        ext = payload["data"]["ext"]
        message = SUCCESS_MESSAGE
        if workdir is None:
            raise ValueError
        if input_filename is None:
            raise ValueError
        if new_filename is None:
            raise ValueError
        pd_data = pd_read_data(workdir, input_filename, ext)
        pca_model = FeatureDimensionReductionFactory(logging_level=logging_level). \
            create(DimensionModel.PCA.value, payload["features"])
        pd_result = pca_model.fit_transform(pd_data)
        pd_write_data(pd_result, workdir, new_filename, ext)
    except Exception as e:
        message = repr(e)
    return {ReturnConst.MESSAGE.value: message}