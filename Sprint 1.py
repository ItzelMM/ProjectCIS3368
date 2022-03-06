#Project Sprint 1 - Itzel Munoz Monroy
import flask
from flask import jsonify
from flask import request
from sql import create_con
from sql import execute_query
from sql import execute_read_query
from datetime import date 

#Setting up the application
app = flask.Flask(__name__)  #Sets up the application
app.config["DEBUG"] = True 

# API to get all vacation plans
@app.route('/api/vacation/all', methods=['GET'])
def api_plans():
    conn = create_con("database2.c7gxabw0pbmb.us-east-2.rds.amazonaws.com", "moimoi", "3n$Eri0pls", "database2db")    #Conection to SQL database
    query = "SELECT * FROM vacations"

    plans = execute_read_query(conn, query)    #Creates connection and selects all vacations from the vacations table
    results = []

    for plan in plans:
        results.append(plan)

    return jsonify(results)

app.run()