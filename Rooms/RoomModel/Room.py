from .Position import Position
from .CardinalDirection import CardinalDirection
import uuid

class Room():
    def __init__(self, name, position=Position.zero(), north=None, south=None, east=None, west=None):
        self.name = name
        self.position = position
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.players = set()
        self.itemReward = None
        self.id = str(uuid.uuid4())

    def toDict(self):
        newDict = {}
        newDict["name"] = self.name
        newDict["position"] = self.position.toArray()
        newDict["id"] = self.id
        if self.north:
            newDict["north"] = self.north.id
        if self.south:
            newDict["south"] = self.south.id
        if self.west:
            newDict["west"] = self.west.id
        if self.east:
            newDict["east"] = self.east.id
        newDict["itemReward"] = self.itemReward
        return newDict

    def connectNorthTo(self, room):
        self.north = room
        relativePosition = Position(0, 1)
        self.north.position = self.position + relativePosition
        if room.south != self:
            room.connectSouthTo(self)

    def connectSouthTo(self, room):
        self.south = room
        relativePosition = Position(0, -1)
        self.south.position = self.position + relativePosition
        if room.north != self:
            room.connectNorthTo(self)

    def connectEastTo(self, room):
        self.east = room
        relativePosition = Position(1, 0)
        self.east.position = self.position + relativePosition
        if room.west != self:
            room.connectWestTo(self)

    def connectWestTo(self, room):
        self.west = room
        relativePosition = Position(-1, 0)
        self.west.position = self.position + relativePosition
        if room.east != self:
            room.connectEastTo(self)

    def connectedInDirections(self):
        connectedDirections = set()
        if self.north:
            connectedDirections.add(CardinalDirection.NORTH)
        if self.south:
            connectedDirections.add(CardinalDirection.SOUTH)
        if self.east:
            connectedDirections.add(CardinalDirection.EAST)
        if self.west:
            connectedDirections.add(CardinalDirection.WEST)
        return connectedDirections

    def visualizeTextCharacter(self):
        connections = self.connectedInDirections()
        if len(connections) == 4:
            return "+"
        elif len(connections) == 3:
            # nes
            if CardinalDirection.NORTH in connections and CardinalDirection.EAST in connections and CardinalDirection.SOUTH in connections:
                return "+"
            # new
            elif CardinalDirection.NORTH in connections and CardinalDirection.EAST in connections and CardinalDirection.WEST in connections:
                return "+"
            # nws
            elif CardinalDirection.NORTH in connections and CardinalDirection.SOUTH in connections and CardinalDirection.WEST in connections:
                return "+"
            # ews
            else:
                return "+"
        elif len(connections) == 2:
            # ne
            if CardinalDirection.NORTH in connections and CardinalDirection.EAST in connections:
                return "+"
            # nw
            elif CardinalDirection.NORTH in connections and CardinalDirection.WEST in connections:
                return "+"
            # ns
            elif CardinalDirection.NORTH in connections and CardinalDirection.SOUTH in connections:
                return "|"
            # es
            elif CardinalDirection.EAST in connections and CardinalDirection.SOUTH in connections:
                return "r"
            # ew
            elif CardinalDirection.EAST in connections and CardinalDirection.WEST in connections:
                return "-"
            # sw
            else:
                return "+"
        elif len(connections) == 1:
            # n
            if CardinalDirection.NORTH in connections:
                return "⏝"
            # s
            elif CardinalDirection.SOUTH in connections:
                return "⏜"
            # w
            elif CardinalDirection.WEST in connections:
                return ")"
            # e
            else:
                return "("
        else:
            return " "

    def __str__(self):
        connectedRooms = [self.north, self.south, self.east, self.west]
        connectionCount = len(connectedRooms)
        roomsString = "room" + ("" if connectionCount == 1 else "s")
        return f"Room: {self.name} - connected to {connectionCount} {roomsString}"
