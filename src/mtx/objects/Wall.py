
from ..baseObjects import SolidObject
from .. import RegisterObjectClass


class Wall(SolidObject):

    @staticmethod
    def GetSymbols():
        return "#"


RegisterObjectClass(Wall)
