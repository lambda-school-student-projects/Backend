import unittest
from bsvRoomController import RoomController
from bsvRoom import Room
from bsvPosition import Position
from bsvCardinalDirection import CardinalDirection
import json


class RoomTests(unittest.TestCase):
    def setUp(self):
        pass

    def testPosition(self):
        position = Position(23.547, 29.557)
        self.assertEqual(position.x, 23.547)
        self.assertEqual(position.y, 29.557)

        zPos = Position.zero()
        self.assertEqual(zPos.x, 0)
        self.assertEqual(zPos.y, 0)

        distance = zPos.distanceTo(position)
        37.78991
        self.assertEqual(distance, 37.78991211950618)

        gtTest = zPos.distanceIsGreaterThan(position, 35)
        self.assertEqual(gtTest, True)
        gtTest = zPos.distanceIsGreaterThan(position, 40)
        self.assertEqual(gtTest, False)

        otherPos = Position(0, 0)

        self.assertEqual(position == otherPos, False)
        self.assertEqual(position != otherPos, True)
        self.assertEqual(otherPos == zPos, True)
        self.assertEqual(otherPos != zPos, False)

        n, s, e, w = zPos.nsewOne()
        self.assertEqual(n, Position(0, 1))
        self.assertEqual(s, Position(0, -1))
        self.assertEqual(e, Position(1, 0))
        self.assertEqual(w, Position(-1, 0))

    def testPositionInSet(self):
        mySet = set([Position.zero(), Position(0, 1)])
        self.assertEqual(len(mySet), 2)
        mySet.add(Position.zero())
        self.assertEqual(len(mySet), 2)

        self.assertEqual(Position.zero() in mySet, True)

    def rooms(self):
        roomA = Room("Room A")
        roomB = Room("Room B")
        roomC = Room("Room C")
        return (roomA, roomB, roomC)

    def testRoomConnections(self):
        a, b, c = self.rooms()

        a.connectEastTo(b)
        b.connectEastTo(c)

        self.assertEqual(a.position, Position(0, 0))
        self.assertEqual(b.position, Position(1, 0))
        self.assertEqual(c.position, Position(2, 0))

        # reset
        a, b, c = self.rooms()

        a.connectNorthTo(b)
        b.connectNorthTo(c)

        self.assertEqual(a.position, Position(0, 0))
        self.assertEqual(b.position, Position(0, 1))
        self.assertEqual(c.position, Position(0, 2))

        # reset
        a, b, c = self.rooms()

        a.connectSouthTo(b)
        b.connectSouthTo(c)

        self.assertEqual(a.position, Position(0, 0))
        self.assertEqual(b.position, Position(0, -1))
        self.assertEqual(c.position, Position(0, -2))

        # reset
        a, b, c = self.rooms()

        a.connectWestTo(b)
        b.connectWestTo(c)

        self.assertEqual(a.position, Position(0, 0))
        self.assertEqual(b.position, Position(-1, 0))
        self.assertEqual(c.position, Position(-2, 0))

        # reset
        a, b, c = self.rooms()
        d, e, f = self.rooms()

        a.connectNorthTo(b)
        b.connectWestTo(c)
        c.connectSouthTo(d)
        d.connectWestTo(e)
        e.connectNorthTo(f)

        self.assertEqual(a.position, Position(0, 0))
        self.assertEqual(b.position, Position(0, 1))
        self.assertEqual(c.position, Position(-1, 1))
        self.assertEqual(d.position, Position(-1, 0))
        self.assertEqual(e.position, Position(-2, 0))
        self.assertEqual(f.position, Position(-2, 1))

    def testRoomController(self):
        controller = RoomController()
        controller.resetAllRooms()

        # adding rooms
        self.assertEqual(controller.canAddRoomAt(Position(0, 1)), True)
        self.assertEqual(controller.canAddRoomAt(Position(0, -1)), True)
        self.assertEqual(controller.canAddRoomAt(Position(1, 0)), True)
        self.assertEqual(controller.canAddRoomAt(Position(-1, 0)), True)
        self.assertEqual(controller.canAddRoomAt(Position(0, 0)), False)

        # add room confirmation booleans
        spawn = controller.spawnRoom
        a, b, c = self.rooms()
        d, e, f = self.rooms()
        controller.addRoomConnection(a, spawn, CardinalDirection.NORTH)
        controller.addRoomConnection(b, a, CardinalDirection.EAST)
        self.assertEqual(controller.canAddRoomAt(Position(1, 0)), False)
        self.assertEqual(controller.canAddRoomAt(Position(2, 1)), True)

        self.assertEqual(controller.roomEligibleToAppend(spawn), True)

        controller.addRoomConnection(c, spawn, CardinalDirection.WEST)
        controller.addRoomConnection(d, c, CardinalDirection.SOUTH)
        self.assertEqual(controller.roomEligibleToAppend(spawn), False)

        # add room eligible directions
        self.assertEqual(controller.roomEligibleDirections(b), set([CardinalDirection.NORTH, CardinalDirection.EAST]))
        self.assertEqual(controller.roomEligibleDirections(d), set([CardinalDirection.SOUTH, CardinalDirection.WEST]))

    def testGenerateQuickTestJSON(self):
        roomController = RoomController(10)
        file_write = open("rooms10.json", "w")
        json.dump(roomController.toDict(), file_write, indent=2)
        file_write.close()

        roomController = RoomController(100)
        file_write = open("rooms100.json", "w")
        json.dump(roomController.toDict(), file_write)
        file_write.close()

        roomController.textVisualization()

        roomController = RoomController(500)
        file_write = open("rooms500.json", "w")
        json.dump(roomController.toDict(), file_write)
        file_write.close()

        # print(roomController.toDict())


if __name__ == '__main__':
    unittest.main()
