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

from . import ActGroup, GameConsole, Settings

class GameInterface():
    @classmethod
    def GetName(cls):
        """
        Returns a unique name for the game. The default name is the name of the class.
        The method must only be overwritten if the name to be used differs from the class name.

        Returns:
            :obj:`str`: The unique name of this game.
        """
        return cls.__name__

    @staticmethod
    def GetDescription():
        """
        Returns a description of this game. This is shown in a game console during the game
        selection. By default, an empty string is returned.

        Returns:
            :obj:`str`: The description of this game.
        """
        return ""

    @classmethod
    def GetAuthor(cls):
        """
        Returns the author of the game. This is shown in a game console during the game selection.
        By default, an empty string is returned.

        Returns:
            :obj:`str`: The author of this game.
        """
        return ""

    @staticmethod
    def GetMaxPlayers():
        """
        Returns the maximum number of players that can play at the same time on this game.
        By default, 1 is returned.

        Returns:
            :obj:`int`: The maximum number of players.
        """
        return 1

    def OnInit(self, settings):
        """
        This method is called when the game is :class:`loaded<mtx.GameConsole.LoadGame>` in a game
        console. Variables can be initialized and settings can be set.

        Parameters:
            settings (:class:`mtx.Settings`): The settings object for this game in which all game
                relevant settings can be set.
        """
        pass

    def OnShutdown(self):
        """
        This method is called when the game is finished and can be used to clean up things.
        """
        pass

    def OnPlayerMoveRequest(self, number, direction):
        self.MovePlayer(number, direction)

    def OnPlayerJumpRequest(self, number, direction):
        self.JumpPlayer(number, direction, 2)

    def OnIdle(self, deltaTime):
        """
        Event method that is called periodically. The frequency of the calls depends on the
        implementation of the game console, but 20 milliseconds are recommended.

        It can be used to perform time-based actions such as the movement of opponents.

        **It can not be guaranteed that the frequency of the calls will be met exactly.**
        To be independent of the frequency, the elapsed time since the last call is passed as a
        parameter.

        Parameters:
            deltaTime (:obj:`float`): Time that has elapsed since the last call.

        """

        pass

    def OnTriggerEnter(self, trigger, source):
        """
        Event method, which is called when an object enters a cell with an event object.

        Parameters:
            trigger (:class:`mtx.baseObjects.TriggerObject`): The trigger object that was
                triggered.

            source (:class:`mtx.BaseObject`): The object that triggered the trigger object.
        """
        pass

    def OnTriggerLeave(self, trigger, source):
        """
        Event method, which is called when an object leaves a cell with an event object.

        Parameters:
            trigger (:class:`mtx.baseObjects.TriggerObject`): The trigger object that was
                triggered.

            source (:class:`mtx.BaseObject`): The object that triggered the trigger object.
        """
        pass

    def OnCollect(self, collectable, source):
        """
        Event method, which is called when a collectable object is to be collected. To veto, the
        method should return False.

        Parameters:
            collectable (:class:`mtx.baseObjects.CollectableObject`): The collectable object.
            source (:class:`mtx.BaseObject`): The collector.

        Returns:
            True if the collectable object can be collected and removed by the collector, False
            otherwise.
        """
        return True

    def OnRemove(self, removable, source):
        """
        Event method, which is called when a removable object is to be removed. To veto, the
        method should return False.

        Parameters:
            removable (:class:`mtx.baseObjects.RemovableObject`): The removable object.
            source (:class:`mtx.BaseObject`): The remover.

        Returns:
            True if the removable object can be removed, False otherwise.
        """
        return True

    def OnLevelStart(self, level, isReset):
        """
        Event method, which is called upon each start or reset of a level.

        It can be used to get the number of different objects in the level (e.g. the number of
        items that need to be collected) or to get a particular object (e.g. the player).

        Parameters:
            level (:class:`mtx.Level`): The level object to get access to the objects.
            isReset (:obj:`bool`): True, if the start was caused by a reset, False otherwise.
        """
        pass

    def OnUndo(self):
        pass

    def GetNextLevel(self):
        """
        This method is called from the game console to get the next level.

        **! You must override this method and have to return a level object.**

        Returns:
            A :class:`mtx.Level` object to load as the next level.

        Raises:
            NotImplementedError: If there is not implementation for this method.

        Examples:
            A level can be created by using a level definition, which is a dictionary that defines
            all the information for the level. The level structure itself is defined by an ascii
            matrix where each ascii sign represents one or more game objects.

            .. code-block:: python
                :linenos:

                def GetNextLevel(self):
                    levelDef = {'name':  'Level 1',
                                'plan': ['#####',
                                         '#1bt#',
                                         '#####']}

                    return mtx.Level.CreateByDef(levelDef)

            If you want to create a level based on an algorithm than you have to create a
            :class:`mtx.Level` object and add the game objects with the :class:`Add<mtx.Level.Add>`
            method.

            .. code-block:: python
                :linenos:

                def GetNextLevel(self):
                    level = mtx.Level(5, 3, 'Level 1')

                    level.Add(0, 0, '#')
                    ...

                    return level
        """
        raise NotImplementedError()


