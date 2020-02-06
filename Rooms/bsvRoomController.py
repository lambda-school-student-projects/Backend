from .bsvQueue import Queue
from .bsvPosition import Position
from .bsvCardinalDirection import CardinalDirection
from .bsvRoom import Room
# from Player import Player # ready for importing
from livestream.consumers import consumerController
import random
import time
import threading
import json

roomSize = 740
roomMid = roomSize / 2


class RoomController():
    # pass an integer in to initializer to modify the room limit
    def __init__(self, roomLimit=100):
        self.roomLimit = roomLimit
        self.generateRooms()
        
        thread = threading.Thread(target=self.gameLoop, args=())
        thread.daemon = True
        thread.start()


    def toDict(self):
        newDict = {}
        roomDict = {}
        for room in self.rooms:
            roomDict[room.id] = room.toDict()
        newDict["rooms"] = roomDict
        newDict["roomCoordinates"] = [pos.toArray() for pos in self.roomCoordinates]
        newDict["spawnRoom"] = self.spawnRoom.id
        return newDict

    def getRoom(self, roomID):
        roomID = str(roomID) ## sometimes the id is in uuid format - convert for dict key
        room = self.roomDict.get(roomID, None)
        return room

    def spawnPlayerInRoom(self, player, roomID, fromDirection=None):
        self.removePlayerFromCurrentRoom(player)
        newRoom = self.roomDict.get(roomID, self.spawnRoom)
        self.occupiedRooms.add(newRoom)
        if newRoom in self.emptyRooms:
            self.emptyRooms.remove(newRoom)

        self.allPlayers[str(player.id)] = player
        newRoom.addPlayer(player)

        if fromDirection is None:
            position = Position(roomMid, roomMid)
        elif fromDirection == CardinalDirection.NORTH:
            position = Position(roomMid, roomSize)
        elif fromDirection == CardinalDirection.EAST:
            position = Position(roomSize, roomMid)
        elif fromDirection == CardinalDirection.SOUTH:
            position = Position(roomMid, 0)
        else: # west
            position = Position(0, roomMid)

        player.setPosition(position)

    def removePlayerFromCurrentRoom(self, player):
        room = self.getRoom(player.current_room)
        if room:
            room.removePlayer(player)
            if not room.occupied and room in self.occupiedRooms:
                self.occupiedRooms.remove(room)
                self.emptyRooms.add(room)

    def resetAllRooms(self):
        self.roomDict = {}
        self.rooms = set()
        self.occupiedRooms = set()
        self.emptyRooms = set()
        self.roomCoordinates = set()
        self.allPlayers = {}

        self.spawnRoom = Room("Spawn Area")
        self.addRoomConnection(self.spawnRoom, None, None)

    def generateRooms(self, seed=time.time()):
        self.resetAllRooms()
        random.seed(seed)

        roomQueue = Queue()
        roomQueue.enqueue(self.spawnRoom)

        while len(self.rooms) < self.roomLimit:
            if len(roomQueue) == 0:
                print("Somehow there are no valid rooms in the queue")
                return
            oldRoom = roomQueue.dequeue()
            newRoom = Room(f"Room {len(self.rooms)}")

            possibleDirections = list(self.roomEligibleDirections(oldRoom))
            possibleDirections.sort()
            if len(possibleDirections) > 0:
                newDirection = random.choice(possibleDirections)
                self.addRoomConnection(newRoom, oldRoom, newDirection)
                if self.roomEligibleToAppend(newRoom):
                    roomQueue.enqueue(newRoom)
                if self.roomEligibleToAppend(oldRoom):
                    roomQueue.enqueue(oldRoom)

    # must include an oldRoom and direction or the new room will sit abandoned and alone. Exception is made for initial room.
    def addRoomConnection(self, newRoom, oldRoom, direction):
        if oldRoom and direction:
            if direction == CardinalDirection.NORTH:
                oldRoom.connectNorthTo(newRoom)
            elif direction == CardinalDirection.EAST:
                oldRoom.connectEastTo(newRoom)
            elif direction == CardinalDirection.SOUTH:
                oldRoom.connectSouthTo(newRoom)
            elif direction == CardinalDirection.WEST:
                oldRoom.connectWestTo(newRoom)
            else:
                # something went wrong
                return

        self.rooms.add(newRoom)
        self.roomDict[newRoom.id] = newRoom
        self.emptyRooms.add(newRoom)
        self.roomCoordinates.add(newRoom.position)

    # checks to see how many NSEW neighbors a new room would potentially have. returns true if the neighbor count is 1
    def canAddRoomAt(self, position):
        nswe = [pos for pos in (position.nsewOne())]

        count = len([direction for direction in nswe if direction in self.roomCoordinates])
        if count == 1:
            return True
        else:
            return False

    def roomEligibleDirections(self, room):
        n, s, e, w = room.position.nsewOne()
        eligibleDirections = set()
        if self.canAddRoomAt(n):
            eligibleDirections.add(CardinalDirection.NORTH)
        if self.canAddRoomAt(s):
            eligibleDirections.add(CardinalDirection.SOUTH)
        if self.canAddRoomAt(e):
            eligibleDirections.add(CardinalDirection.EAST)
        if self.canAddRoomAt(w):
            eligibleDirections.add(CardinalDirection.WEST)
        return eligibleDirections

    def roomEligibleToAppend(self, room):
        return len(self.roomEligibleDirections(room)) > 0

    def textVisualization(self):
        xValueSet = {room.position.x for room in self.rooms}
        yValueSet = {room.position.y for room in self.rooms}
        xValues = sorted(list(xValueSet))
        yValues = sorted(list(yValueSet))

        xRange = xValues[-1] - xValues[0]
        xOffset = 0 - xValues[0]
        yRange = yValues[-1] - yValues[0]
        yOffset = 0 - yValues[0]

        yTemplateArray = [" "] * (yRange + 1)

        xTemplateArray = [yTemplateArray.copy() for i in range(xRange + 1)]

        for room in self.rooms:
            xIndex = xOffset + room.position.x
            yIndex = yOffset + room.position.y
            xTemplateArray[xIndex][yIndex] = "O" if room.position == Position.zero() else room.visualizeTextCharacter()

        outStr = ""
        for yIndex in range(yRange - 1, 0, -1):
            for xIndex in range(xRange):
                outStr += xTemplateArray[xIndex][yIndex]
            outStr += "\n"

        print(outStr)

    def playerDisconnected(self, player):
        if player:
            room = self.getRoom(str(player.current_room))
            if room:
                room.removePlayer(player)


    def gameLoop(self):
        tEnd = time.monotonic() - 1
        while time.monotonic() >= tEnd:
            tEnd = time.monotonic() + 0.03333


            # game logic
            for room in self.occupiedRooms:
                # room = Room("test")
                allPlayerInfo = {}
                for player in room.players:
                    allPlayerInfo[str(player.id)] = { "position": player.getPosition().toArray() }
                
                allPlayerJson = json.dumps({"messageType": "playerPositions", "data": allPlayerInfo})
                for player in room.players:
                    # print(room.name, player.id)
                    playerWS = consumerController.get(str(player.id), None)
                    if playerWS is not None:
                        playerWS.send(text_data=allPlayerJson)


            # delay if not enough time has elapsed
            if tEnd > time.monotonic():
                time.sleep(tEnd - time.monotonic())


roomController = RoomController()
