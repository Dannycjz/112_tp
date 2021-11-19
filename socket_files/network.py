import socket, pickle

'''
Class basically copied from:
www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
Changed the data sending/reception to use pickle instead of string encoding/decoding
'''
class Network(object):
    '''
    Function basically copied from:
    www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
    Removed the self.pos attribute
    '''
    def __init__(self):
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST= "172.26.99.23"
        self.port=5555
        self.addr=(self.HOST, self.port)

    '''
    Function copied from:
    www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
    '''
    def connect(self):
        # Error handling
        try:    
            self.client.connect(self.addr)
            return self.client.recv(2048*2).decode()
        except:
            pass
    
    '''
    Function inspired by:
    www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
    Changed data handling to use pickle and not string encoding/decoding
    '''
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

    