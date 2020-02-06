import math

class Position():
    @staticmethod
    def zero():
        return Position(0, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Position(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        return Position(self.x / other.x, self.y / other.y)

    def __floordiv__(self, other):
        return Position(self.x // other.x, self.y // other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def nsewOne(self):
        northOne = self + Position(0, 1)
        southOne = self + Position(0, -1)
        westOne = self + Position(-1, 0)
        eastOne = self + Position(1, 0)
        return (northOne, southOne, eastOne, westOne)

    def __distanceToNoRoot(self, toPosition):
        return (self.x - toPosition.x) * (self.x - toPosition.x) + (self.y - toPosition.y) * (self.y - toPosition.y)

    def distanceTo(self, toPosition):
        return math.sqrt(self.__distanceToNoRoot(toPosition))

    def distanceIsGreaterThan(self, toPosition, comparedValue):
        return self.__distanceToNoRoot(toPosition) > (comparedValue * comparedValue)

    def __repr__(self):
        return f"({repr(self.x)}, {repr(self.y)})"

    def __str__(self):
        return f"({str(self.x)}, {str(self.y)})"

    def __hash__(self):
        return hash(repr(self))

    def toArray(self):
        return [self.x, self.y]
