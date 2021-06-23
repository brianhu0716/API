# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:13:14 2021

@author: Brian Hu
"""
from flask import Flask, request, redirect, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret" # encode type 
jwt = JWTManager(app)

# users: {name: password}
users = {"FelixHsiao" : 2345, "BrianHu" : 5678, "JerryLee" : 1234,}


@app.route('/signup/token', methods = ["POST"])
def SignUp():    
    payload = request.get_json()
    name = payload["user"]
    password = payload["password"]
    
    if not name or not password:
        return jsonify("invalid username or password")
    
    if name in users:
        return jsonify("username has been registered")
    
    users[name] = password
    access_token = create_access_token(identity=name) # encode token based on username
    return jsonify({"access token: ": str(access_token), # return the generated token so that we can use it in postman to verify the token function
                    "user database: ": users})

@app.route("/login/token", methods = ["POST"])
@jwt_required() 
# the user identity is included in token, so we don't need to pass username or 
# password again and the endpoint can decrypted token to get user's information 
# directly without another database to store them
def JWT_protected():
    current_user = get_jwt_identity()
    return jsonify("Hello " + current_user)

@app.route('/login/session', methods=["POST"])
def Sesseion_protected():
    payload = request.get_json()
    name = payload["user"]
    password = payload["password"]
    
    if not name and not password:
        return "invalid input string"
    
    if name not in users:
        return jsonify("you need to register first")
        
    if users[name] == password:
        return jsonify("Hello " + name)
    return jsonify("Authentication Failed")
    
    
    
if __name__ == "__main__":
    debug = True
    app.run()
        