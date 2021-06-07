#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 20:20:06 2021

@author: brian
"""

from flask import Flask
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def index() :
    return "Hello Man"
@app.route("/user/<username>")
def username(username) :
    return "I am " + username
@app.route("/user/<int:age>")
def user_age(age) :
    return "I am " + str(age) + " years old"

if __name__ == '__main__':
    app.debug = True
    app.run()