import numpy as np
from flask import Flask, request, jsonify, render_template
import requests

import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "OqEsLaZK9LASCFmiJIm5aXJttmURT4x0KwPc3KAKLrP6"
token_response = requests.post('https://iam.eu-gb.bluemix.net/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
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
    
    city = request.form["city"]
    month = request.form["month"]
    day = request.form["day"]
    year = request.form["year"]
    
    if city="bombay":
    	o1,o2=0,0
    elif city="calcutta":
    	o1,o2=0,1
    elif city="chennai":
    	o1,o2=1,0
    elif city="delhi":
    	o1,o2=1,1


    t = [[o1,o2,int(month),int(day),int(year)]]
    print(t)
    payload_scoring = {"input_data": [ {"field": [["city","month","day","year"]],
                   "values": t}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/fa38032a-c6b0-4f4e-b19c-9ce0e51c1342/predictions?version=2021-02-10', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    #having issue to access to ibm cloud services
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    output=pred
  
    return render_template('index.html', prediction_text= output)


if __name__ == "__main__":
    app.run(debug=True)