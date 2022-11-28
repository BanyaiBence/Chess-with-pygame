from constants import *


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.valid = self._valid()

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f'Pos({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError('Position only has two values')

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError('Position only has two values')

    def __bool__(self):
        return self.valid

    def __copy__(self):
        return Position(self.x, self.y)

    def __deepcopy__(self, memo):
        return Position(self.x, self.y)

    def to_notation(self):
        return f'{chr(self.x + 65)}{8 - self.y}'

    def _valid(self):
        return self.x in VALID_RANGE and self.y in VALID_RANGE


Pos = Position

if __name__ == "__main__":
    pos = Position(0, 0)
    print(pos)
