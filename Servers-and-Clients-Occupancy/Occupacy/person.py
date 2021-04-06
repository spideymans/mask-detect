from math import dist
from itertools import count


class Person:
    id_iter = count()

    def __init__(self, rect=None):
        self.id = next(Person.id_iter)
        self.closestPerson = None
        self.closestPersonDistance = None
        self.rect = rect
        self.lostFrames = 0
        self.maxLostFrames = 30
        self.isGone = False
        self.isMarked = False
        self.referencedPersons = []
        if rect is not None:
            self.center = self.setCenter()
            self.initialCenter = self.center
        else:
            self.center = None
            self.initialCenter = None

    def setRect(self, rect):
        self.rect = rect
        self.center = self.setCenter()
        if self.initialCenter is None:
            self.initialCenter = self.center

    def setCenter(self):
        return (self.rect[0] + self.rect[2]/2,
                self.rect[1] + self.rect[3]/2)

    def setMarked(self):
        self.isMarked = True

    def getMarked(self):
        return self.isMarked

    def getRect(self):
        return self.rect

    def getCenter(self):
        return self.center

    def getInitialCenter(self):
        return self.initialCenter

    def getID(self):
        return self.id

    def addReferencedPerson(self, person):
        self.referencedPersons.append(person)

    def distanceTo(self, person):
        return None if self.center is None or person.getCenter() is None else dist(self.center, person.getCenter())

    def minDistanceTo(self, persons):
        if len(persons) > 0 and self.center is not None:
            smallest = self.distanceTo(persons[0])
            closestPerson = persons[0]
            if smallest is None:
                smallest = 100000
                closestPerson = None
            for person in persons:
                distance = self.distanceTo(person)
                if distance is not None:
                    if distance < smallest:
                        smallest = distance
                        closestPerson = person
            self.closestPerson = closestPerson
            self.closestPersonDistance = smallest
            closestPerson.addReferencedPerson(self)

    def getClosestPerson(self):
        return self.closestPerson

    def getClosestPersonDistance(self):
        return self.closestPersonDistance

    def getReferencedPersons(self):
        return self.referencedPersons

    def updateAttributes(self):
        self.setRect(self.closestPerson.getRect())
        self.closestPersonDistance = None
        self.closestPerson = None
        self.closestPersonID = None

    def loseFrames(self):
        self.lostFrames += 1

    def resetFrames(self):
        self.lostFrames = 0

    def ifGone(self):
        return True if self.lostFrames > self.maxLostFrames else False

    def isLosingFrames(self):
        return self.lostFrames != 0

    def __str__(self):
        attributes = "No attributed entered for this person."
        if self.rect is not None and self.center is not None:
            attributes = "Box: " + str(self.rect) + \
                ", Center: " + str(self.center)
        return "Person: " + attributes
