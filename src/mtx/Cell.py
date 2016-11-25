"""
    mtxPython - A framework to create matrix games.
    Copyright (C) 2016  Tobias Stampfl <info@matrixgames.rocks>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation in version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from . import Constants, BaseObject


class Cell():
    """
    Class to manage a cell that is part of a playing :class:`field<mtx.Field>` at a specific
    position.

    Each cell can hold :ref:`game objects<mtx.objects>` that are kept in a list and methods are
    provided to add new game objects, delete existing ones, access neighboring cells, and query
    whether a new game object can be placed on the cell.
    """

    def __init__(self, field, x, y):
        """
        Parameters:
            field (:class:`mtx.Field`): The parent of the cell.
            x (:obj:`int`): The x coordinate of the cell within the field.
            y (:obj:`int`): The y coordinate of the cell within the field.
        """

        self._field = field
        self._x = x
        self._y = y
        self._objCount = {}

        self._objects = []

    def __repr__(self):
        return 'mtx.Cell(%r, %r)' % (self._field, self._position)

    def __iter__(self):
        return self._objects.__iter__()

    def __contains__(self, obj):
        if isinstance(obj, BaseObject):
            return obj in self._objects

        return self._objCount.get(obj, 0) > 0

    def __reversed__(self):
        return self._objects.__reversed__()

    def Add(self, obj):
        """
        Adds a new :ref:`object<mtx.objects>` to the cell.

        Parameters:
            obj (:class:`mtx.BaseObject`): The object to be added to the cell.
        """

        # If the object is currently placed on another cell, it has to be removed from it.
        oldCell = obj.GetCell()
        if oldCell is not None:
            oldCell.Remove(obj)

        # Set this cell as the new parent for the object and add it on top of the object list.
        obj.SetCell(self)
        self._objects.insert(0, obj)

        # Increase the counter of the object type in this cell.
        symbol = obj.GetSymbol()
        self._objCount[symbol] = self._objCount.get(symbol, 0) + 1

    def Remove(self, obj):
        """
        Removes an :class:`object<mtx.objects>` from the cell.

        Parameters:
            obj (:class:`mtx.BaseObject`): The object to be removed from the cell.

        Raises:
            :obj:`LookupError`: If the object is not in the objects list.
        """
        if obj not in self._objects:
            raise LookupError("Object `%s` not in list." % obj)

        # Set the object as parentless and remove it from the object list.
        obj.SetCell(None)
        self._objects.remove(obj)

        # Decrease the counter of the object type in this cell.
        symbol = obj.GetSymbol()
        self._objCount[symbol] = self._objCount[symbol] - 1

    def GetPosition(self):
        """
        Returns:
            :obj:`tuple`: The position of the cell.
        """
        return (self._x, self._y)

    def GetNeighbour(self, location, distance=1):
        """
        Returns the neighboring cell described by `location` and `distance`.
        `location` must be one of :class:`mtx.UP<mtx.Constants.UP>`,
        :class:`mtx.RIGHT<mtx.Constants.RIGHT>`, :class:`mtx.DOWN<mtx.Constants.DOWN>`,
        :class:`mtx.LEFT<mtx.Constants.LEFT>`

        Parameters:
            location (:obj:`int`): The location relative to this cell.
            distance (:obj:`int`): The distance from this cell. The default is 1.

        Returns:
            :class:`mtx.Cell`: The neighboring cell.

        Raises:
            :obj:`AttributeError`: If `location` is not valid.
        """
        if location == Constants.LEFT:
            return self._field.GetCell(self._x - distance, self._y)

        if location == Constants.RIGHT:
            return self._field.GetCell(self._x + distance, self._y)

        if location == Constants.UP:
            return self._field.GetCell(self._x, self._y - distance)

        if location == Constants.DOWN:
            return self._field.GetCell(self._x, self._y + distance)

        raise AttributeError()

    def IsAccessible(self, moving, gameSettings):
        """
        Returns, if an :class:`object<mtx.objects>` can be placed on the cell.
        The result depends on the objects the cell containing and the
        :class:`settings<mtx.Settings>` of the game.

        Parameters:
            moving (:obj:`bool`): True, if the cell will be entered by a move (not a jump), False
                otherise. If move is True and there is a moving object on the cell which can also
                be moved, access is granted.
            gameSettings (:class:`mtx.Settings`): The settings of the game.

        Returns:
            :obj:`bool`: True, if cell is accessible, False otherwise.
        """
        whitelist = gameSettings.cellAccessWhitelist
        blacklist = gameSettings.cellAccessBlacklist

        if len(self._objects) == 0:
            if whitelist is not None and ' ' not in whitelist:
                return False

            if blacklist is not None and ' ' in blacklist:
                return False

            return True

        whitelistRespected = False

        for obj in self._objects:
            if obj.IsSolid():
                # If a solid object is on the cell, no other object is allowed.
                return False

            if obj.IsMovable() and (not moving or not obj.IsMovableByObject()):
                # If a movable object is on the cell, and either one object wants to acces without
                # moving or the movable object can't be moved by another object, the access will
                # be denied.
                return False

            if whitelist is not None and not whitelistRespected and obj.GetSymbol() in whitelist:
                whitelistRespected = True

            if blacklist is not None and obj.GetSymbol() in blacklist:
                return False

        if whitelist is not None and not whitelistRespected:
            return False

        return True

    def GetFirstObject(self):
        """
        Returns:
            :class:`mtx.BaseObject` or :obj:`None`: The top most object on the cell or None if none
            exists.
        """

        if len(self._objects) > 0:
            return self._objects[0]
        return None

    def GetObjectBelow(self, obj):
        """
        Parameters:
            obj (:class:`mtx.BaseObject`): The object from which the next underlying object is to
                be returned.

        Returns:
            :class:`mtx.BaseObject` or :obj:`None`: The first object below the given one or None if
            none exists.
        """

        if obj not in self._objects:
            return None

        idx = self._objects.index(obj)
        if idx == len(self._objects) - 1:
            return None

        return self._objects[idx + 1]

    def GetObjectCount(self, symbol):
        """
        Parameters:
            symbol (:obj:`str`): The symbol of an object.

        Returns:
            :obj:`int`: The number of objects with the given symbol.
        """
        return self._objCount.get(symbol, 0)
