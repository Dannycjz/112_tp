import socket, sys, pickle
from _thread import *

# Local IPV4 Address for my desktop
# HOST="172.26.19.215"
HOST="172.25.3.242"
port=5555

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, port))
# Error Handling
# prints out error for debugging
except socket.error as e:
    str(e)

# Initiates list in memory to store dots
dots=[(200, 200)]

# Make the socket start listening to connections
s.listen(2)
print("Waiting for a connection, Server Started")

def client_thread(conn):
    # Sends dots back to client to start
    conn.send(pickle.dumps(dots))

    # Continuously check for data from conn
    while True:
        try:
            # Try to receive/decode data 
            data=pickle.loads(conn.recv(2048*2))
            dots.append(data)
            
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
    
# continuously checks for connections 
while True:
    # aceepts incoming connection
    conn, addr=s.accept()
    print("Connected to:", addr)

    start_new_thread(client_thread, (conn, ))