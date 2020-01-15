from _thread import *
import serial
import sys
import glob
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from flask_cors import CORS


def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class Home(Resource):
    def get(self):
        return {'state': state, 'password': password}

    def post(self):
        password = request.json['password']
        print("New password : " + password)
        return {'status': 'success'}


class Server:

    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Home, '/')

        @self.app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response

    def start(self):
        self.app.run(port='5002')

def CoArduino():
    while 1:
        pass
    #    if ser.read().decode('ascii') == 'A':
    #        ser.write(b"B")

password = "test"
state = False
print(serial_ports())

#ser = serial.Serial('/dev/ttyS9', 9600)
s = Server()
#now keep talking with the client

start_new_thread(CoArduino, ())
s.start()