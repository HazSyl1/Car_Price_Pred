from flask import Flask, render_template, request,send_from_directory
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from pywebio.input import *
from pywebio.output import *
import pywebio

model = pickle.load(open('RF_MODEL.pkl', 'rb'))
app = Flask(__name__)

@app.route('/predict')
def predict():
    Year = input("Enter the modle year:", type=NUMBER)
    Year=2023 - Year
    Present_price=input("Enter the Present Price in lakh:",type=FLOAT)
    Kms_Driven=input("Enter the KmsDriven:",type=FLOAT)
    Kms_Driven2=np.log(Kms_Driven)
    Owner = input("Enter the Owners previously used(0,1,2):",type=NUMBER)
    Fuel_type = select("Enter the Fuel Type ",['Petrol', 'Diesel', 'CNG'])
    if(Fuel_type == 'Petrol'):
        Fuel_type=239
    elif (Fuel_type =='Diesel'):
        Fuel_type=60
    else:
        Fuel_type=2
    Seller_Type=select('Are you a dealer or an individual',['Dealer','Individual'])
    if (Seller_Type == 'Individual'):
        Seller_Type=106
    else:
        Seller_Type=195
    Transmission=select('Enter the Transmission Type',['Mannual','Automatic'])
    if(Transmission == 'Manual'):
        Transmission=261
    else:
        Transmission=40
    
    prediction=model.predict([[Present_price,Kms_Driven2,Fuel_type,Seller_Type,Transmission, Owner, Year]])
    output=round(prediction[0],2)
    
    if output<0:
        put_text("Sory cant be sold")
    else:
        put_text("You can sell it as :",output)
    

app.add_url_rule('/tool','webio_view',webio_view(predict),methods=['GET', 'POST','OPTIONS'])

#pywebio.start_server(predict , port=8080)    

app.run(host='0.0.0.0', port=8080, debug=True)
# if __name__=="__main__":
#      app.run(debug=True)
 