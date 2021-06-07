#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 17:26:56 2021

@author: brian
"""

from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/",methods = ["GET"])
def main() :
    return render_template("login.html")

@app.route("/login",methods = ["GET","POST"])
def login() :
    if request.method == "POST" :
        user = request.values["user"]
        return render_template("result.html", name = user)



if __name__ == "__main__" :
    app.run(debug = True)
    