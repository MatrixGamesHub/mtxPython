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

    def __init__(self, gameConsole, games):
        self._gameConsole = gameConsole
        self._renderers = {}
        self._games = {g.GetName(): g for g in games}

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
        return self._games.keys()

    def GetGameInfo(self, name):
        game = self._GetGame(name)

        return GameInfo(game.GetName(), game.GetDescription(), game.GetMaxPlayers())

    def LoadGame(self, name):
        game = self._GetGame(name)
        self._gameConsole.LoadGame(game())

    def MovePlayer(self, number, direction):
        self._gameConsole.MovePlayer(number, direction)

    def JumpPlayer(self, number, direction):
        self._gameConsole.JumpPlayer(number, direction)

    def ResetLevel(self):
        self._gameConsole.ResetLevel()

    def _GetGame(self, name):
        game = self._games.get(name)
        if game is None:
             raise GameError('A game with the name "%s" does not exist.' % name)
        return game
