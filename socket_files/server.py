"""References for this file:
    https://docs.python.org/3/library/socket.html
    https://docs.python.org/3/library/_thread.html
    https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
    https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
"""
import socket, sys, pickle
from _thread import *

# Initiates list in memory to store dots
dots=[(200, 200, "red")]

'''
Code inspired by
https://www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
'''
def main():
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
    s.listen()
    print("Waiting for a connection, Server Started")

    # Tracks current player
    currentPlayer=0
    # continuously checks for connections 
    while True:
        # aceepts incoming connection
        conn, addr=s.accept()
        print("Connected to:", addr)

        start_new_thread(client_thread, (conn, currentPlayer))
        currentPlayer+=1

'''
Code inspired by 
https://www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
'''
def client_thread(conn, currentPlayer):
    if currentPlayer==0: 
        color=("red", )
    else:
        color=("green", )
    
    # Sends dots back to client to start
    conn.send(pickle.dumps(dots))

    # Continuously check for data from conn
    while True:
        try:
            # Try to receive/decode data 
            data=pickle.loads(conn.recv(2048*2))
            dot=data+color
            dots.append(dot)
            
            # Break connection if the client is not sending data
            if not data:
                print("Disconnected")
                break
            else: 
                print(dots)
            
            # Encode info before sending it to the client
            conn.sendall(pickle.dumps(dots))
        
        # Error handling
        except:
            break
    
    # If disconnected:
    print("Lost connection")
    conn.close()

if __name__=="__main__":
    main()