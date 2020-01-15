import socket
import sys
from _thread import *
from signal import signal, SIGINT

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

class Home(Resource):
    def get(self):
        return {"Directeur":"http://127.0.0.1:5002/cible/Directeur",
                "Laboratoire":"http://127.0.0.1:5002/cible/Laboratoire",
                "Docteur":"http://127.0.0.1:5002/cible/Docteur"}

class Server:

    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Home, '/')

    def start(self):
        self.app.run(port='5002')

def handler(signal_received, frame):
    # Handle any cleanup here
	try:
		pass
	except:
		pass
	exit()

signal(SIGINT, handler)

def testA():
    while 1:
        print("A")

def testB():
    while 1:
        print("B")

s = Server()
#now keep talking with the client

start_new_thread(testA, ())
start_new_thread(testB, ())
s.start()

s.close()