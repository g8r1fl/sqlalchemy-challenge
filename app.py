from flask import Flask

app = Flask(__name__)

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

    
# def home():
#     """List all available routes"""
    
#     return (f"Available Routes:<br/>"



if __name__ == "__main__":
    app.run(debug=True)