class Game(GameInterface):

    def __init__(self):
        self._console = None
        self._level = None
        self._settings = Settings()

    def SetConsole(self, console):
        """
        Sets the game console that is responsible for managing this game.

        **The method is used internally and should not be called externally.**

        Parameters:
            console (:class:`mtx.GameConsole`): A game console object.
        """
        self._console = console

    def GetLevel(self):
        """
        Returns:
            :class:`mtx.Level`: The object of the currently loaded level.
        """
        return self._level

    def GetSettings(self):
        """
        Returns:
            :class:`mtx.Settings`: The settings object of this game.
        """
        return self._settings

    def NextLevel(self):
        self._level = self.GetNextLevel()
        if self._level is not None:
            self.OnLevelStart(self._level, False)

        self._console.OnNextLevel()

    def IsCellAccessible(self, cell, moving):
        return cell.IsAccessible(moving, self._settings)

    def GetAccessibleNeighbourCell(self, obj, moving, direction, distance=1):
        # Get the cell of the object. If the object does not belong to a cell, return None.
        cell = obj.GetCell()
        if cell is None:
            return None

        # Get neighbour cell. If there is no neighbour, or the neighbour is not accessible, then
        # return None.
        nCell = cell.GetNeighbour(direction, distance)
        if nCell is None or not nCell.IsAccessible(moving, self._settings):
            return None

        return nCell

    def HasPlayer(self, number):
        return self._level.GetPlayer(number) is not None

    def MoveObject(self, obj, direction, moveDepth=1):
        """
        Moves an object in the given direction.

        Parameters:
            obj (:class:`mtx.BaseObject`): The object to be moved.
            direction (:obj:`int`): Direction in which the objekt is to be moved.
            moveDepth (:obj:`int`): The maximum number of adjacent moving objects that can be moved
                at a time.

        Returns:
            True, if the object could be moved, False otherwise.
        """

        # Create new ActGroup
        actGrp = self._console.CreateActGroup()

        result = self._MoveObject(obj, direction, moveDepth, actGrp)

        if result:
            actGrp.Ready()
            self._console.ProcessActGroup()
        else:
            self._console.DiscardActGroup(actGrp)

    def MovePlayer(self, number, direction, moveDepth=1):
        """
        Moves a player with given number in the given direction.

        Parameters:
            number (:obj:`int`): The number of the player.
            direction (:obj:`int`): Direction in which the player is to be moved.
            moveDepth (:obj:`int`): The maximum number of adjacent moving objects that can be
                moved at a time.

        Returns:
            True, if the player could be moved, False otherwise.
        """

        # Get player by number
        player = self._level.GetPlayer(number)

        if player is None:
            return False

        # Move the player
        return self.MoveObject(player, direction, moveDepth)

    def JumpObject(self, obj, direction, distance):
        """
        Jump with an object in the given direction and distance.

        Parameters:
            obj (:class:`mtx.BaseObject`): Object which is to perform a jump.
            direction (:obj:`int`): Direction in which to jump.
            distance (:obj:`int`): Distance how far to jump.

        Returns:
            True, if the object could jump, False otherwise.
        """

        nCell = self.GetAccessibleNeighbourCell(obj, moving=False, direction=direction,
                                                distance=distance)
        if nCell is None:
            return False

        # Create new ActGroup
        actGrp = self._console.CreateActGroup()

        actGrp.AddJumpAct(obj, direction, nCell._x, nCell._y)

        self._LeaveCell(obj, obj.GetCell(), actGrp)
        self._EnterCell(obj, nCell, actGrp)

        actGrp.Ready()
        self._console.ProcessActGroup()

        return True

    def JumpPlayer(self, number, direction, distance):
        """
        Jump with a player in the given direction and distance.

        Parameters:
            number (:obj:`int`): The number of the player.
            direction (:obj:`int`): Direction in which to jump.
            distance (:obj:`int`): Distance how far to jump.

        Returns:
            True, if the player could jump, False otherwise.
        """

        # Get player by number
        player = self._level.GetPlayer(number)

        if player is None:
            return False

        # Jump the player
        return self.JumpObject(player, direction, distance)

    def _MoveObject(self, obj, direction, moveDepth, actGrp):
        """
        Moves an object in the given direction.

        Parameters:
            obj (:class:`mtx.BaseObject`): The object to be moved.
            direction (:obj:`int`): Direction in which the object is to be moved.
            moveDepth (:obj:`int`): The maximum number of adjacent moving objects that can be moved
                at a time.
            actGrp (mtx.ActGroup): All acts that occur during the move are added to this group.

        Returns:
            True, if the object could be moved, False otherwise.
        """
        nCell = self.GetAccessibleNeighbourCell(obj, moving=True, direction=direction)
        if nCell is None:
            return False

        # Check if a movable object is on the neighbour cell.
        nObj = nCell.GetFirstObject()
        if nObj is not None and nObj.IsMovable():
            # If moveDepth is zero or the object on the neighbour cell could not be moved, then
            # return False.
            if moveDepth == 0 or not self._MoveObject(nObj, direction, moveDepth-1, actGrp):
                return False

        actGrp.AddMoveAct(obj, direction, nCell._x, nCell._y)

        self._LeaveCell(obj, obj.GetCell(), actGrp)
        self._EnterCell(obj, nCell, actGrp)

        return True

    def _EnterCell(self, obj, cell, actGrp):
        # If any collectable objects are present, then ALL of them will be collected, if
        # they are accepted by the entering object. The top most object, that is not a
        # collectable will be treated separately.
        nonCollectableFound = False
        for o in cell:
            if o.IsCollectable():
                if self.OnCollect(o, obj):
                    actGrp.AddCollectAct(o, obj)
                    cell.Remove(o)
            elif not nonCollectableFound:
                # The top most non-collectable object has been found, so make sure that no
                # other non-collectable objects are handled.
                nonCollectableFound = True

                if o.IsRemovable():
                    if o.RemoveOnEnter() and self.OnRemove(o, obj):
                        actGrp.AddRemoveAct(o, obj)
                        cell.Remove(o)
                elif o.IsTrigger():
                    self.OnTriggerEnter(o, obj)
                    actGrp.AddTriggerEnterAct(o, obj)

        cell.Add(obj)

    def _LeaveCell(self, obj, cell, actGrp):
        cell.Remove(obj)

        # Only treat the top most object.
        o = cell.GetFirstObject()
        if o is None:
            return

        if o.IsTrigger():
            self.OnTriggerLeave(o, obj)
            actGrp.AddTriggerLeaveAct(o, obj)
        elif o.IsRemovable() and not o.RemoveOnEnter() and self.OnRemove(o, obj):
             actGrp.AddRemoveAct(o, obj)
             cell.Remove(o)
