from flask import Flask
from flask_cors import CORS, cross_origin
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from time import sleep
import signal
import sys
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

server = socket(AF_INET, SOCK_STREAM)
serverIsClosed = False

roomID = 1001

maxOccupancy = 20
occupancyCount = 5
currentOccupancy = occupancyCount
occupancyAlarm = False
occupancyAlarmStatus = "Room is currently not overoccupied"

maskDetected = False
personEnteredRoom = False
maskAlarm = False
maskAlarmStatus = "No mask alarm"


@app.route("/")
def start():
    return 'Welcome to our project'


@app.route("/api/v1/roomInfo")
def roomDetails():
    occupancy = {
        "occupancyCount": occupancyCount,
        "maxOccupancy": maxOccupancy,
        "occupancyAlarm": occupancyAlarm,
        "occupancyAlarmStatus": occupancyAlarmStatus,
    }

    mask = {
        "maskDetected": maskDetected,
        "maskAlarmStatus": maskAlarmStatus,
        "personEnteredRoom": personEnteredRoom,
        "maskAlarm": maskAlarm
    }
    return {
        "roomID": roomID,
        "occupancy": occupancy,
        "mask": mask
    }


def signal_handler(sig, frame):
    global server, serverIsClosed
    print("Ctrl-C")
    serverIsClosed = True
    server.close()
    sys.exit(0)


def server():
    global occupancyCount, maxOccupancy, occupancyAlarm, occupancyAlarmStatus
    global maskAlarm, maskAlarmStatus, maskDetected, personEnteredRoom
    global server, serverIsClosed
    host = "127.0.0.1"
    port = 12370
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((host, port))
    print("Server listening for clients")
    server.listen()

    while True:
        conn, addr = server.accept()
        print('Got connection from', addr)
        conn.send("ack".encode("UTF8"))
        dataRecv = conn.recv(1024).decode("UTF8")

        if dataRecv == "Occ":
            thread = Thread(target=occupancyClient, args=(conn,))
            thread.daemon = True
            thread.start()
        elif dataRecv == "Mask":
            thread = Thread(target=maskClient, args=(conn,))
            thread.daemon = True
            thread.start()


def occupancyClient(conn):
    global occupancyCount, maxOccupancy, currentOccupancy, occupancyAlarm, occupancyAlarmStatus
    global maskAlarm, maskAlarmStatus, maskDetected, personEnteredRoom
    print("occupancy thread...")
    while True:
        if serverIsClosed:
            print("Closing server...")
            break
        dataRecv = conn.recv(1024).decode("UTF8")
        if dataRecv:
            data = json.loads(dataRecv)
        else:
            continue

        if data == None or data == "":
            continue

        occupancyCount = data.get("occupancyCount")

        if occupancyCount is None:
            print("One of the modules is not connected")
            continue

        print(data)

        if occupancyCount > currentOccupancy:
            personEnteredRoom = True
            currentOccupancy = occupancyCount
            if occupancyCount > maxOccupancy:
                occupancyAlarm = True
                occupancyAlarmStatus = "Room is overoccupied"
            else:
                occupancyAlarm = False
                occupancyAlarmStatus = "Room is not overoccupied"

        if occupancyCount < currentOccupancy:
            personEnteredRoom = False
            currentOccupancy = occupancyCount
            if occupancyCount <= maxOccupancy:
                occupancyAlarm = False
                occupancyAlarmStatus = "Room is not overoccupied"


def maskClient(conn):
    global occupancyCount, maxOccupancy, occupancyAlarm, occupancyAlarmStatus
    global maskAlarm, maskAlarmStatus, maskDetected, personEnteredRoom
    print("client thread...")
    conn.send("ack".encode("UTF8"))
    while True:
        if serverIsClosed:
            print("Closing server...")
            break
        dataRecv = conn.recv(1024).decode("UTF8")
        if dataRecv:
            data = json.loads(dataRecv)
        else:
            continue

        if data == None or data == "":
            continue

        maskWorn = data.get("mask")

        if maskWorn is None:
            print("One of the modules is not connected")
            continue

        print(data)

        if maskWorn:
            maskDetected = True
            maskAlarm = False
            maskAlarmStatus = "Person is wearing mask, no alarm"
        else:
            if personEnteredRoom:
                maskAlarm = True
                maskDetected = False
                maskAlarmStatus = "Person entered room without wearing mask"
            else:
                maskAlarm = False
                maskAlarmStatus = "Person did not enter room, no mask alarm"
            maskDetected = False


sthread = Thread(target=server)
sthread.daemon = True
sthread.start()


#signal.signal(signal.SIGINT, signal_handler)
