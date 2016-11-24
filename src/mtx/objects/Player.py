
from ..baseObjects import MovableObject
from .. import RegisterObjectClass


class Player(MovableObject):

    def __init__(self, id, symbol):
        MovableObject.__init__(self, id, symbol)
        self._number = int(symbol)

    @staticmethod
    def GetSymbols():
        return "12345678"

    def IsMovableByObject(self):
        return False

    def GetNumber(self):
        return self._number


RegisterObjectClass(Player)
