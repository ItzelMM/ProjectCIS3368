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
@app.route('/api/vacation', methods=['GET'])
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


#API to update the values of a vacation plan in the zoo table
@app.route('/api/vacation', methods=['POST'])
def api_update_plan():
    conn = create_con("database2.c7gxabw0pbmb.us-east-2.rds.amazonaws.com", "moimoi", "3n$Eri0pls", "database2db")    #Conection to SQL database

    request_data = request.get_json()      #Set request info as a dictionary and then iterate through it to get the different fields and correspoding values that need to be updated
    if "id" in request_data:   #Only proceed if id provided as argument
        id = int(request_data["id"])
        del request_data["id"]
        for field in request_data:
            value = request_data[field]
            # This query will be iterated to update the different values that have to be updated
            update_query = "UPDATE vacations SET `%s` = '%s' WHERE id = %d" % (field, value, id)
            execute_query(conn, update_query)
    else:
        return "ERROR: No id provided"

    return "Update request succesful"


#API to add a vacation plan to the vacations table
@app.route('/api/vacation', methods=['PUT'])
def api_add():
    conn = create_con("database2.c7gxabw0pbmb.us-east-2.rds.amazonaws.com", "moimoi", "3n$Eri0pls", "database2db")    #Conection to SQL database
    request_data = request.get_json()
    transport = request_data["transportation"]  
    startd = request_data["startdate"]
    endd = request_data["enddate"]
    #I'm assuming that the city has to also be entered in the request information to get the destinationid that matches the city
    city = request_data["city"]


    #With this query I'm getting the destination record of the city requested
    query_id = "SELECT * FROM destionation WHERE city = '%s'" % (city)
    specific_destination = execute_read_query(conn, query_id)    #Creates connection and selects all destinations with the specified city from destination table

    #This loop extracts the destination id from the destination record with the requested city
    for info_destination in specific_destination:         
        destination_id = int(info_destination["id"])

    # This query adds the new animal to the zoo table
    query = "INSERT INTO vacations (destinationid, transportation, startdate, enddate) VALUES (%d, '%s', '%s', '%s')" % (destination_id, transport, startd, endd)
    execute_query(conn, query)

    return "Add request succesful"    

app.run()
