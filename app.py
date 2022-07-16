from flask import Flask, render_template, request
import json
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('loan_application.pickle', 'rb'))

with open("columns.json", "r") as f:
    __data_columns = json.load(f)['data_columns']

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():

    if request.method == 'POST':
        applicantincome = int(request.form['applicantincome'])
        coapplicantincome = int(request.form['coapplicantincome'])
        loanamount = int(request.form['loanamount'])
        loanamountterm = int(request.form['loanamountterm'])
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        selfemployed = request.form['selfemployed']
        credithistory = request.form['credithistory']
        propertyarea = request.form['propertyarea']

        if gender=='Female':
            g =0
        else:
            g =1
        if married=='No':
            m =0
        else:
            m =1

        dep = dependents
        if dep == '1':
            dp = 1
        elif dep == '2':
            dp = 2
        elif dep == '3+':
            dp = 3 
        else:
            dp = 0 
    
        if education == 'Not Graduate':
            e =0
        else:
            e =1
    
        if selfemployed == 'Yes':
            se =1
        else:
            se =0

        if credithistory == '0':
            ch = 0
        else:
            ch = 1
    
        prop_area = propertyarea
        if prop_area=='Rural':
            pa = 0
        elif prop_area=='Urban':
            pa = 2
        else:
            pa = 1

        x = np.zeros(len(__data_columns))
        x[0] = g
        x[1] = m
        x[2] = dp
        x[3] = e
        x[4] = se
        x[5] = applicantincome
        x[6] = coapplicantincome
        x[7] = loanamount
        x[8] = loanamountterm
        x[9] = ch
        x[10] = pa

        prediction=model.predict([x])[0]




        if prediction==0:
            return render_template('index.html',prediction_neg="Sorry, your loan application is Rejected.")
        else:
            return render_template('index.html',prediction_pos="Congratulations!!! your loan application is Approved!")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run()
