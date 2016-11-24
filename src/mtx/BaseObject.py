
class BaseObject():
    """
    Base class for all objects.

    An object is something that can be placed on a :class:`mtx.Cell` and what is visualized by a
    renderer.
    """

    def __init__(self, id, symbol):
        self._id = id
        self._symbol = symbol
        self._cell = None

    @staticmethod
    def GetSymbols():
        raise NotImplementedError()

    def GetId(self):
        return self._id

    def GetSymbol(self):
        return self._symbol

    def Is(self, symbol):
        return self._symbol == symbol

    def IsBelow(self, symbol):
        objBelow = self._cell.GetObjectBelow(self)
        return objBelow is not None and objBelow.Is(symbol)

    def GetObjectCount(self, symbol):
        return self._cell.GetObjectCount(symbol)

    def SetCell(self, cell):
        """
        Parameters:
            cell (:class:`mtx.Cell`): The cell to which the object belongs.
        """
        self._cell = cell

    def GetCell(self):
        """
        Returns:
            The (:class:`cell<mtx.Cell>`) to which the object belongs.
        """
        return self._cell

    def IsSolid(self):
        """
        Returns:
            True if the object is solid, False otherwise.

        See Also:
            :class:`mtx.baseObjects.SolidObject`
        """
        return False

    def IsMovable(self):
        """
        Returns:
            True if the object is movable, False otherwise.

        See Also:
            :class:`mtx.baseObjects.MovableObject`
        """
        return False

    def IsCollectable(self):
        """
        Returns:
            True if the object is collectable, False otherwise.

        See Also:
            :class:`mtx.baseObjects.CollectableObject`
        """
        return False

    def IsRemovable(self):
        """
        Returns:
            True if the object is removable, False otherwise.

        See Also:
            :class:`mtx.baseObjects.RemovableObject`
        """
        return False

    def IsTrigger(self):
        """
        Returns:
            True if the object is a trigger, False otherwise.

        See Also:
            :class:`mtx.baseObjects.TriggerObject`
        """
        return False


REGISTERED_OBJECT_CLASSES = {}
MULTI_OBJECT_SYMBOL = {}


def _CheckSymbol(symbol):
    if symbol in REGISTERED_OBJECT_CLASSES:
        raise RuntimeError("Symbol '%s' already used by another object: %s" %\
                           (symbol, REGISTERED_OBJECT_CLASSES[symbol].__name__))

    if symbol in MULTI_OBJECT_SYMBOL:
        raise RuntimeError("Symbol '%s' already registered as a multi object symbol: %s" %\
                           (symbol, MULTI_OBJECT_SYMBOL[symbol]))


def RegisterObjectClass(objCls):
    """
    Method to register an object class.
    """
    for symbol in objCls.GetSymbols():
        _CheckSymbol(symbol)
        REGISTERED_OBJECT_CLASSES[symbol] = objCls


def RegisterMultiObjectSymbol(symbol, symbols):
    """
    Method to register a symbol, that represents more than one object. The objects are linked
    by there symbols. The order in symbols is relevant, they will be added from left to right.
    """
    _CheckSymbol(symbol)
    MULTI_OBJECT_SYMBOL[symbol] = symbols


def GetRegisteredObjectClass(symbol):
    if symbol not in REGISTERED_OBJECT_CLASSES:
        raise RuntimeError("No object class registered for the symbol `%s`" % symbol)
    return REGISTERED_OBJECT_CLASSES[symbol]


def IsMultiObjectSymbol(symbol):
    return symbol in MULTI_OBJECT_SYMBOL


def GetRegisteredMultiObjectSymbols(symbol):
    if symbol not in MULTI_OBJECT_SYMBOL:
        raise RuntimeError("No multi object registered for the symbol `%s`" % symbol)
    return MULTI_OBJECT_SYMBOL[symbol]
