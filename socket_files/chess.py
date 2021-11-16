import tkinter
from cmu_112_graphics import *

def appStarted(app):
    app.board=[[]for i in range(8)]
    app.pieces=init_pieces()
    app.cellSize=app.width/8
    imageUrl="http://clipart-library.com/images/pcqrGKzLi.png"
    #imageUrl="https://www.clipartmax.com/png/middle/455-4559543_chess-pieces-sprite-chess-pieces-sprite-sheet.png"
    app.chessSprites=app.loadImage(imageUrl)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict()
    init_sprites(app)
    # Initiates 2D list to represent which cell should be outlined on the board
    app.outlined=[[False, False, False, False, 
                    False, False, False, False]for i in range(8)]
    # Initiates a variable that stores which piece is selected
    app.selectedPiece=None
    # Initiates a variable that indicates whether a player is making a move
    app.makingMove=False
    # Initiates a variable that stores the current location of the selected piece
    app.currLoc=None

# Original code inspired by https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#loadImageUsingUrl
# Loads chess sprites and stores them in dicts
def init_sprites(app):
    app.chessSprites=app.scaleImage(app.chessSprites, 0.25)
    width, height=app.chessSprites.size
    possiblePieces=["king0", "queen1", "bishop2", "knight3", "castle4", "pawn5"]
    for piece in possiblePieces:
        index=int(piece[-1])
        newPiece=piece[:-1]
        leftx=index*(width/6)
        rightx=(index+1)*(width/6)
        whiteSprite=app.chessSprites.crop((leftx, 0, rightx, height/2))
        blackSprite=app.chessSprites.crop((leftx, height/2, rightx, height))
        app.whitePieces[newPiece]=whiteSprite
        app.blackPieces[newPiece]=blackSprite

# Initializes 2D list to store the locations of pieces on board
def init_pieces():
    pieces=[
        [("black", "castle"), ("black", "knight"), ("black", "bishop"), 
        ("black", "queen"), ("black", "king"), ("black", "bishop"), 
        ("black", "knight"), ("black", "castle")],
        [("black", "pawn")for i in range(8)], 
        [("empty", "empty")for i in range(8)], 
        [("empty", "empty")for i in range(8)], 
        [("empty", "empty")for i in range(8)], 
        [("empty", "empty")for i in range(8)], 
        [("white", "pawn")for i in range(8)], 
        [("white", "castle"), ("white", "knight"), ("white", "bishop"), 
        ("white", "queen"), ("white", "king"), ("white", "bishop"), 
        ("white", "knight"), ("white", "castle")]
        ]
    return pieces

def mousePressed(app, event):
    x=event.x
    y=event.y
    cell=selectCell(app, x, y)
    if cell!=None:
        row=cell[0]
        col=cell[1]
        if app.makingMove is False:
            selectPiece(app, row, col)
            updateValidMoves(app)
        else:
            if isValidMove(app, row, col):
                makeMove(app, row, col)
                clearOutlines(app)

# Selects a cell on the chessboard
def selectCell(app, x, y):
    if app.makingMove is False:
        for row in range(8):
            for col in range(8):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                if (x in range(int(x0), int(x1))) and (y in range(int(y0), int(y1))):
                    app.outlined[row][col]=True
                    selectedCell=(row, col)
        return selectedCell

# Selects a chess piece if the user clicks on one
def selectPiece(app, row, col):
    if app.pieces[row][col]!=("empty", "empty"):
        app.selectedPiece=app.pieces[row][col]
        app.currLoc=(row, col)
        app.makingMove=True
    else:
        pass

# Moves the selected chess piece to the destination cell
def makeMove(app, row, col):
    currR=app.currLoc[0]
    currC=app.currLoc[1]
    app.pieces[currR][currC]=("empty", "empty")
    app.pieces[row][col]=app.selectedPiece
    app.selectedPiece=None
    app.currLoc=None
    app.makingMove=False

# Clear outlines
def clearOutlines(app):
    for row in range(8):
        for col in range(8):
            app.outlined[row][col]=False

# Updates valid moves for selected piece in [currR][currC]
def updateValidMoves(app):
    for row in range(8):
        for col in range(8):
            if isValidMove(app, row, col):
                app.outlined[row][col]=True

# Checks if [row][col] is a valid move from [currR][currC]
def isValidMove(app, row, col):
    currR=app.currLoc[0]
    currC=app.currLoc[1]
    piece=app.selectedPiece[1]
    if piece=="pawn":
        return isValidPawnMove(app, currR, currC, row, col)

# Checks if [row][col] is a valid pawn move from [currR][currC]
def isValidPawnMove(app, currR, currC, row, col):
    color=app.selectedPiece[0]
    if color=="black":
        if app.pieces[row][col]==("empty", "empty"):
            if (col==currC) and (currR==row-1):
                return True
            else:
                return False
        else:
            if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
                return True
            else:
                return False
    else:
        if app.pieces[row][col]==("empty", "empty"):
            if (col==currC) and (currR==row+1):
                return True
            else:
                return False
        else:
            if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                return True
            else:
                return False

# Returns (x, y) center of given cell in grid
def getCellCenter(app, row, col):
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    x=(x0+x1)/2
    y=(y0+y1)/2
    return (x, y)

# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
# # Function partially taken from 15-112 website 
def getCellBounds(app, row, col):
    x0 = col * app.cellSize
    x1 = (col+1) * app.cellSize
    y0 = row * app.cellSize
    y1 = (row+1) * app.cellSize
    return (x0, y0, x1, y1)

# draw grid of cells
# Function partially taken from 15-112 website 
def drawCell(app, canvas, row, col):
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    if row%2==0 and col%2!=0:
        fill="grey"
    elif row%2!=0 and col%2==0:
        fill="grey"
    else:
        fill="white"
    if app.outlined[row][col] is True:
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='red', 
                                width=4)
    else:
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='black', 
                                width=3)

# Draws the chess board
def drawBoard(app, canvas):
    for row in range(8): 
        for col in range(8): 
            drawCell(app, canvas, row, col)

# Loads pieces onto chess board
def loadPieces(app, canvas):
    for row in range(8):
        for col in range(8):
            (x, y)=getCellCenter(app, row, col)
            (color, piece)=app.pieces[row][col]
            if color=="black":
                sprite=app.blackPieces[piece]
            elif color=="white":
                sprite=app.whitePieces[piece]
            else:
                continue
            canvas.create_image(x, y, image=ImageTk.PhotoImage(sprite))

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    loadPieces(app, canvas)

def chessAnimation():
    runApp(width=800, height=800)

if __name__=="__main__":
    chessAnimation()