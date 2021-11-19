""" 
Object concept copied from 
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
"""
class Game(object):
    """ 
    Method inspired by
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    Changed the went attribute to indicate which player has went
    Changed the move method to a tuple instead of a list
    Added attributes blackwins/whiteWins
    Added attribute over to indicate game over state
    """
    def __init__(self, id):
        self.went=None
        self.ready=False
        self.id=id
        self.move=()
        self.whiteWins=False
        self.blackWins=False
        self.over=False
        self.ties=0
    
    def __repr__(self):
        return str(self.id)
    
    """ 
    Method inspired by
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    Changed the function to return my defined move attribute
    """
    def getMove(self):
        return self.move

    """ 
    Method inspired by
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    Changed the function to better fit my defined attributes
    """
    def updateMove(self, player, move):
        self.move = move
        if player == 0:
            self.went=1
        else:
            self.went=0

    """ 
    Method copied from
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    """
    def connected(self):
        return self.ready

    def winner(self):
        pass
    
    """ 
    Method copied from
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    Probably going to change this just havn't gotten to it yet
    """
    def resetWent(self, player):
        self.p1Went = False
        self.p2Went = False