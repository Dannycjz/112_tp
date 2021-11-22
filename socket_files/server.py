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
HOST = "172.26.19.215"
port=5555

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, port))
# Error Handling
# prints out error for debugging
except socket.error as e:
    str(e)

# Make the socket start listening to connections
s.listen()
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

    reply=""
    # Continuously check for data from conn
    while True:
        try:
            # Try to receive/decode data 
            data=pickle.loads(conn.recv(2048*4))

            if gameId in games:
                game=games[gameId]
                # Break connection if the client is not sending data
                if not data:
                    print("Disconnected")
                    break
                # Updates the updated status 
                elif type(data)==str and data=="Updated":
                    game.setUpdated(player)
                    print("Updated", player)
                    print(game.updated)
                # Set the went status for the player if requested
                elif type(data)==str and data=="setWent":
                    game.setWent(player)
                    print(game.getWent(player), player, "Went")
                elif type(data)==str and data=="Checkmate":
                    game.setGameOver()
                    game.setWinner(player)
                    print(player, "just lost")
                elif type(data)==str and data=="EnPassant":
                    game.setEnPassant(player)
                    game.resetCastling()
                    print(player, "just got en passanted")
                elif type(data)==str and data=="resetSpecialMoves":
                    game.resetCastling()
                    game.resetEnPassant()
                elif type(data)==str and data=="RightCastling":
                    game.setRightCastling(player)
                    game.resetEnPassant()
                elif type(data)==str and data=="LeftCastling":
                    game.setLeftCastling(player)
                    game.resetEnPassant()
                # if data is a move
                # update the move
                # reset update status so the other player can pull the move
                elif type(data)==tuple:
                    print(data, player)
                    game.updateMove(player, data)
                    game.resetUpdated(player)
                    game.resetWent(player)
                    print("Reset requested by:", player)
                    print(game.updated)
                    
                conn.sendall(pickle.dumps(game))
            else:
                print("gameId not in games")
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

    # Receives player data on initial connection
    player=conn.recv(4096).decode()
    print("The player wants to play as", player)

    # Keeps track of how many people are connected to the server
    idCount+=1
    gameId=(idCount-1)//2
    
    # Creates a new game if there are an odd number of connections
    if (idCount%2==1) and (int(player)==0):
        games[gameId]=Game(gameId)
        print(f"Created a new game...:{gameId}")
        print(games)
        start_new_thread(client_thread, (conn, int(player), gameId))
    elif idCount%2==1:
        conn.close()
        idCount-=1
        print("Connection closed", addr)
    else:
        games[gameId].ready = True
        print(f"Second player connected to game{gameId}")
        print(games)
        start_new_thread(client_thread, (conn, int(player), gameId))
