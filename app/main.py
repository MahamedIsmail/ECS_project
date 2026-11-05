from flask import Flask, render_template, request
from Getcerts import socket_connection
from Store_data import store_data,list_data,delet_data


app = Flask(__name__)
app.json.sort_keys = False

def get_certificate(domain):
   Data=socket_connection(domain)
   return store_data(Data)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    domain_name = request.form.get('domain')
    
    if not domain_name:
        return "Please provide a valid domain.", 400
   
    return  get_certificate(domain_name)


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




