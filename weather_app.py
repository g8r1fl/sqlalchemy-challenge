import numpy as np

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

    
def precipitation("/api/v1.0/precipitation")
    """convert the query results to a dictionary using 'date' as the key and 'prcp' as the value"""
    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(366)
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).all()

    prcp_data = []
    for date, prcp in precip:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

def stations("/api/v1.0/stations")
    """Return JSON list of stations from the dataset"""
    return

def tobs("/api/v1.0/tobs")

    return

def start("/api/v1.0/start")

    return

def end("/api/v1.0/end")

    return

if __name__ == "__main__":
    app.run(debug=True)