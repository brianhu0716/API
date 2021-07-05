# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:08:04 2021

@author: Brian Hu
"""

import connexion

def get_fft():
    return {"get_tfa_fft": "get_tfa_fft"}
def fft():
    return {"tfa_fft": "tfa_fft"}
def del_fft():
    return {"delete_tfa_fft": "delete_tfa_fft"}

# app = connexion.App(__name__, 
#                     specification_dir='C:\\Users\\Brian Hu\\Documents\\GitHub\\eda')
# app.add_api('analytic_platform.yml')

app = connexion.App(__name__,
                    specification_dir='C:\\Users\\Brian Hu\\Documents\\GitHub\API\\Swagger')
app.add_api('tfa.yaml')
app.run(port=8080)
