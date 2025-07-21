from flask import Flask, render_template, request, redirect, url_for
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from data import (
    route_list,
    sources,
    destinations,
    additional_info,
    airline,
    filter_routes,
    get_time_period,
)

model = joblib.load("flight_model.joblib")
app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "index.html",
        sources=sources,
        destinations=destinations,
        routes=route_list,
        add_info=additional_info,
        airline=airline,
    )


@app.route("/submit-form", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        form_values = request.form.to_dict()
        time = form_values.get("departure_time")
        form_values["depatures"] = get_time_period(time)
        date = datetime.strptime(form_values.get("date"), "%Y-%m-%d")
        form_values["month"] = date.month
        form_values["day"] = date.day
        columns = [
            "Airline",
            "Source",
            "Destination",
            "Route",
            "Duration",
            "Total_Stops",
            "Additional_Info",
            "Day",
            "Month",
            "Depatures",
        ]
        frame = pd.DataFrame(columns=columns)
        for col in columns:
            frame.loc[0, col] = form_values.get(col.lower())

        pred = model.predict(frame)
        pred = np.exp(pred)
        return f"<h1> Price is: ${pred[0].round(1)} </h1>"


@app.route("/get_route")
def another():
    source = request.args.get("source")
    dest = request.args.get("dest")
    print(source)
    print(dest)
    routes = filter_routes(source, dest)
    return routes


@app.route("/check_route")
def check_route():
    route = request.args.get(key="route")
    stops = len(route.split("→")) - 2
    return str(stops)


if __name__ == "__main__":
    app.run(debug=True)
