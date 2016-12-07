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
import encodings.idna
from threading import Thread, Event, Lock

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from .controllerService import ControllerService


class ControllerServer():

    def __init__(self, port, handler):
        self._port = port
        self._handler = handler
        self._active = Event()

    def Run(self, blocking=False):
        self._active.set()
        serverThread = Thread(target=self._ServerThread)
        serverThread.setDaemon(True)
        serverThread.start()

        if blocking:
            try:
                while self._active.is_set():
                    time.sleep(0.02)
            except KeyboardInterrupt:
                pass

    def Stop(self):
        self._active.clear()

    def _ServerThread(self):
        processor = ControllerService.Processor(self._handler)
        transport = TSocket.TServerSocket(host="0.0.0.0", port=self._port)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
        server.serve()
