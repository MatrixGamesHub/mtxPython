
import time
from threading import Thread, Event, Lock

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer, TNonblockingServer

from .mtxControllerService import MtxControllerService


class MtxNetControllerServer():

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
        processor = MtxControllerService.Processor(self._handler)
        transport = TSocket.TServerSocket(port=self._port)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
        server.serve()
