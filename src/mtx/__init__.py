
from .Constants import *
from .Settings import Settings
from .Act import *
from .Renderer import *
from .GameConsole import *
from .BaseObject import (BaseObject, RegisterObjectClass, RegisterMultiObjectSymbol,
                         GetRegisteredObjectClass, IsMultiObjectSymbol,
                         GetRegisteredMultiObjectSymbols)
from .Cell import *
from .Field import *
from .Level import *
from .Game import *

from . import baseObjects
from . import objects
