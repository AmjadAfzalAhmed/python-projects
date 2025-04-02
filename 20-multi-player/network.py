import socket
import pickle

# defines the network class
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.100.156" # server IP address of your machine
        self.port = 5555 # port number of your machine
        self.addr = (self.server, self.port) # address of your machine
        self.p = self.connect() # player number

    def getP(self): # returns the player number
        return self.p 

    def connect(self): # connects to the server
        try:
            self.client.connect(self.addr) # connects to the server
            return self.client.recv(2048).decode() # receives the player number
        except:
            pass

    def send(self, data): # sends data to the server
        try:
            self.client.send(str.encode(data)) # sends the data
            return pickle.loads(self.client.recv(2048*2)) # receives the data
        except socket.error as e:
            print(e)

