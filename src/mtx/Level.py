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

from . import (Constants, Field, GetRegisteredObjectClass, IsMultiObjectSymbol,
               GetRegisteredMultiObjectSymbols)
from .objects import Player
from .Utils import count


class Level():
    """
    Class for managing a game level. It contains a :class:`field<mtx.Field>` and a backup of the
    initial state of the field to allow a level reset. It keeps track on the number of the
    different :ref:`game objects<mtx.objects>` and gives access to specific objects.
    """

    def __init__(self, width, height, name=None,
                 groundTexture=Constants.TEXTURE.GROUND.NONE,
                 wallTexture=Constants.TEXTURE.WALL.WHITE_BRICKS):
        """
        Parameters:
            width (:obj:`int`): The width of the level.
            height (:obj:`int`): The height of the level.
            name (:obj:`str`): The name of the level.
            groundTecture (:class:`mtx.TEXTURE.GROUND<mtx.Constants.TEXTURE.GROUND>`): The texture
                for the ground of the level.
            wallTecture (:class:`mtx.TEXTURE.GROUND<mtx.Constants.TEXTURE.GROUND>`): The texture
                for a wall in the level.
        """
        self._number = None
        self._field = Field(width, height)
        self._name = name
        self._groundTexture = groundTexture
        self._wallTexture = wallTexture
        self._players = {}
        self._objCount = {}
        self._resetDataList = []
        self._newId = count()

    @staticmethod
    def Create(defDict):
        """
        This method creates a new level on the basis of a level definition in the form of a
        directory. It defines all the information for the level such as the name, the textures and
        the structure. The level structure itself is defined by an ascii matrix where each ascii
        sign represents one or more game objects.

        Available dictionary keys:

            :name: The name of the level (:obj:`str`).  **- optional**
            :ground: The texture for the ground of the level (:class:`mtx.TEXTURE.GROUND<mtx.Constants.TEXTURE.GROUND>`).  **- optional**
            :wall: The texture for a wall in the level (:class:`mtx.TEXTURE.WALL<mtx.Constants.TEXTURE.WALL>`).  **- optional**
            :plan: List of rows with object symbols representing the structure of the level (:obj:`list`).  **- required**

        Parameters:
            defDict (:obj:`dict`): A dictionary with the level definition.

        Returns:
            :class:`mtx.Level`: The level object for the given definition.

        Example:
            .. code-block:: python

                {'name':   'Level 1',
                 'ground': mtx.TEXTURE.GROUND.EARTH,
                 'wall':   mtx.TEXTURE.WALL.RED_BRICKS,
                 'plan':  ['#####',
                           '#1bt#',
                           '#####']}
        """
        name = defDict.get('name', '')
        groundTexture = defDict.get('ground', Constants.TEXTURE.GROUND.NONE)
        wallTexture = defDict.get('wall', Constants.TEXTURE.WALL.WHITE_BRICKS)
        plan = defDict.get('plan')
        width  = len(plan[0])
        height = len(plan)

        level = Level(width, height, name, groundTexture, wallTexture)

        for y, row in enumerate(plan):
            for x, symbol in enumerate(row):
                level.Add(x, y, symbol)

        return level

    def GetNumber(self):
        """
        Returns:
            :obj:`int`: The number of the level.
        """
        return self._number

    def SetNumber(self, number):
        """
        Parameters:
            number (:obj:`int`): The number of the level.
        """
        self._number = number

    def GetName(self):
        """
        Returns:
            :obj:`str`: The name of the level.
        """
        return self._name if self._name is not None else 'Level %s' % self._number

    def GetGroundTexture(self):
        """
        Returns:
            :class:`mtx.TEXTURE.GROUND<mtx.Constants.TEXTURE.GROUND>`: The texture for the ground
            of the level.
        """
        return self._groundTexture

    def GetWallTexture(self):
        """
        Returns:
            :class:`mtx.TEXTURE.WALL<mtx.Constants.TEXTURE.WALL>`: The texture for a wall in the
            level.
        """
        return self._wallTexture

    def GetField(self):
        """
        Returns:
            :class:`mtx.Field`: The field of the level.
        """
        return self._field

    def GetFieldSize(self):
        """
        Returns:
            :obj:`tuple`: The levels field size.
        """
        return self._field.GetSize()

    def GetPlayers(self):
        """
        Returns:
            :obj:`dict`: All players in a directory that maps a player number to a player object.
        """
        return self._players

    def GetPlayer(self, number):
        """
        Parameters:
            number (:obj:`int`): The number of the player.

        Returns:
            :class:`mtx.BaseObject` or :obj:`None`: The player object or `None`, if no player with
            the given `number` exists.
        """
        return self._players.get(number)

    def GetObjectCount(self, symbol):
        """
        Parameters:
            symbol (:obj:`str`): The symbol of the object.

        Returns:
            :obj:`int`: Returns the number of objects in the entire level with the given `symbol`.
        """
        return self._objCount.get(symbol, 0)

    def Reset(self):
        """
        Resets the level to the initial state.
        """
        self._field.Clear()
        for (x, y), obj in self._resetDataList:
            self._field.GetCell(x, y).Add(obj)

    def Add(self, x, y, symbol):
        """
        Creates a new game object for the given `symbol` and adds it to the level at position
        (`x`, `y`).

        Parameters:
            x (:obj:`int`): `X` coordinate of the position of the game object.
            y (:obj:`int`): `Y` coordinate of the position of the game object.
            symbol (:obj:`str`): The symbol of the game object.
        """

        # A space as symbol will be ignored, because it is not representing an object.
        if symbol in (' '):
            return

        if IsMultiObjectSymbol(symbol):
            # The symbol of a multi object will also be counted
            self._objCount[symbol] = self._objCount.get(symbol, 0) + 1

            for sym in GetRegisteredMultiObjectSymbols(symbol):
                self.Add(x, y, sym)
        else:
            self._objCount[symbol] = self._objCount.get(symbol, 0) + 1

            objCls = GetRegisteredObjectClass(symbol)
            obj = objCls(next(self._newId), symbol)
            if isinstance(obj, Player):
                self._players[obj.GetNumber()] = obj

            self._resetDataList.append(((x, y), obj))
            self._field.GetCell(x, y).Add(obj)

    def GetCell(self, x, y):
        """
        Parameters:
            x (:obj:`int`): `X` coordinate of the cell position.
            y (:obj:`int`): `Y` coordinate of the cell position.

        Returns:
            :class:`mtx.Cell`: The cell for the given coordinates.
        """

        return self._field.GetCell(x, y)
