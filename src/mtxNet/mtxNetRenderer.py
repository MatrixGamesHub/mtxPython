
import mtx
from .mtxRendererService import MtxRendererService
from .mtxRendererService.ttypes import LevelInfo

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class MtxNetRenderer(mtx.Renderer):

    def __init__(self, host, port):
        self._transport = TSocket.TSocket(host, port)
        protocol = TBinaryProtocol.TBinaryProtocol(self._transport)
        self._client = MtxRendererService.Client(protocol)
        self._connected = False
        self._host = host
        self._port = port

    def GetHost(self):
        return self._host

    def GetPort(self):
        return self._port

    def Connect(self):
        try:
            self._transport.open()
            self._connected = True
        except TTransport.TTransportException:
            self._connected = False

        return self._connected

    def Disconnect(self):
        self._transport.close()
        self._connected = False

    def IsConnected(self):
        return self._connected

    def _CallClientCommand(self, cmd, *args, **kwargs):
        if not self._connected:
            return False

        try:
            cmd(*args, **kwargs)
        except (ConnectionAbortedError, ConnectionResetError):
            print("Connection to renderer client lost...")
            self._connected = False

    def ProcessActGroup(self, actGrp):
        self._CallClientCommand(self._client.Freeze)

        try:
            for act in actGrp:
                if act.id in mtx.Act.LEVEL:

                    level = act.level
                    field = level._field

                    netField = []
                    for y in range(field._height):
                        row = []
                        for x in range(field._width):
                            cell = []
                            for obj in reversed(field._cells[y][x]):
                                cell.append([obj._id, ord(obj._symbol)])
                            row.append(cell)
                        netField.append(row)

                    if act.id == mtx.Act.LOAD_LEVEL:
                        self._CallClientCommand(self._client.LoadLevel, netField, LevelInfo(level._name, level._groundTexture, level._wallTexture))
                    else:
                        self._CallClientCommand(self._client.ResetLevel, netField)
                elif act.id == mtx.Act.SPAWN:
                    self._CallClientCommand(self._client.Spawn, act.objId, ord(act.symbol), act.x, act.y)
                elif act.id == mtx.Act.REMOVE:
                    self._CallClientCommand(self._client.Remove, act.objId, act.sourceId)
                elif act.id == mtx.Act.COLLECT:
                    self._CallClientCommand(self._client.Collect, act.objId, act.sourceId)
                elif act.id == mtx.Act.MOVE:
                    self._CallClientCommand(self._client.Move, act.objId, act.direction, act.fromX, act.fromY, act.toX, act.toY)
                elif act.id == mtx.Act.JUMP:
                    self._CallClientCommand(self._client.Jump, act.objId, act.direction, act.fromX, act.fromY, act.toX, act.toY)
        finally:
            self._CallClientCommand(self._client.Thaw)
