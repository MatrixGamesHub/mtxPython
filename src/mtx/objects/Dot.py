
from ..baseObjects import CollectableObject
from .. import RegisterObjectClass


class Dot(CollectableObject):

    @staticmethod
    def GetSymbols():
        return "."


RegisterObjectClass(Dot)
