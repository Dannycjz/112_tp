import socket
from _thread import *
import sys

# Local IPV4 Address for my desktop
server="172.26.19.215"
port=5555

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
# Error Handling
# prints out error for debugging
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    reply=" "
    # Continuously check for data from conn
    while True:
        try:
            # Try to receive data (2048 bits)
            data=conn.recv(2048)
            # Decode the data in utf-8 format
            reply=data.decode("utf-8")
            
            # Break connection if the client is not sending data
            if not data:
                print("Disconnected")
                break
            else:
                print("Received:", reply)
                print("Sending:", reply)
            
            # Encode info before sending it to the client
            conn.sendall(str.encode(reply))
        
        # Error handling
        except:
            break
# continuously checks for connections 
while True:
    # aceepts incoming connection
    conn, addr=s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, ))