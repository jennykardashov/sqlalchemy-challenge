import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from flask import Flask, jsonify

## Database Setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )  

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the last 12 months of precipitation data
    prcp_date_qry = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= dt.date(2016, 8, 23)).\
    filter(Measurement.date <= dt.date(2017, 8, 23)).order_by(Measurement.date).all()
        
    session.close()

    precipitation_data = []
    for date, prcp in prcp_date_qry:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

# # Stations Route - Returns JSON response of stations
# @app.route("/api/v1.0/stations")
# def stations():
#     # Create session link from Python to DB
#     session = Session(engine)

#     # Query all stations
#     total_stations = session.query(Station.station, Station.name).all()

#     # Close session
#     session.close()

#     # Create list and return JSON response
#     all_stations = list(np.ravel(total_stations))

#     return jsonify(all_stations)

# Tobs Route - Queries dates and temp observations of the most-active station for the previous year, and returns a JSON response
# @app.route("/api/v1.0/tobs")
# def tobs():
#     # Create session link from Python to DB
#     session = Session(engine)

#     # Query dates and temp observations of most-active station for previous year
#     most_active_year_qry = session.query(Measurement.station, Measurement.tobs).filter(Measurement.station == most_id).filter(Measurement.date >= dt.date(2016, 8, 23)).filter(Measurement.date <= dt.date(2017, 8, 23)).order_by(Measurement.tobs).all()19281").filter(Measurement.date>="2016-08-23").all()

#     # Close session
#     session.close()

#     # Create list and return JSON response
#     most_active = list(np.ravel(most_active_year_qry))

#     return jsonify(most_active)

# # Start and End Routes - Returns JSON resposne of min temp, max temp, and avg temp for a specified start or start-end range
# @app.route("/api/v1.0/start/<start>")
# @app.route("/api/v1.0/start_end/<start>/<end>")
# def start_end(start, end = "2017-08-23"):
#     # Create session link from Python to DB
#     session = Session(engine)

#     # Query min temp, avg temp, and max temp for specified start or start-end range
#     results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
#         filter(Measurement.date >=start).filter(Measurement.date <= end).all()

#     # Close session
#     session.close()

#     # Create list and return JSON response
#     start_result = list(np.ravel(results))

#     return jsonify(start_result)

if __name__ == '__main__':
    app.run()    