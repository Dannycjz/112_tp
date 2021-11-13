import socket, pickle

'''
Code inspired by:
www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
'''

class Network(object):
    def __init__(self):
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST= "172.26.19.215"
        self.port=5555
        self.addr=(self.HOST, self.port)
        self.dots=self.connect()

    def connect(self):
        # Error handling
        try:    
            self.client.connect(self.addr)
            return self.client.recv(2048*2)
        except:
            pass
    
    def send(self, data):
        # Error handling
        try:
            self.client.send(pickle.dumps(data))
            recv_data=pickle.loads(self.client.recv(2048*2))
            return recv_data
        # Prints error to terminal
        except socket.error as e:
            print(e)

# Debugging stuff
# n=Network()
# dots=pickle.loads(n.dots)
# print(dots)
# dots=n.send((150, 150))
# print(dots)

    