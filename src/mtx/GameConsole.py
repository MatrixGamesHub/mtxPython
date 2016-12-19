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

import time
from . import ActGroup, ActQueue
from threading import Thread
import queue


class ActionProcessor(Thread):

    def __init__(self, renderer):
        Thread.__init__(self, name="ActionProcessor %s" % renderer)
        self._active = True
        self._actQueue = queue.Queue()
        self._renderer = renderer
        self.setDaemon(True)

    def AddActGroup(self, actGroup):
        self._actQueue.put(actGroup)
        
    def Stop(self):
        print("stopping", self.getName())
        self._active = False

    def run(self):
        print("start", self.getName())
        while self._active:
            actGrp = None
            try:
                actGrp = self._actQueue.get(timeout=1)
            except queue.Empty:
                continue

            if len(actGrp) > 0:
                self._renderer.ProcessActGroup(actGrp)
        print("finishing", self.getName())


class GameConsole():

    def __init__(self):
        self._renderers = []
        self._game = None
        self._gameInitialized = False
        self._clock = time.clock()
        self._actQueue = ActQueue()
        
    def Destroy(self):
        for actProc in self._renderers:
            actProc.Stop()

    def RegisterRenderer(self, renderer):
        actProc = ActionProcessor(renderer)
        self._renderers.append(actProc)
        if self._game is not None and self._game._level is not None:
            actGrp = ActGroup()
            actGrp.AddLoadLevelAct(self._game._level)
            actGrp.Ready()

            actProc.AddActGroup(actGrp)

        actProc.start()

    def UnregisterRenderer(self, renderer):
        self._renderers.remove(renderer)

    def GetGame(self):
        return self._game

    def LoadGame(self, game):
        if self._game is not None:
            self._game.OnShutdown()

        self._gameInitialized = False
        self._game = game
        self._game.SetConsole(self)

        self._game.OnInit(self._game.GetSettings())
        self._game.NextLevel()
        self._gameInitialized = True

    def StopGame(self):
        if self._game is not None:
            self._gameInitialized = False
            self._game.OnShutdown()
            self._game = None

            actGrp = self._actQueue.CreateActGroup()
            actGrp.AddClearAct()
            actGrp.Ready()

            self.ProcessActGroup()

    def MovePlayer(self, number, direction):
        if self._game is not None:
            self._game.OnPlayerMoveRequest(number, direction)

    def JumpPlayer(self, number, direction):
        if self._game is not None:
            self._game.OnPlayerJumpRequest(number, direction)

    def ResetLevel(self):
        if self._game is not None:
            level = self._game._level
            level.Reset()
            self._game.OnLevelStart(level, True)

            actGrp = self._actQueue.CreateActGroup()
            actGrp.AddResetLevelAct(level)
            actGrp.Ready()

            self.ProcessActGroup()

    def Undo(self):
        if self._game is not None:
            self._game.OnUndo()

    def Idle(self):
        clock = time.clock()
        deltaTime = clock - self._clock
        self._clock = clock

        if self._game is not None and self._gameInitialized:
            self._game.OnIdle(deltaTime)

    def CreateActGroup(self):
        return self._actQueue.CreateActGroup()

    def DiscardActGroup(self, actGrp):
        self._actQueue.remove(actGrp)

    def ProcessActGroup(self, actGrp=None, renderer=None):
        queue = self._actQueue if actGrp is None else [actGrp]
        renderers = self._renderers if renderer is None else [renderer]

        for actGrp in queue[:]:
            for renderer in renderers:
                renderer.AddActGroup(actGrp)

            queue.remove(actGrp)

    def OnNextLevel(self):
        actGrp = self._actQueue.CreateActGroup()
        actGrp.AddLoadLevelAct(self._game._level)
        actGrp.Ready()

        self.ProcessActGroup()
