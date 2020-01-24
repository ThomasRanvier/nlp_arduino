import serial
import re
import sys
import glob
import json
import os
from _thread import *
import speech_recognition as sr
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from flask_cors import CORS
import datetime
from signal import signal, SIGINT
from sys import exit
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment



def handler(signal_received, frame):
    # Handle any cleanup here
    logger.createLog(4, "Arret du serveur")
    logger.saveLog()
    exit(0)

class Logger:
    def __init__(self):
        try:
            with open('data/logs.json') as json_data:
                self.logs = json.load(json_data)
        except:
            self.logs = []
            with open('data/logs.json', 'w', encoding='utf-8') as f:
                json.dump(self.logs, f, ensure_ascii=False, indent=4)

    def getAll(self):
        return self.logs
    
    def getLasts(self,nb):
        return self.logs[:nb]

    def createLog(self, prio, msg):
        t = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        self.logs.insert(0, {'type': t[prio], 'content': msg, 'date': str(datetime.datetime.now())})

    def saveLog(self):
        with open('data/logs.json', 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=4)

class Home(Resource):

    def post(self):
        global password
        global logger
        if 'logs' in request.json:
            return {'code': '220', 'logs' : logger.getLasts(5)}
        old = request.json['old']
        if password == old:
            password = request.json['password']
            with open('data/password.json', 'w', encoding='utf-8') as f:
                json.dump(password, f, ensure_ascii=False, indent=4)
            logger.createLog(3, "Changement du mot de passe")
            ser.write(b'C')
            return {'code': '200'}
        else:
            logger.createLog(2, "Erreur de mot de passe")
            return {'code': '500'}

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
        global logger
        logger.createLog(4, "Demarage du serveur")
        self.app.run(port='5002')

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

def CoArduino():
    while 1:
        if ser.read().decode('ascii') == 'A':
            print("Ecoute en cours...")
            with sr.Microphone() as source:
                audio = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                sd.wait()  # Wait until recording is finished
                write('data/output.wav', fs, audio)  # Save as WAV file )
                song = AudioSegment.from_wav("data/output.wav")
                song.export("data/output.flac",format = "flac")
                try:
                    voice = sr.AudioFile('data/output.flac')
                    with voice as source:
                        audio = r.record(source)
                    text = r.recognize_google(audio, language="fr-FR")
                    print("Entendu : ", text)
                    os.remove("data/output.flac")
                    os.remove("data/output.wav")
                    if re.search(password, text):
                        logger.createLog(3, "Mot de passe reconnu")
                        ser.write(b'B')
                    else:
                        logger.createLog(3, "Mot de passe non reconnu")
                        ser.write(b'N')
                except sr.UnknownValueError:
                    print("Je n'ai pas compris")
                except sr.RequestError as e:
                    logger.createLog(1, "Erreur API Google : " + format(e))
                    print("Le service Google Speech API ne fonctionne plus" + format(e))

logger = Logger()
fs = 44100  # Sample rate
seconds = 5  # Duration of recording
r = sr.Recognizer()
ser = serial.Serial(serial_ports()[0], 9600)
s = Server()

signal(SIGINT, handler)

try:
    with open('data/password.json') as json_data:
        password = json.load(json_data)
except:
    password = "test"
    with open('data/password.json', 'w', encoding='utf-8') as f:
            json.dump(password, f, ensure_ascii=False, indent=4)  
 
start_new_thread(CoArduino, ())
s.start()