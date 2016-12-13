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

class Act():
    PAUSE         = 0x00
    RESUME        = 0x01
    CLEAR         = 0x02
    LOAD_LEVEL    = 0x03
    RESET_LEVEL   = 0x04
    UPDATE        = 0x05
    MOVE          = 0x06
    JUMP          = 0x07
    SPAWN         = 0x08
    REMOVE        = 0x09
    COLLECT       = 0x0A
    TRIGGER_ENTER = 0x0B
    TRIGGER_LEAVE = 0x0C

    MOTION = (MOVE, JUMP)
    LEVEL = (LOAD_LEVEL, RESET_LEVEL)

    def __init__(self, id):
        self.id = id


class ObjectAct(Act):
    def __init__(self, actId, objId):
        Act.__init__(self, actId)
        self.objId = objId


class LevelAct(Act):
    def __init__(self, actId, level):
        Act.__init__(self, actId)
        self.level = level


class UpdateAct(ObjectAct):
    def __init__(self, objId, key, value):
        ObjectAct.__init__(self, Act.UPDATE, objId)
        self.key = key
        self.value = value


class SpawnAct(ObjectAct):
    def __init__(self, objId, symbol, x, y):
        ObjectAct.__init__(self, Act.SPAWN, objId)
        self.symbol = symbol
        self.x = x
        self.y = y


class EventAct(ObjectAct):
    def __init__(self, actId, objId, sourceId):
        ObjectAct.__init__(self, actId, objId)
        self.sourceId = sourceId


class MotionAct(ObjectAct):
    def __init__(self, actId, objId, direction, fromX, fromY, toX, toY):
        ObjectAct.__init__(self, actId, objId)
        self.direction = direction
        self.fromX = fromX
        self.fromY = fromY
        self.toX = toX
        self.toY = toY


class ActGroup():
    def __init__(self):
        self._acts = []
        self._busy = True

    def __iter__(self):
        return self._acts.__iter__()

    def __len__(self):
        return len(self._acts)

    def IsBusy(self):
        return self._busy

    def Ready(self):
        self._busy = False

    def AddPauseAct(self):
        self._acts.append(Act(Act.PAUSE))

    def AddResumeAct(self):
        self._acts.append(Act(Act.RESUME))

    def AddClearAct(self):
        self._acts.append(Act(Act.CLEAR))

    def AddLoadLevelAct(self, level):
        self._acts.append(LevelAct(Act.LOAD_LEVEL, level))

    def AddResetLevelAct(self, level):
        self._acts.append(LevelAct(Act.RESET_LEVEL, level))

    def AddUpdateAct(self, obj, key, value):
        self._acts.append(UpdateAct(obj.GetId(), key, value))

    def AddMoveAct(self, obj, direction, toX, toY):
        self._acts.append(MotionAct(Act.MOVE, obj.GetId(), direction, obj._cell._x, obj._cell._y, toX, toY))

    def AddJumpAct(self, obj, direction, toX, toY):
        self._acts.append(MotionAct(Act.JUMP, obj.GetId(), direction, obj._cell._x, obj._cell._y, toX, toY))

    def AddSpawnAct(self, obj, x, y):
        self._acts.append(SpawnAct(obj.GetId(), obj.GetSymbol(), x, y))

    def AddRemoveAct(self, obj, source):
        self._acts.append(EventAct(Act.REMOVE, obj.GetId(), source.GetId()))

    def AddCollectAct(self, obj, source):
        self._acts.append(EventAct(Act.COLLECT, obj.GetId(), source.GetId()))

    def AddTriggerEnterAct(self, obj, source):
        self._acts.append(EventAct(Act.TRIGGER_ENTER, obj.GetId(), source.GetId()))

    def AddTriggerLeaveAct(self, obj, source):
        self._acts.append(EventAct(Act.TRIGGER_LEAVE, obj.GetId(), source.GetId()))


class ActQueue():
    def __init__(self):
        self._actGroups = []

    def CreateActGroup(self):
        actGroup = ActGroup()
        self._actGroups.append(actGroup)
        return actGroup

    def __iter__(self):
        return self._actGroups.__iter__()

    def remove(self, actGroup):
        self._actGroups.remove(actGroup)

    def __getitem__(self, key):
        return self._actGroups.__getitem__(key)

    def __delitem__(self, key):
        self._actGroups.__delitem__(key)
