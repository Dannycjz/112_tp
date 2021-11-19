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
        self.updated=[False, False]
        self.ready=False
        self.id=id
        self.p0move=()
        self.p1move=()
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
    def getMove(self, player):
        if player==0:
            return self.p1move
        else:
            return self.p0move

    def setUpdated(self, player):
        self.updated[player]=True
    
    # Resets the updated status for the other player
    # Since player just made a new move
    def resetUpdated(self, player):
        if player==0:
            self.updated[1]=False
        else:
            self.updated[0]=False

    """ 
    Method inspired by
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    Changed the function to better fit my defined attributes
    """
    def updateMove(self, player, move):
        if player==0:
            self.p0move=move
        else:
            self.p1move=move

    """ 
    Method copied from
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    """
    def connected(self):
        return self.ready

    def winner(self):
        pass
    
