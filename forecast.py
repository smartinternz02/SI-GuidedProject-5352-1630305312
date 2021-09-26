import numpy as np
from flask import Flask, request, jsonify, render_template
from joblib import load

from tensorflow.keras.models import load_model
app = Flask(__name__)

model = load_model("sales_forecast.h5")
sc=load("transform1.save")

@app.route('/')
def home():
    return render_template('sales_forecast.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
   
    a = request.form['city']
    if (a == "bombay"):
        o1,o2,o3,o4 = 0,0,0,1
    elif (a == "calcutta"):
        o1,o2,o3,o4 = 0,0,1,0
    elif (a == "chennai"):
        o1,o2,o3,o4 = 0,1,0,0
    elif (a == "delhi"):
        o1,o2,o3,o4 = 1,0,0,0
    
    b = request.form['month']
    b1 = int(b)
    
    c = request.form['day']
    c1 = int(c)
    
    d = request.form['year']
    d1 = int(d)
    
    total = [[o1,o2,o3,o4,b1,c1,d1]]
    prediction = model.predict(sc.transform(total))
    
    output = "Sales forecasted :" + prediction
    

    return render_template('sales_forecast.html', prediction_text='Result: {}'.format(output))

if __name__ == "__main__":
    app.run(port=8086,debug=True)
