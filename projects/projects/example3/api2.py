#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 18:40:14 2021

@author: brian
"""

from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
     name = request.args.get('name')
     return 'My name is {}'.format(name)
# http://127.0.0.1:8000/?name=Brian

if __name__ == '__main__':
     app.run(host='127.0.0.1', port=8000)