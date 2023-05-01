# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, Request, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def main():
    return(
        f"Welcome to Climate Changes in Hawaii<br />"
        f"Available Routes<br />"
        f"Rainfall from last year: /api/v1.0/precipitation<br />"
        f"Stations Available: /api/v1.0/stations<br />"
        f"Temperature Observed /api/v1.0/tobs<br />"
        f"Min, Max and Avg Temperature for given start date /api/v1.0/yyyy-mm-dd<br/>"
        f"Min, Max and Avg Temperature for given start date to end date /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
        
          
    )

@app.route("/api/v1.0/precipitation")
def prcp():
          
    #Query the data and return the jsonified precipitation data for the last year in the database
     
          last_date = dt.date(2017, 8, 23) - dt.timedelta(days= 365)
          result= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= last_date).all()
          session.close()
          precipitation= {date: prcp for date, prcp in result}
          return jsonify (precipitation)


@app.route("/api/v1.0/stations")
def stations():
    #Query all station 
    result1= session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    station_name= list(np.ravel(result1))

#Return jsonified data

    return jsonify (station_name)



@app.route("/api/v1.0/tobs")
def tobs():
    #Query the date and temperature observed for the most active station   
    result2= session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= '2016-08-23').all()
    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(result2))

#return the jsonified data for the last year
    return jsonify (tobs)


@app.route("/api/v1.0/<start>")
def start(start):

    #Query the temperature observed and Return the min, max, and average temperatures calculated from the given start date to the end of the dataset
    result3 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()


    #Create a dictionary from the row data and append to a list of temperature stats
    temp_stats = []
    for min, avg, max in result3:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Max"] = max
        tobs_dict["Average"] = avg
        
        temp_stats.append(tobs_dict)

#return the jsonified data
    return jsonify(temp_stats)



@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):

#Query the data and Return the min, max, and average temperatures calculated from the given start date to the given end date

    result4 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()


     # Create a dictionary from the row data and append to a list of all statistics
   

    all_stats = []
    for min, avg, max in result4:
        tobs_dict1 = {}
        tobs_dict1["Min"] = min
        tobs_dict1["Max"] = max
        tobs_dict1["Average"] = avg
        
        all_stats.append(tobs_dict1)

    ##return the jsonified data    
    return jsonify(all_stats)




if __name__ == "__main__":
    app.run(debug = True)