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

import itertools
import logging

from .RendererClient import RendererClient
from .controllerService.ttypes import GameInfo, GameError


class ControllerHandler():

    __NEW_RENDERER_ID__ = itertools.count()

    def __init__(self, gameConsole, gameLoader):
        self._gameConsole = gameConsole
        self._gameLoader = gameLoader

        self._renderers = {}

    def Ping(self):
        pass

    def ConnectRenderer(self, host, port):
        logging.info('Renderer connected: %s@%s' % (port, host))
        renderer = RendererClient(host, port)
        if renderer.Connect():
            rendererId = next(self.__NEW_RENDERER_ID__)
            self._renderers[rendererId] = renderer
            self._gameConsole.RegisterRenderer(renderer)
        else:
            rendererId = -1

        return rendererId

    def DisconnectRenderer(self, rendererId):
        renderer = self._renderers.get(rendererId)

        if renderer is not None:
            logging.info('Renderer disconnected: %s@%s' % (renderer.GetPort(), renderer.GetHost()))
            renderer.Disconnect()
            del self._renderers[rendererId]

    def GetGames(self):
        return self._gameLoader.GetGames()

    def GetGameInfo(self, name):
        gameClass = self._GetGameClass(name)

        return GameInfo(gameClass.GetName(), gameClass.GetDescription(), gameClass.GetMaxPlayers())

    def LoadGame(self, name):
        gameClass = self._GetGameClass(name)
        self._gameConsole.LoadGame(gameClass())

    def ReloadGame(self):
        idx = -1
        game = self._gameConsole.GetGame()

        if game is not None:
            idx = self._gameLoader.GetGameIndex(game.GetName())

        self._gameConsole.StopGame()
        self._gameLoader.Load()

        gameClass = self._gameLoader.GetGameClass(idx)

        if gameClass is not None:
            self._gameConsole.LoadGame(gameClass())

    def MovePlayer(self, number, direction):
        self._gameConsole.MovePlayer(number, direction)

    def JumpPlayer(self, number, direction):
        self._gameConsole.JumpPlayer(number, direction)

    def ResetLevel(self):
        self._gameConsole.ResetLevel()

    def _GetGameClass(self, name):
        game = self._gameLoader.GetGameClass(name)
        if game is None:
             raise GameError('A game with the name "%s" does not exist.' % name)
        return game
