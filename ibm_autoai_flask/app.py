import numpy as np
from flask import Flask, request, jsonify, render_template
import requests

import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "iCtSN6ILgqr5TlSlYEhkzxSBRVM_PAwFbtjzCMmM4y22"
token_response = requests.post('https://iam.ng.bluemix.net/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    
    geography = request.form["geography"]
    gender = request.form["gender"]
    age = request.form["age"]
    tenure = request.form["tenure"]
    creditscore = request.form["creditscore"]
   
    balance = request.form["balance"]
    noof = request.form["no of"]
    hascreditcard = request.form["has credit card"]
    isactivemember = request.form["is active member"]
    estimatedsalary = request.form["estimated salary"]
  
   

    if (geography == "Spain"):
        s1,s2,s3 = 0,0,1
    if (geography == "Germany"):
        s1,s2,s3 = 0,1,0
    if (geography == "Newyork"):
        s1,s2,s3 = 0,1,0
    
    if (gender == "female"):
        gender = 0
    if (gender == "male"):
        gender = 1
         
    if (isactivemember == "no"):
        isactivemember = 0
    if (isactivemember == "yes"):
        isactivemember = 1
         
    if ( hascreditcard == "no"):
        hascreditcard = 0
    if ( hascreditcard == "yes"):
         hascreditcard = 1
    
    t = [[int(s1),int(s2),int(s3),int(creditscore),int(gender),int(age),int(tenure),int(balance),int(noof),int(hascreditcard),int(isactivemember),int(estimatedsalary)]]
    print(t)
    payload_scoring = {"input_data": [ {"field": [["G1","G2","G3","CreditScore","Gender","Age","Tenure",	"Balance",	"NumOfProducts",	"HasCrCard",	"IsActiveMember",	"EstimatedSalary"]],
                   "values": t}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7753c081-b55b-4021-a33c-bf6165aed208/predictions?version=2020-12-26', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    if(pred == 0):
        output = "he will not get exited"
        print("he will not get exited")
    else:
        output = "he getssexited"
        print("he gets exited")
    return render_template('index.html', prediction_text= output)


if __name__ == "__main__":
    app.run(debug=True)
