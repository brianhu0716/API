# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 21:12:51 2021

@author: Brian Hu
"""

from flask import Flask,render_template,request

app=Flask(__name__)
@app.route('/index',methods=['POST','GET'])
def index():
	if request.method =='POST':
		if request.values['send']=='送出':
			return render_template('index.html',name=request.values['user'])
	return render_template('index.html',name="")

if __name__ == '__main__':
	app.run()