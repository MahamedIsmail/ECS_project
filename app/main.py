from flask import Flask
from Getcerts import socket_connection

app = Flask(__name__)

@app.route("/")
def hello_world():
    
    return socket_connection()


@app.route("/Health")
def health_check():
    return { "status" :"ok" }

