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
HOST = "172.26.2.71"
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

games={}
idCount=0
gameId=0

'''
Code inspired by 
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
Changed the sending/receiving to use pickle
Changed the data handling to fit my game object
Added commands to control chess moves
'''
def client_thread(conn, player, gameId):
    global idCount

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
                # If there is a checkmate
                # Set game to be over
                elif type(data)==str and data=="Checkmate":
                    game.setGameOver()
                    game.setWinner(player)
                    print(player, "just lost")
                # Deals with special moves
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
                elif type(data)==str and data=="promotedPawnToQueen":
                    game.promotingPawnToQueen=True
                    game.resetUpdated(player)
                elif type(data)==str and data=="promotedPawnToBishop":
                    game.promotingPawnToBishop=True
                    game.resetUpdated(player)
                elif type(data)==str and data=="promotedPawnToKnight":
                    game.promotingPawnToKnight=True
                    game.resetUpdated(player)
                elif type(data)==str and data=="promotedPawnToRook":
                    game.promotingPawnToRook=True
                    game.resetUpdated(player)
                elif type(data)==str and data=="resetPawnPromotion":
                    game.resetPawnPromotion()
                    game.setUpdated(player)
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
Code inspired by
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
Added gameId and player assignment to allow players to choose either white or black
Added a loop through all the existing games to decide whether a new player should join-
-an existing game or have a new game created for them
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

    # Keeps track of whether the player is connected into a game
    connected=False
    
    # Creates a new game if there are an odd number of connections
    if len(games.items())==0:
        games[gameId]=Game(gameId)
        games[gameId].open[int(player)] = False
        print(f"Created a new game...:{gameId}")
        print(games)
        start_new_thread(client_thread, (conn, int(player), gameId))
    else:
        # Checks all current games to see if there's an open spot
        for gameId in games:
            game=games[gameId]
            if game.open[int(player)]:
                games[gameId].ready=True
                games[gameId].open[int(player)] = False
                print(f"Second player connected to game{gameId}")
                print(games)
                start_new_thread(client_thread, (conn, int(player), gameId))
                connected=True
                break
        if connected==False:
            # Opens a new game if no current ones are open
            gameId+=1
            games[gameId]=Game(gameId)
            games[gameId].open[int(player)] = False
            print(f"Created a new game...:{gameId}")
            print(games)
            start_new_thread(client_thread, (conn, int(player), gameId))
            connected=True
    
    for gameId in games:
        print(games[gameId].open, gameId)


