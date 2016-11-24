
from ..baseObjects import TriggerObject
from .. import RegisterObjectClass


class Target(TriggerObject):

    @staticmethod
    def GetSymbols():
        return "t"


RegisterObjectClass(Target)
