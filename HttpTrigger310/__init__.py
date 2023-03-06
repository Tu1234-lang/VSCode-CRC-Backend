import json
import logging
import azure.functions as func
import socket
VISITOR_ID = "1"

def main(req: func.HttpRequest, messageIn, message: func.Out[str]) -> func.HttpResponse:
    #get hostname and ip adress of user
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    #get entities from table
    from_entity = json.loads(messageIn)
    #if table does not have any entity, inserts a brand new one starting with 1
    if len(from_entity) == 0:
        my_entity = {
            'PartitionKey': VISITOR_ID,
            'RowKey': ip_address,
        }
    #if table already has an entity, takes the last PartitionKey number, and add up
    else:
        lastentity = (from_entity[-1]['PartitionKey'])
        my_entity = {
            'PartitionKey': str(int(lastentity) + 1),
            'RowKey': ip_address,
        }
    #insert entity
    message.set(json.dumps(my_entity))
    #get HTTP respone
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(json.dumps(my_entity),mimetype="application/json", status_code=200)