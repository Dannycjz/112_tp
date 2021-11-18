""" 
Code inspired by 
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
"""
from tkinter.constants import FALSE


class Game(object):
    def __init__(self, id):
        self.went=None
        self.ready=False
        self.id=id
        self.move=()
        self.whiteWins=False
        self.blackWins=False
        self.ties=0
    
    def getMove(self):
        return self.move

    def updateMove(self, player, move):
        self.move = move
        if player == 0:
            self.went=1
        else:
            self.went=0

    def connected(self):
        return self.ready

    def winner(self):
        pass

    def resetWent(self, player):
        self.p1Went = False
        self.p2Went = False