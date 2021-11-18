""" 
Code inspired by 
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
"""
class Game(object):
    def __init__(self, id):
        self.p0Went=False
        self.p1Went= False
        self.ready=False
        self.id=id
        self.moves={}
        self.whiteWins=False
        self.blackWins=False
        self.ties=0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def winner(self):
        pass

    def resetWent(self, player):
        self.p1Went = False
        self.p2Went = False