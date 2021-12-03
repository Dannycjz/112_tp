import socket, pickle

'''
Network class used by local client to connect to the server
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
        # Input IPv4 Address
        self.HOST= "172.26.34.16"
        self.port=5555
        self.addr=(self.HOST, self.port)

    '''
    Function inspired by:
    www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
    Changed the actions in the try method to immediately send the player-
    -choice to the server upon connection
    '''
    def connect(self, player):
        # Error handling
        try:    
            self.client.connect(self.addr)
            self.client.send(str.encode(str(player)))
        except:
            return False
    
    '''
    Function inspired by:
    www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients/
    Changed data handling to use pickle and not string encoding/decoding
    '''
    def send(self, data):
        # Error handling
        try:
            self.client.send(pickle.dumps(data))
            recv_data=pickle.loads(self.client.recv(2048*4))
            return recv_data
        # Prints error to terminal
        except socket.error as e:
            print(e)


    