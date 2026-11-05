from flask import Flask
from Getcerts import socket_connection
from Store_data import store_data,list_data,delet_data

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/")
def hello_world():
   Data=socket_connection()
   return store_data(Data)


@app.route("/DB")
def Display_DB():
  
  return list_data()

@app.route("/Health")
def health_check():
    return { "status" :"ok" }


@app.post("/DB/<item_id>/delete")

def delete_item(item_id):
    removed = delet_data(item_id)
    if removed is None:
        return {"error": "item not found", "id": item_id}, 404
    return {"deleted": removed}
