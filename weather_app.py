import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask setup

app = Flask(__name__)


# Routes setup
@app.route("/")

def home():
    """List all available routes"""

    return (f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start/<br/>"
            f"/api/v1.0/start/end/<br/>"
    )

@app.route("/api/v1.0/precipitation")    
def precipitation():
    """convert the query results to a dictionary using 'date' as the key and 'prcp' as the value"""
    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(366)
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()
    session.close()

    prcp_data = []
    for date, prcp in precip:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return JSON list of stations from the dataset"""
    session = Session(engine)
    stations = session.query(Station.station, Station.name).all()
    session.close()
    station_list = list(np.ravel(stations))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temps for the previous year"""
    session = Session(engine)
    query = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()
    most_active = (sorted(query, key=lambda x :int(x[1]), reverse=True))[0][0]
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date > "2016-8-23").all()
    session.close()
    return jsonify(temps)

@app.route("/api/v1.0/<start>")   
def start(start):
    """Return a list of min, max and avg temperatures for\
         the path variable supplied by the user, or a 404 if not."""

    session = Session(engine)
    query = session.query(func.min(Measurement.tobs),\
         func.max(Measurement.tobs), func.avg(Measurement.tobs))\
             .filter(Measurement.date >= start).all()    
    session.close()
    return jsonify(query)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    """Return a list of min, max and avg temperatures for\
         the path variable supplied by the user, or a 404 if not."""
    session = Session(engine)
    query = session.query(func.min(Measurement.tobs),\
         func.max(Measurement.tobs), func.avg(Measurement.tobs))\
             .filter(Measurement.date >= start, Measurement.date <= end).all()    
    
    session.close()
    # weather_dict = {'Min Temperature': func.min(Measurement.tobs),'Max Temperature': func.max(Measurement.tobs), 'Avg Temperature': func.avg(Measurement.tobs)}
    return jsonify(query)


if __name__ == "__main__":
    app.run(debug=True)