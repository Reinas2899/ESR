from enum import Enum
import pickle

class PacoteTipo(Enum):
    FLOOD_REQUEST = 1
    FLOOD_REPLY = 2
    FLOOD_ERR = 3

    VIDEO_REQUEST = 4
    VIDEO_REPLY = 5
    VIDEO_ERR = 6

    SHUTDOWN = 7

class Pacote:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    def __str__(self) -> str:
        return f"Pacote(type={self.type}, \ndata={self.data})"
    
class Message:
    HEADER_LENGTH = 8
    MESSAGE_LENGTH = 1024

    @staticmethod
    def send_message(socket, message):
        message = pickle.dumps(message)
        
        message_len = len(message)
        message_header = message_len.to_bytes(Message.HEADER_LENGTH, "big")

        socket.sendall(message_header + message)

    @staticmethod
    def send_message_udp(socket, message, addr):
        message = pickle.dumps(message)
        
        message_len = len(message)
        message_header = message_len.to_bytes(Message.HEADER_LENGTH, "big")

        socket.sendto(message_header + message, addr)

    @staticmethod
    def receive_message(socket):
        message_header = socket.recv(Message.HEADER_LENGTH)

        if not message_header:
            return None

        message_len = int.from_bytes(message_header, "big")
        message = socket.recv(message_len)

        return Message.deserialize_message(message)
    
    @staticmethod
    def receive_message_udp(socket):
        bufferSize = 20480
        message, addr = socket.recvfrom(bufferSize)

        if not message:
            return None

        msg = Message.deserialize_message(message)

        return (msg, addr)

    @staticmethod
    def deserialize_message(message):
        try:
            data = pickle.loads(message)
        except EOFError:
            data = None
        return data