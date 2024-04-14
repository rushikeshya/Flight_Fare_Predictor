from flask import Flask,request,render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

#create flask app
app = Flask(__name__)

#load the pickle model
model = pickle.load(open("flight_model.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/predict",methods=["GET","POST"])
@cross_origin()
def predict():
    if request.method=='POST':
        
        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)
        duration=(dur_hour*60) + dur_min

        # Total Stops
        stops = int(request.form["stops"])

        # Airline
        airline = request.form['airline']
        airline_dict={'Air Asia':0,'Air India':1,'GoAir':2,'IndiGo':3,'Jet Airways':4,'Jet Airways Business':5,'Multiple carriers':6,
        'Multiple carriers Premium economy':7,'SpiceJet':8,'Trujet':9,'Vistara':10,'Vistara Premium economy':11}
        airline_enc=airline_dict[airline]

        # Source
        source=request.form['source']
        source_dict={'Banglore':0,'Chennai':1,'Delhi':2,'Kolkata':3,'Mumbai':4}
        source_enc=source_dict[source]

        # Destination
        destination=request.form["destination"]
        des_dict={'Banglore':0,'Cochin':1,'Delhi':2,'Hyderabad':3,'Kolkata':4,'New Delhi':5}
        destination_enc=des_dict[destination]

        prediction = model.predict([[
            airline_enc,
            source_enc,
            destination_enc,
            duration,
            stops,
            Journey_day,
            Journey_month,
            Arrival_hour,
            Arrival_min,
            Dep_hour,
            Dep_min]])

        result=round(prediction[0], 2)

        return render_template('index.html', prediction_result="Your Flight Fare From {} To {} is Rs. {}".format(source,destination,result))
    
    return render_template("index.html")

if __name__== "__main__":
    app.run(debug=True)