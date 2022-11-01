# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from calendar import leapdays
from distutils.log import debug
from tkinter import *
import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from awscrt import mqtt
from flask import Flask, render_template, request
# from flask_ngrok import run_with_ngrok
# import numpy as np # for array operations
# import pandas as pd # for working with DataFrames
import requests, io # for HTTP requests and I/O commands
# import matplotlib.pyplot as plt # for data visualization
# %matplotlib inline
# import sys
# # scikit-learn modules
# # from sklearn.model_selection import train_test_split # for splitting the data
# from sklearn.metrics import mean_squared_error # for calculating the cost function
# from sklearn.ensemble import RandomForestRegressor # for building the model
# # import seaborn as sns
# # import matplotlib.pyplot as plt
# from sklearn import preprocessing, svm
# # from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# import pickle


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a1efhuyrjhdcnv-ats.iot.ap-northeast-1.amazonaws.com"
CLIENT_ID = "GUIHOME"
PATH_TO_CERTIFICATE = "certificates/ae72b5e7b0fb59c4073133dc1624e06333b99bb858823efba2513fed86d50cc0-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/ae72b5e7b0fb59c4073133dc1624e06333b99bb858823efba2513fed86d50cc0-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/AmazonRootCA1 (1).pem"
LED_STATE_OFF = "OFF"
LED_STATE_ON = "ON"
TOPIC = "GUIHOME/pub"
RANGE = 20

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

myAWSIoTMQTTClient.connect()
temperature = None
humidity = None

action = None
auto_on = False
dataq = {"humidity": 0, "temperature": 0}

def refresh(client, userdata, message):
    global humidity,temperature,dataq
    payload = message.payload.decode("utf-8")
    payload = json.loads(payload)
    humidity = payload['humidity']
    temperature = payload['temperature']
    dataq = {"humidity":humidity,"temperature":temperature}
    print(payload)
    
def LED_ON():
    print("led on")
    print('Begin Publish')
    message = {"LED" : "ON"}
    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'GUIHOME/pub")

    print('Publish End')

def LED_OFF():
    print("led off")
    print('Begin Publish')
    

    message = {"LED" : "OFF"}
    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'GUIHOME/pub")

    print('Publish End')



myAWSIoTMQTTClient.subscribe("ESPDHT/pub",1 ,refresh)


# from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
app = Flask(__name__)
# run_with_ngrok(app)


@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        if request.form.get('action1') == 'LED ON':
            print("led on")
            LED_ON()
        elif  request.form.get('action2') == 'LED OFF':
            print("led off")
            LED_OFF() # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template('index.html')

# @app.route('/home',methods=["GET","POST"])
# def home():
#     return render_template('home.html')

# @app.route("/check")
# def check():
# 	fs = int(request.args.get("fs"))
# 	r1 = request.args.get("r1")
# 	if r1 == "Yes":
# 		fu = 1
# 	else:
# 		fu = 0
# 	with open("model.pkl","rb") as f:
# 		model = pickle.load(f)
# 	res = model.predict([[fs,76]])
# 	msg = res[0]
# 	if msg == "YES":
# 		txt = "Unfortnately you have diabetes :("
# 	else:
# 		txt = "You dont have diabetes :)"
# 	return render_template("home.html", msg = res)


@app.route('/data', methods=["GET", "POST"])
def data():

    global dataq
 
    response = make_response(json.dumps(dataq))

    response.content_type = 'application/json'

    return response



if __name__ == "__main__":
    app.run(debug='true')
    # app.run(host='0.0.0.0',port = 5000)
myAWSIoTMQTTClient.disconnect()
