import can
import threading

class UdsClient:
    bus = None
    recvCallback = None
    recvThread = None
    interface = None
    def runable(self):
        while True:
            message = self.bus.recv()
            if message is None:
                continue                
            if self.recvCallback is not None:
                self.recvCallback(message)
    def __init__(self, interface='pcan') -> None:
        self.interface = interface
    def open(self):
        if self.interface == 'pcan':
            self.bus = can.Bus(interface=self.interface)
        else:
            self.bus = None
        if self.bus is None:
            return False
        self.recvThread = threading.Thread(target=self.runable)
        self.recvThread.start()
    def close(self):
        self.bus.shutdown()
        self.bus = None
    def send(self, message):
        self.bus.send(message)
    def recv(self):
        return self.bus.recv()
    def setCallback(self, callback):
        self.recvCallback = callback
    def readByIdentifier(self, identifier):
        self.send(can.Message(arbitration_id=identifier, data=[0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        
    
