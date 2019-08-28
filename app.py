import flask
import pickle
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from flask import *
from datetime import datetime
from dbModel import *
import numpy
from psycopg2.extensions import register_adapter, AsIs

def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

register_adapter(numpy.int64, adapt_numpy_int64)

# Use pickle to load in the pre-trained model
with open(f'model/ckd_random_red.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

@app.route('/')
def index():
   return render_template('login.html')

# Route for handling the login page logic
@app.route('/logins', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        # Just render the initial form, to get input
       return (render_template('login.html'))
    
    if request.method == 'POST':
        if request.form['username'] == 'admin' or request.form['pass'] == 'P@55w0rd':
            return redirect(url_for('main'))
        else:
            error = 'Invalid Credentials. Please try again.' 
    return render_template('login.html', error=error)

# Set up the main route
@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        # Just render the initial form, to get input
        return(render_template('main.html'))
    
    if request.method == 'POST':
        # Extract the input
        
        specific_gravity = request.form.get('specific_gravity')
        Albumin = request.form.get('Albumin')
        Blood_Gluc_rand = request.form['Blood_Gluc_rand']
        Blood_Urea = request.form['Blood_Urea']
        Serum_Cr = request.form['Serum_Cr']
        sodium = request.form['sodium']
        Hemoglobin = request.form['Hemoglobin']
        packed_cell_volume = request.form['packed_cell_volume']
        rbc_cnt = request.form['rbc_cnt']
        htn = request.form.get('htn')
        diabetes = request.form.get('diabetes')
        actual_class = request.form.get('diabetes')
        
        # Make DataFrame for model
        input_variables = pd.DataFrame([[specific_gravity,Albumin,Blood_Gluc_rand,Blood_Urea,Serum_Cr,sodium,Hemoglobin,packed_cell_volume,rbc_cnt,htn,diabetes]],
                                       columns=['specific_gravity','Albumin','Blood_Gluc_rand','Blood_Urea','Serum_Cr','sodium','Hemoglobin', 'packed_cell_volume','rbc_cnt','htn', 'diabetes'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]

    if Blood_Gluc_rand != "" and Blood_Urea != "" and Serum_Cr != "" and sodium != "" and Hemoglobin != "":
        add_data = KidneyData(
        specific_gravity = specific_gravity,
        Albumin = Albumin,
        Blood_Gluc_rand = Blood_Gluc_rand,
        Blood_Urea = Blood_Urea,
        Serum_Cr = Serum_Cr,
        sodium = sodium,
        Hemoglobin = Hemoglobin,
        packed_cell_volume = packed_cell_volume,
        rbc_cnt = rbc_cnt,
        htn = htn,
        diabetes = diabetes,
        actual_class = actual_class,
        predicted_class = prediction,
        CreateDate=datetime.now()
                                )

        db.session.add(add_data)
        db.session.commit()

        if int(prediction)==1:
            prediction='Patient may have chronic Kidney Disease'
        else:
            prediction='Patient is Healthy !!!!!'
       
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return render_template('main.html',
                                      original_input={
                                                     'specific_gravity':specific_gravity,
                                                     'Albumin':Albumin,
                                                     'Blood_Gluc_rand':Blood_Gluc_rand,
                                                     'Blood_Urea':Blood_Urea,
                                                     'Serum_Cr':Serum_Cr,
                                                     'sodium':sodium,
                                                     'Hemoglobin':Hemoglobin,
                                                     'packed_cell_volume':packed_cell_volume,
                                                     'rbc_cnt':rbc_cnt,
                                                     'htn':htn,
                                                     'diabetes':diabetes,
                                                     },
                                     result=prediction
                                     
                                     )
@app.route('/logout')
def logout():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
