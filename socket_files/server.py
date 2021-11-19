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
Code basically copied from
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
'''
# Input Local IPV4 Address
HOST = "172.26.99.23"
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
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
Changed the sending/receiving to use pickle
Changed the data handling to fit my game object
'''
def client_thread(conn, player, gameId):
    global idCount
    # Sends assigned gameId back to client to start
    conn.send(str.encode(str(player)))

    reply=""
    # Continuously check for data from conn
    while True:
        try:
            # Try to receive/decode data 
            data=pickle.loads(conn.recv(2048*2))

            if gameId in games:
                game=games[gameId]
                # Break connection if the client is not sending data
                if not data:
                    print("Disconnected")
                    break
                # elif type(data)==str and data=="get":
                #     reply=game
                elif type(data)==tuple:
                    game.updateMove(player, data)

                conn.sendall(pickle.dumps(game))
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

'''
Code basically copied from
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
'''
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
        print(f"Created a new game...:{gameId}")
        print(games)
    else:
        games[gameId].ready = True
        player=1
        print(f"Second player connected to game{gameId}")
        print(games)

    start_new_thread(client_thread, (conn, player, gameId))
