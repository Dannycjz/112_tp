"""References for this file:
    https://docs.python.org/3/library/socket.html
    https://docs.python.org/3/library/_thread.html
    https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
    https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
"""
import socket, sys, pickle
from _thread import *
from game import Game

'''
Code inspired by
https://www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
'''
# Local IPV4 Address
HOST = "172.26.18.51"
port=5555

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, port))
# Error Handling
# prints out error for debugging
except socket.error as e:
    str(e)

# Make the socket start listening to connections
s.listen(2)
print("Waiting for a connection, Server Started")

connected=set()
games={}
idCount=0

'''
Code inspired by 
https://www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
'''
def client_thread(conn, player, gameId):
    global idCount
    # Sends assigned gameId back to client to start
    conn.send(str.encode(str(player)))

    # Continuously check for data from conn
    while True:
        try:
            # Try to receive/decode data 
            data=pickle.loads(conn.recv(2048*2))

            if gameId in games:
                # Break connection if the client is not sending data
                if not data:
                    print("Disconnected")
                    break
                else:
                    if player==0:
                        pass
            else:
                break
        # Error handling
        except:
            break
    
    # If disconnected:
    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount-=1
    conn.close()

# continuously checks for connections 
while True:
    # aceepts incoming connection
    conn, addr=s.accept()
    print("Connected to:", addr)

    # Keeps track of how many people are connected to the server
    idCount+=1
    player=0
    gameId=(idCount-1)//2
    
    # Creates a new game if there are an odd number of connections
    if idCount%2==1:
        games[gameId]=Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        player=1

    start_new_thread(client_thread, (conn, player, gameId))
