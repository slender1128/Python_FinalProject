from flask import Flask, render_template, request
from joblib import dump, load
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

model = load("model.joblib")

hours = np.arange(0, 24, 1)

temperature = "13" #Temperature(°C) min=-17.8 mean=12.88 max=39.4
humidity = "60" #Humidity(%) min=0 mean=58.23 max=98
visibility = "2000" #Visibility (10m) min=27 mean=1436.82 max=2000
solarRad = "0" #Solar Radiation (MJ/m2) min=0 mean=0.57 max=3.52
rainfall = "0" #Rainfall(mm) min=0 mean=0.15 max=35
snowfall = "0" #Snowfall (cm) min=0 mean=0.075 max=8.8
seasons = "0" #Seasons
holiday = "1" #Holiday

@app.route('/', methods=['GET', 'POST'])
def index():
    global model
    global temperature
    global humidity
    global visibility
    global solarRad
    global rainfall
    global snowfall
    global seasons
    global holiday
    
    if request.method == 'POST':
        if request.form.get('plotButton') == 'Plot':
            temperature = request.form["temperature"]
            humidity = request.form["humidity"]
            visibility = request.form["visibility"]
            solarRad = request.form["solarRad"]
            rainfall = request.form["rainfall"]
            snowfall = request.form["snowfall"]
            seasons = request.form["seasons"]
            holiday = request.form["holiday"]
    return render_template('index.html', graphJSON = plot_graph(), temperature = temperature, humidity = humidity, visibility = visibility, solarRad = solarRad, rainfall = rainfall, snowfall = snowfall, seasons = seasons, holiday = holiday)

def plot_graph():
    parameters = pd.DataFrame({"Hour":hours,
                               "Temperature(°C)":[float(temperature) for i in hours],
                               "Humidity(%)":[float(humidity) for i in hours],
                               "Visibility (10m)":[int(visibility) for i in hours],
                               "Solar Radiation (MJ/m2)":[float(solarRad) for i in hours],
                               "Rainfall(mm)":[float(rainfall) for i in hours],
                               "Snowfall (cm)":[float(snowfall) for i in hours],
                               "Seasons":[int(seasons) for i in hours],
                               "Holiday":[bool(holiday) for i in hours]})
    bikes = model.predict(parameters)
     
    fig = px.line(pd.DataFrame({"Hour":hours, "Rented Bike Count":bikes}), x="Hour", y="Rented Bike Count", markers=True, range_x=[0, 23])
    fig.update_layout(xaxis = dict(tickmode = "linear", tick0 = 0, dtick = 1))
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON

if __name__ == '__main__':
    app.run(debug=False)