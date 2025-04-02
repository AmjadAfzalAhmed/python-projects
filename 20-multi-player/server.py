import socket
from _thread import *
import pickle
from game import Game

server = "192.168.100.156"
port = 5555 # port number where the server will listen

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a socket for the server

try:
    s.bind((server, port)) # binds the server and port to the socket
except socket.error as e: # if there is an error
    str(e) # prints the error

s.listen(2) # listens for connections
print("Waiting for a connection, Server Started")

connected = set() # stores the ip addresses of the clients that are connected
games = {} # stores the games that are created
idCount = 0 # counts the number of clients that are connected

# handles the connection of the client
def threaded_client(conn, p, gameId):
    global idCount # counts the number of clients that are connected
    conn.send(str.encode(str(p))) # sends the player number to the client

    reply = "" # stores the reply
    while True: 
        try:
            data = conn.recv(4096).decode() # receives the data and decodes it

            if gameId in games: # if the game exists
                game = games[gameId] # gets the game ready

                if not data: # if there is no data
                    break # breaks the loop
                else:
                    if data == "reset": # if the data is reset
                        game.resetWent() # resets the game
                    elif data != "get": # if the data is not get
                        game.play(p, data) # plays the game

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except: # if there is an error
            break # breaks the loop

    print("Lost connection") # prints the loss of connection
    try: # tries to delete the game
        del games[gameId] # deletes the game
        print("Closing Game", gameId) # prints the game id
    except: # if there is an error
        pass # ignores the error
    idCount -= 1 # decrements the id count
    conn.close() # closes the connection



while True:
    conn, addr = s.accept() # accepts the connection
    print("Connected to:", addr) # prints the ip address of the client

    idCount += 1 # increments the id count
    p = 0 # player
    gameId = (idCount - 1)//2 # increments game id 
    if idCount % 2 == 1: # if the id count is odd
        games[gameId] = Game(gameId) # creates a new game
        print("Creating a new game...")
    else:
        games[gameId].ready = True # sets the game as ready
        p = 1 # player

    start_new_thread(threaded_client, (conn, p, gameId)) # starts a new thread for the client