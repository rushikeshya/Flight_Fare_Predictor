const express = require('express');
const bodyParser = require('body-parser');
const moment = require('moment');
const fs = require('fs');

const app = express();

// Load the pickle model
const model = fs.readFileSync('flight_model.pkl');

// Parse URL-encoded bodies and JSON bodies
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.sendFile('index.html', { root: __dirname });
});

app.post('/predict', (req, res) => {
  const dateDep = req.body.Dep_Time;
  const journeyDay = moment(dateDep, 'YYYY-MM-DDTHH:mm').day();
  const journeyMonth = moment(dateDep, 'YYYY-MM-DDTHH:mm').month() + 1;

  const depHour = moment(dateDep, 'YYYY-MM-DDTHH:mm').hour();
  const depMin = moment(dateDep, 'YYYY-MM-DDTHH:mm').minute();

  const dateArr = req.body.Arrival_Time;
  const arrivalHour = moment(dateArr, 'YYYY-MM-DDTHH:mm').hour();
  const arrivalMin = moment(dateArr, 'YYYY-MM-DDTHH:mm').minute();

  const durHour = Math.abs(arrivalHour - depHour);
  const durMin = Math.abs(arrivalMin - depMin);
  const duration = (durHour * 60) + durMin;

  const stops = parseInt(req.body.stops, 10);

  const airline = req.body.airline;
  const airlineDict = {
    'Air Asia': 0,
    'Air India': 1,
    'GoAir': 2,
    'IndiGo': 3,
    'Jet Airways': 4,
    'Jet Airways Business': 5,
    'Multiple carriers': 6,
    'Multiple carriers Premium economy': 7,
    'SpiceJet': 8,
    'Trujet': 9,
    'Vistara': 10,
    'Vistara Premium economy': 11
  };
  const airlineEnc = airlineDict[airline];

  const source = req.body.source;
  const sourceDict = {
    'Banglore': 0,
    'Chennai': 1,
    'Delhi': 2,
    'Kolkata': 3,
    'Mumbai': 4
  };
  const sourceEnc = sourceDict[source];

  const destination = req.body.destination;
  const destinationDict = {
    'Banglore': 0,
    'Cochin': 1,
    'Delhi': 2,
    'Hyderabad': 3,
    'Kolkata': 4,
    'New Delhi': 5
  };
  const destinationEnc = destinationDict[destination];

  // Make predictions using the model

  // ...

  res.send(`Your Flight Fare From ${source} To ${destination} is Rs. ${result}`);
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
