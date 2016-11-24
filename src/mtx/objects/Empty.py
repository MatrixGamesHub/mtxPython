
from ..baseObjects import SolidObject
from .. import RegisterObjectClass


class Empty(SolidObject):

    @staticmethod
    def GetSymbols():
        return "-"


RegisterObjectClass(Empty)
