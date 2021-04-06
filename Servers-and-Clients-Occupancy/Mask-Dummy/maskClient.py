from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
import signal
import sys
import json

client = socket(AF_INET, SOCK_STREAM)
clientIsClosed = False


def signal_handler(sig, frame):
    global client
    print("Ctrl-C, closing client")
    clientIsClosed = True
    client.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

host = "127.0.0.1"
port = 12370

while not clientIsClosed:
    try:
        client.connect((host, port))
        client.recv(1024)
        client.send("Mask".encode("UTF8"))

        while not clientIsClosed:
            maskWorn = False
            mask = input("Did person wear mask? (Press y for yes): ")
            if mask == "y":
                maskWorn = True
            else:
                maskWorn = False
            try:
                data = {"mask": maskWorn}
                client.send(json.dumps(data).encode("UTF8"))
            except Exception as e:
                print(e)
                print("Server connection terminated, retrying....")
                client.close()
                break
            count = 0
    except Exception as e:
        print(e)
        print("Cannot connect to server")
        sleep(5)

count = 0
