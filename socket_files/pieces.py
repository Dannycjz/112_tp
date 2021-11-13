# A common class that has properties for all pieces
class piece(object):
    # Initiates the piece's color/status
    def __init__(self, color):
        self.color=color
        self.killed=False
    
    # Checks if a piece is white or black
    def isWhite(self):
        if self.color=="white":
            return True
        else: 
            return False
    
    # Checks if a piece is killed
    def isKilled(self):
        return self.killed
    
    # Kill a piece
    def kill(self):
        self.killed=not self.killed

class king(piece):
    def validMove(self, startSpot, endSpot):
        pass
