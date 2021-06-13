# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 09:55:50 2021

@author: Brian Hu
"""

from flask import Flask,request,url_for
app = Flask(__name__)

@app.route("/")
def index():
    return "get data successfully"

@app.route('/tfa/fft',methods = ["POST"])
def ask_for_data():
    payload = request.get_json()
    print(payload["filename"])
    return url_for(index)

if __name__ == "__main__":
    debug = True
    app.run()
