# import dependencies
import os
import numpy as np
import pandas as pd
from flask import Flask, jsonify

# SQLAlchemy dependencies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# db setup
db_path = "C:/Users/kcalo/Desktop/Bootcamp/SqlAlchemy-challenge/SurfsUp/Resources/hawaii.sqlite"
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database file not found at {db_path}")
print("Database exists:", os.path.exists(db_path))

# engine to hawaii.sqlite
engine = create_engine(f"sqlite:///{db_path}")

# reflect the db
Base = automap_base()
Base.prepare(engine, reflect=True)

# save refs to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# flask setup
app = Flask(__name__)

# flask routes

@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23"
        f"/api/v1.0/2016-08-23/2017-08-23"
    )

############

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data."""
    session = Session(engine)
   
    last_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = (pd.to_datetime(last_date) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')

    precipitation_data = (
        session.query(measurement.date, Measurement.prcp) .filter(measurement.date >= one_year_ago) .all()
    )
    session.close()

    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

############

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    session = Session(engine)
    station_data = session.query(station.station).all()
    session.close()

    stations_list = [station[0] for station in station_data]
    return jsonify(stations_list)

############

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the most active station."""
    session = Session(engine)
    
    most_active_station = (
        session.query(measurement.station).group_by(measurement.station).order_by(func.count(measurement.station).desc()) .first()[0]
    )
    
    last_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = (pd.to_datetime(last_date) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')

    tobs_data = (
        session.query(measurement.tobs) .filter(measurement.station == most_active_station) .filter(measurement.date >= one_year_ago).all()
    )
    session.close()

    tobs_list = [tobs[0] for tobs in tobs_data]
    return jsonify(tobs_list)

############

@app.route("/api/v1.0/<start>")
def start_temp(start):
    """
    Return min, avg, and max temperatures from the beginning of the dataset to the given start date.
    """
    session = Session(engine)

    first_date = session.query(func.min(measurement.date)).scalar()
    last_date = session.query(func.max(measurement.date)).scalar()

    try:
        start_date = pd.to_datetime(start, format='%Y-%m-%d').strftime('%Y-%m-%d')
        if start_date < first_date or start_date > last_date:
            return jsonify({
                "error": f"Start date out of range. Must be between {first_date} and {last_date}."
            }), 400

    except Exception:
        session.close()
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    sel = [func.min(Measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    try:
        results = session.query(*sel).filter(measurement.date >= first_date, measurement.date <= start_date).all()
        session.close()

        if not results or results[0][0] is None:
            return jsonify({"error": "No data found for the given date range."}), 404

        temp_stats = {
            "TMIN": results[0][0],
            "TAVG": round(results[0][1], 2) if results[0][1] else None,
            "TMAX": results[0][2],
        }
        return jsonify(temp_stats)

    except Exception as e:
        session.close()
        return jsonify({"error": f"Query failed: {str(e)}"}), 500

############

@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end):
    """
    Return min, avg, and max temperatures for the range 8/23/2016 to 8/23/2017.
    """
    session = Session(engine)

    last_date = "2017-08-23"
    one_year_ago = "2016-08-23"

    try:
        start_date = pd.to_datetime(start, format='%Y-%m-%d').strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end, format='%Y-%m-%d').strftime('%Y-%m-%d')

        if start_date < one_year_ago or start_date > last_date:
            return jsonify({
                "error": f"start date out of range."
            }), 400
        if end_date < one_year_ago or end_date > last_date:
            return jsonify({
                "error": f"end date out of range."
            }), 400

    except Exception:
        session.close()
        return jsonify({"error": "Use YYYY-MM-DD."}), 400

    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    try:
        results = (
            session.query(*sel).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
        )
        session.close()

        if not results or results[0][0] is None:
            return jsonify({"error": "no data found."}), 404

        temperature_stats = {
            "TMIN": results[0][0],
            "TAVG": round(results[0][1], 2) if results[0][1] else None,
            "TMAX": results[0][2],
        }
        return jsonify(temperature_stats)

    except Exception as e:
        session.close()
        return jsonify({"error": f"query failed: {str(e)}"}), 500

# Run the application
if __name__ == "__main__":
    app.run(debug=True)

# Use API: http://127.0.0.1:5000/api/v1.0/