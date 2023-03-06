import json
import logging
import azure.functions as func
import socket
VISITOR_ID = "0"
count = 0

def main(req: func.HttpRequest, message: func.Out[str]) -> func.HttpResponse:
    #get hostname and ip adress of user
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    #define the entity - data to be insert into the table
    my_entity = {
        'PartitionKey': VISITOR_ID,
        'RowKey': ip_address,
        'Hostname': hostname
    }
    #insert entity
    message.set(json.dumps(my_entity))
    #update visitor num
    updateVISITOR()
    #get HTTP respone
    logging.info('Python HTTP trigger function processed a request.')
    outMessage = hostname + " " + ip_address #req.get_body()
    return func.HttpResponse(f"Received the message: {outMessage}", status_code=200)

def updateVISITOR():
    #update count
    global count 
    count += 1
    #update visitor id so it matches count
    global VISITOR_ID
    VISITOR_ID = str(count)
    str(VISITOR_ID)