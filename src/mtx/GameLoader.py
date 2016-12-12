import os
import inspect
import importlib
import logging

import mtx


class GameLoader():
    def __init__(self, *args):
        self._pathList = [os.path.abspath(path) for path in args if os.path.isdir(path)]
        self._gameDict = {}
        self._gameList = []

    def Load(self):
        self._gameDict = {}

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
                                        self._gameDict[attr.GetName()] = {'class': attr,
                                                                          'module': gameModule}
                                        break
                            except BaseException as e:
                                logging.error("Error while loading game module '%s': %s" % (modName, e))
                                continue

        self._gameList = list(self._gameDict.keys())
        self._gameList.sort()

    def ReloadGame(self, nameOrIdx):
        name = self._gameList[nameOrIdx] if isinstance(nameOrIdx, int) else nameOrIdx

        if name in self._gameDict:
            module = self._gameDict[name]['module']
            importlib.reload(module)

    def GetGamesCount(self):
        return len(self._gameList)

    def GetGameName(self, idx):
        return self._gameList[idx]

    def GetGameNames(self):
        return self._gameList

    def GetGameClass(self, nameOrIdx):
        name = self._gameList[nameOrIdx] if isinstance(nameOrIdx, int) else nameOrIdx
        elem = self._gameDict.get(name)
        return elem['class'] if elem is not None else None
