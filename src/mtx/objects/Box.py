
from ..baseObjects import MovableObject
from .. import RegisterObjectClass, RegisterMultiObjectSymbol


class Box(MovableObject):

    @staticmethod
    def GetSymbols():
        return "b"


RegisterObjectClass(Box)
RegisterMultiObjectSymbol("B", "tb")
