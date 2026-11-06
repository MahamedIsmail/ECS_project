from flask import Flask, render_template, request
from Getcerts import socket_connection
from Store_data import store_data,list_data,delet_data
from validator import clean_domain, resolve_public_ip, InvalidDomain   


app = Flask(__name__)
app.json.sort_keys = False

def get_certificate(domain,ip):
   Data=socket_connection(domain,ip)
   return store_data(Data)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    raw = request.form.get("domain", "")

    try:                                         
        domain = clean_domain(raw)
        ip = resolve_public_ip(domain)
    except InvalidDomain as err:
        return {"error": str(err), "input": raw}, 400

    return get_certificate(domain, ip), 201



@app.route("/DB")
def Display_DB():
  
  return list_data()

@app.route("/health")
def health_check():
    return { "status" :"ok" }


@app.post("/DB/<item_id>/delete")

def delete_item(item_id):
    removed = delet_data(item_id)
    if removed is None:
        return {"error": "item not found", "id": item_id}, 404
    return {"deleted": removed}




