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


# API to get a specific vacation plan based on the id of the plan
@app.route('/api/animal', methods=['GET'])
def api_plan():
    if "id" in request.args:   #Only proceed if id provided as argument
        id = int(request.args["id"])
    else:
        return "ERROR: No id provided"    

    conn = create_con("database2.c7gxabw0pbmb.us-east-2.rds.amazonaws.com", "moimoi", "3n$Eri0pls", "database2db")    #Conection to SQL database
    query = "SELECT * FROM vacations"

    vacations = execute_read_query(conn, query)    #Creates connection and selects all vacation plans from the vacations table
    results = []

    for plan in vacations:                     
        if plan["id"] == id:           #Checks if id in table matches argument id
            results.append(plan)        #Appends only the information of the id that matches the argument id

    return jsonify(results)

app.run()
