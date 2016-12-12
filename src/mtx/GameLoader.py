import os
import inspect
import importlib
import logging

import mtx


class GameLoader():
    def __init__(self, *args):
        self._pathList = [os.path.abspath(path) for path in args if os.path.isdir(path)]
        self._gameList = []
        self._gameClassDict = {}
        self._gameModuleDict = {}

    def Load(self):
        self._gameList = []
        self._gameClassDict = {}
        self._gameModuleDict = {}

        for path in self._pathList:
            for folder in os.listdir(path):
                folderPath = os.path.join(path, folder)
                if os.path.isdir(folderPath):
                    for pyFile in os.listdir(folderPath):
                        modName, fileExt = os.path.splitext(pyFile)
                        if fileExt == '.py':
                            try:
                                pyFilePath = os.path.join(folderPath, pyFile)
                                loader = importlib.machinery.SourceFileLoader(modName, pyFilePath)
                                gameModule = loader.load_module()
                                for attrName in dir(gameModule):
                                    attr = getattr(gameModule, attrName)
                                    if inspect.isclass(attr) and issubclass(attr, mtx.Game):
                                        gameName = attr.GetName()
                                        if gameName not in self._gameList:
                                            self._gameList.append(gameName)
                                            self._gameClassDict[gameName] = attr
                                            self._gameModuleDict[gameName] = gameModule
                                        break
                            except BaseException as e:
                                logging.error("Error while loading game module '%s': %s" % (modName, e))
                                continue

        self._gameList.sort()

    def ReloadGame(self, nameOrIdx):
        name = self._GetGameName(nameOrIdx)

        if name in self._gameModuleDict:
            importlib.reload(self._gameModuleDict[name])

    def GetGamesCount(self):
        return len(self._gameList)

    def GetGameName(self, idx):
        try:
            return self._gameList[idx]
        except IndexError:
            return None

    def GetGameIndex(self, name):
        try:
            return self._gameList.index(name)
        except ValueError:
            return -1

    def GetGameNames(self):
        return self._gameList

    def GetGameClass(self, nameOrIdx):
        return self._gameClassDict.get(self._GetGameName(nameOrIdx))

    def _GetGameName(self, nameOrIdx):
        if isinstance(nameOrIdx, int):
            if nameOrIdx >= 0 and nameOrIdx < len(self._gameList):
                return self._gameList[nameOrIdx]
        else:
            return nameOrIdx
        return None
