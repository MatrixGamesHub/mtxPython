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

from ..baseObjects import TriggerObject
from .. import RegisterObjectClass


class Exit(TriggerObject):

    def __init__(self, id, symbol):
        TriggerObject.__init__(self, id, symbol)
        self._locked = symbol == 'E'

    @staticmethod
    def GetSymbols():
        return "eE"

    def IsLocked(self):
        return self._locked

    def IsUnlocked(self):
        return not self._locked

    def Lock(self):
        self._symbol = 'E'
        self._locked = True

    def Unlock(self):
        self._symbol = 'e'
        self._locked = False


RegisterObjectClass(Exit)
