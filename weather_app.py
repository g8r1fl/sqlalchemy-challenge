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
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start/<end><br/>"
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
    stations = session.query(Station.station).all()
    session.close()
    station_list = list(np.ravel(stations))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    query = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()
    return jsonify(list(np.ravel(query)))

@app.route("/api/v1.0/start")
def start():

    return

@app.route("/api/v1.0/end")
def end():

    return

if __name__ == "__main__":
    app.run(debug=True)