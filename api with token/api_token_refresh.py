# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 13:57:40 2021

@author: Brian Hu
"""
import datetime
from jwt import decode, encode, ExpiredSignatureError
from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

data = pd.read_csv("C:\\Users\\Brian Hu\\Desktop\\temp_folder\\pd_write_data\\table.csv")
data = pd.DataFrame.to_json(data)

key = "secret"
algorithm = "HS256"
app = Flask(__name__)

user_database = dict()

def to_integer(time):
    ans = ""
    for char in str(time):
        if char.isnumeric():
            ans += char
        elif char == ".":
            return int(ans)

@app.route('/login', methods=["POST"])
def login():
    info = request.get_json()
    name = info["user"]
    password = info["password"]
    if name not in user_database:
        user_database[name] = password
    else:
        if password != user_database[name]:
            return jsonify("wrong password")
    # convert start time to int type expression, then put it in values of "exp"
    start = to_integer(datetime.datetime.utcnow() + datetime.timedelta(minutes=5))
    access_token = encode({"name": name,
                           "exp": start},
                           key, algorithm)
    return jsonify({"access token": access_token})


@app.route('/getData',methods=["POST"])
def getdata():
    # convert end time to int expression and compare it to the bound in "exp"
    payload = request.get_json()   
    access_token = payload["access token"]
    info = decode(access_token, key, algorithm)
    limit = info["exp"]
    if to_integer(datetime.datetime.utcnow()) > limit:
        return jsonify("this token has expired, please log in again")
    else:
        return data
if __name__ == "__main__":
    app.run(debug=True)