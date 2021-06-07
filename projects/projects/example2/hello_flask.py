#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 23:04:58 2021

@author: brian
"""
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/<user>')
def index(user):
    return render_template('abc.html',user_template = user)

if __name__ == '__main__':
    app.debug = True
    app.run()