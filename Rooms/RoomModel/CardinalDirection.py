from enum import Enum

class CardinalDirection(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
