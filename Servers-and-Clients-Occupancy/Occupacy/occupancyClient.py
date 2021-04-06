from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
import signal
import sys
import json
from threading import Thread
from cv2 import cv2
from person import Person

client = socket(AF_INET, SOCK_STREAM)


def signal_handler(sig, frame):
    global client
    print("Ctrl-C, closing client")
    clientIsClosed = True
    client.close()
    sys.exit(0)


clientIsClosed = False
signal.signal(signal.SIGINT, signal_handler)
host = "127.0.0.1"
port = 12370
personEntered = False
personLeft = False
occupancyCount = 5


def startClient():
    global occupancyCount
    global clientIsClosed
    while not clientIsClosed:
        try:
            client = socket(AF_INET, SOCK_STREAM)
            client.connect((host, port))
            client.recv(1024)
            client.send("Occ".encode("UTF8"))

            while not clientIsClosed:
                sleep(1)
                try:
                    data = {"occupancyCount": occupancyCount}
                    client.send(json.dumps(data).encode("UTF8"))
                except Exception as e:
                    print(e)
                    print("Server connection terminated, retrying....")
                    client.close()
                    break
        except Exception as e:
            print(e)
            print("Cannot connect to server")
            sleep(5)


def calculateCenter(rect):
    center = (rect[0] + rect[2]/2, rect[1] + rect[3]/2)
    return center


def drawBox(frame, rect):
    center = calculateCenter(rect)
    cv2.rectangle(frame, rect, color=(0, 255, 0), thickness=2)
    cv2.putText(frame, ".", (int(center[0]), int(
        center[1])), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


def start(capture, dnn):
    storedPersons = []
    global occupancyCount
    while True:
        newPersons = []
        result, frame = capture.read()
        if not result:
            break
        classVals, _, rect = dnn.detect(frame, confThreshold=0.5)

        for index in range(len(classVals)):
            if classVals.flatten()[index] - 1 == 0:
                newPersons.append(Person(rect[index]))

        if len(storedPersons) == 0:
            for person in newPersons:
                storedPersons.append(person)
                #occupancyCount += 1
        else:
            if len(newPersons) == 0:
                for person in storedPersons:
                    person.loseFrames()
                    if person.ifGone():
                        initialC = person.getInitialCenter()
                        currentC = person.getCenter()
                        #print("Initial Center: ", initialC)
                        #print("Final Center: ", currentC)
                        if initialC is not None and currentC is not None:
                            if initialC[1] >= currentC[1]:
                                occupancyCount += 1
                            else:
                                occupancyCount -= 1
                        storedPersons.remove(person)
                        #occupancyCount -= 1
            else:
                for person in storedPersons:
                    person.minDistanceTo(newPersons)

                if len(newPersons) >= len(storedPersons):
                    for person in storedPersons:
                        person.resetFrames()
                        for newPerson in newPersons:
                            if newPerson.getID() == person.getClosestPerson().getID():
                                newPerson.setMarked()
                        person.updateAttributes()

                    for person in newPersons:
                        if person.getMarked() == True:
                            newPersons.remove(person)
                        else:
                            storedPersons.append(person)
                            #occupancyCount += 1
                else:
                    tempPersons = []
                    for person in newPersons:
                        refPersons = person.getReferencedPersons()
                        if len(refPersons) == 0:
                            continue
                        elif len(refPersons) == 1:
                            refPersons[0].resetFrames()
                            refPersons[0].updateAttributes()
                        else:
                            distance = smallest = refPersons[0].getClosestPersonDistance(
                            )
                            objIndex = 0
                            for jIndex in range(1, len(refPersons)):
                                distance = refPersons[jIndex].getClosestPersonDistance(
                                )
                                if distance < smallest:
                                    smallest = distance
                                    objIndex = jIndex
                            refPersons[objIndex].resetFrames()
                            refPersons[objIndex].updateAttributes()
                            refPersons.remove(refPersons[objIndex])
                            for refP in refPersons:
                                tempPersons.append(refP)
                    for tempPerson in tempPersons:
                        tempPerson.loseFrames()
                        if tempPerson.ifGone():
                            initialC = tempPerson.getInitialCenter()
                            currentC = tempPerson.getCenter()
                            #print("Initial Center: ", initialC)
                            #print("Final Center: ", currentC)
                            if initialC is not None and currentC is not None:
                                if initialC[1] >= currentC[1]:
                                    occupancyCount += 1
                                else:
                                    occupancyCount -= 1
                            storedPersons.remove(tempPerson)
                            #occupancyCount -= 1

        for person in storedPersons:
            if not person.isLosingFrames():
                drawBox(frame, person.getRect())

        print("Occupancy Count: ", occupancyCount)

        cv2.imshow("Video", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break


def setUpVideo():
    captureVideo = cv2.VideoCapture("example_02.mp4")
    captureVideo.set(3, 640)
    captureVideo.set(4, 480)
    return captureVideo


def setUpModel(weights, model):
    dnn = cv2.dnn_DetectionModel(weights, model)
    dnn.setInputSize(320, 320)
    dnn.setInputScale(1.0 / 127.5)
    dnn.setInputMean((127.5, 127.5, 127.5))
    dnn.setInputSwapRB(True)
    return dnn


def init():
    model = 'ssd_mobilenet_v3_large.pbtxt'
    weights = 'frozen_inference_graph.pb'

    capture = setUpVideo()
    dnn = setUpModel(weights, model)

    cthread = Thread(target=startClient)
    cthread.daemon = True
    cthread.start()

    start(capture, dnn)


if __name__ == "__main__":
    init()
