
from ..baseObjects import RemovableObject
from .. import RegisterObjectClass, RegisterMultiObjectSymbol


class Tile(RemovableObject):

    @staticmethod
    def GetSymbols():
        return "+"

    def RemoveOnEnter(self):
        return False


RegisterObjectClass(Tile)
RegisterMultiObjectSymbol("*", "++")
RegisterMultiObjectSymbol("%", "+++")
RegisterMultiObjectSymbol("@", "+1")
