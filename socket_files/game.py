""" 
Object concept copied from 
https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
"""
class Game(object):
    """ 
    Method inspired by
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    Changed the went attribute to indicate which player has went
    Changed the move attribute to tuples instead of a list
    Added attributes blackwins/whiteWins
    Added attribute over to indicate game over state
    """
    def __init__(self, id):
        self.updated=[True, True]
        self.ready=False
        self.id=id
        self.p0move=()
        self.p1move=()
        self.p0Went=False
        self.p1Went=False
        self.enPassant=None
        self.winner=None
        self.over=False
        self.rightCastling=[False, False]
        self.leftCastling=[False, False]
        self.promotingPawnToQueen=False
        self.promotingPawnToBishop=False
        self.promotingPawnToKnight=False
        self.promotingPawnToRook=False

    # For debugging purposes
    def __repr__(self):
        return str(self.id)
    
    """ 
    Function inspired by
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    Changed the function to return my defined move attribute
    """
    def getMove(self, player):
        if player==0:
            return self.p1move
        else:
            return self.p0move

    # Get Went status
    def getWent(self, player):
        if player==0:
            return self.p0Went
        else:
            return self.p1Went

    # Set went status for player
    def setWent(self, player):
        if player==0:
            self.p0Went=True
        else:
            self.p1Went=True
    
    # Reset went status for player
    def resetWent(self, player):
        if player==0:
            self.p1Went=False
        else:
            self.p0Went=False

    # Update the updated list 
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
    
    # Reset all pawn promotion status
    def resetPawnPromotion(self):
        self.promotingPawnToQueen=False
        self.promotingPawnToBishop=False
        self.promotingPawnToKnight=False
        self.promotingPawnToRook=False

    # Set right castling status
    def setRightCastling(self, player):
        self.rightCastling[player]=True

    # Set left castling status
    def setLeftCastling(self, player):
        self.leftCastling[player]=True

    # Returns a tuple of (status, direction)
    # where status is True if the other player has made a castling move
    # False otherwise
    # Status represents the side on which the castling move was made
    def getCastlingStatus(self, player):
        if player==0:
            if self.rightCastling[1]:
                result=(True, "right")
            elif self.leftCastling[1]:
                result=(True, "left")
            else:
                result=(False, None)
        elif player==1:
            if self.rightCastling[0]:
                result=(True, "right")
            elif self.leftCastling[0]:
                result=(True, "left")
            else:
                result=(False, None)
        return result

    # Reset Castling status
    def resetCastling(self):
        self.rightCastling=[False, False]
        self.leftCastling=[False, False]

    # Set En Passant status
    def setEnPassant(self, player):
        if player==0:
            self.enPassant=1
        elif player==1:
            self.enPassant=0
    
    def resetEnPassant(self):
        self.enPassant=None
    
    # Returns true if the other player executed En Passant
    # False otherwise
    def getEnPassant(self, player):
        if self.enPassant==player:
            return True
        else:
            return False

    """ 
    Method copied from
    https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
    """
    def connected(self):
        return self.ready

    def setWinner(self, player):
        if player==0:
            self.winner=1
        else:
            self.winner=0
    
    def setGameOver(self):
        self.over=True
    
