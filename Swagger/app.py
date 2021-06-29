# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:08:04 2021

@author: Brian Hu
"""

import connexion

Id = {"fft_get": "fft_get"}
def search(ope):
    return Id[ope]

app = connexion.App(__name__, 
                    specification_dir='C:\\Users\\Brian Hu\\Documents\\GitHub\\eda')
app.add_api('analytic_platform.yml')
app.run(port=8080)
