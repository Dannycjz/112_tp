import tkinter
from cmu_112_graphics import *

def appStarted(app):
    app.board=[[]for i in range(8)]
    app.pieces=init_pieces()
    # Initiates 2D lists to represent killzones
    app.whiteKZ=[[False, False, False, False, 
                False, False, False, False]for i in range(8)]
    app.blackKZ=[[False, False, False, False, 
                False, False, False, False]for i in range(8)]
    app.cellSize=app.width/8
    imageUrl="http://clipart-library.com/images/pcqrGKzLi.png"
    #imageUrl="https://www.clipartmax.com/png/middle/455-4559543_chess-pieces-sprite-chess-pieces-sprite-sheet.png"
    app.chessSprites=app.loadImage(imageUrl)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict()
    init_sprites(app)
    # Initiates 2D list to represent valid moves 
    app.validMoves=[[False, False, False, False, 
                    False, False, False, False]for i in range(8)]
    # Initiates 2D list to represent killzones visually
    app.kzOutlines=[[False, False, False, False, 
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

# Updates killzones based on piece positions
def update_killzones(app):
    for row in range(8):
        for col in range(8):
            elem=app.pieces[row][col]
            color=elem[0]
            piece=elem[1]
            if color=="white" or color=="empty":
                # Gets all possible threat origins
                (pawnSet, castleSet, knightSet, 
                bishopSet, queenSet, kingSet)=blackMoves(app, row, col)
                # Updates killzone accordingly
                update_blackKZ(app, pawnSet, castleSet, knightSet, 
                bishopSet, queenSet, kingSet, row, col)
            if color=="black" or color=="empty":
                # Gets all possible threat origins
                (pawnSet, castleSet, knightSet, 
                bishopSet, queenSet, kingSet)=whiteMoves(app, row, col)
                # Updates killzone accordingly
                update_whiteKZ(app, pawnSet, castleSet, knightSet, 
                bishopSet, queenSet, kingSet, row, col)
            else:
                continue

# returns black moves from [currR][currC]
def blackMoves(app, currR, currC):
    pawnSet=[]
    castleSet=[]
    knightSet=[]
    bishopSet=[]
    queenSet=[]
    kingSet=[]
    for row in range(8):
        for col in range(8):
            if isValidPawnBackTrack(app, currR, currC, row, col, "black"):
                pawnSet.append((row, col))
            if isValidCastleMove(app, currR, currC, row, col):
                castleSet.append((row, col))
            if isValidKnightMove(currR, currC, row, col):
                knightSet.append((row, col))
            if isValidBishopMove(app, currR, currC, row, col):
                bishopSet.append((row, col))
            if isValidQueenMove(app, currR, currC, row, col):
                queenSet.append((row, col))
            if isValidKingMove(app, currR, currC, row, col, "black"):
                kingSet.append((row, col))
    return pawnSet, castleSet, knightSet, bishopSet, queenSet, kingSet

# returns white moves from [currR][currC]
def whiteMoves(app, currR, currC):
    pawnSet=[]
    castleSet=[]
    knightSet=[]
    bishopSet=[]
    queenSet=[]
    kingSet=[]
    for row in range(8):
        for col in range(8):
            if isValidPawnBackTrack(app, currR, currC, row, col, "white"):
                pawnSet.append((row, col))
            if isValidCastleMove(app, currR, currC, row, col):
                castleSet.append((row, col))
            if isValidKnightMove(currR, currC, row, col):
                knightSet.append((row, col))
            if isValidBishopMove(app, currR, currC, row, col):
                bishopSet.append((row, col))
            if isValidQueenMove(app, currR, currC, row, col):
                queenSet.append((row, col))
            if isValidKingMove(app, currR, currC, row, col, "white"):
                kingSet.append((row, col))
    return pawnSet, castleSet, knightSet, bishopSet, queenSet, kingSet

# Updates killzones for black pieces
def update_blackKZ(app, pawnSet, castleSet, knightSet, 
                bishopSet, queenSet, kingSet, currR, currC):
    for coord in pawnSet:
        (row, col)=coord
        if app.pieces[row][col]==("black", "pawn"):
            app.blackKZ[currR][currC]=True
            return
    for coord in castleSet:
        (row, col)=coord
        if app.pieces[row][col]==("black", "castle"):
            app.blackKZ[currR][currC]=True
            return
    for coord in knightSet:
        (row, col)=coord
        if app.pieces[row][col]==("black", "knight"):
            app.blackKZ[currR][currC]=True
            return
    for coord in bishopSet:
        (row, col)=coord
        if app.pieces[row][col]==("black", "bishop"):
            app.blackKZ[currR][currC]=True
            return
    for coord in queenSet:
        (row, col)=coord
        if app.pieces[row][col]==("black", "queen"):
            app.blackKZ[currR][currC]=True
            return
    for coord in kingSet:
        (row, col)=coord
        if app.pieces[row][col]==("black", "king"):
            app.blackKZ[currR][currC]=True
            return
    app.blackKZ[currR][currC]=False

# Updates killzones for white pieces
def update_whiteKZ(app, pawnSet, castleSet, knightSet, 
                bishopSet, queenSet, kingSet, currR, currC):
    for coord in pawnSet:
        (row, col)=coord
        if app.pieces[row][col]==("white", "pawn"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in castleSet:
        (row, col)=coord
        if app.pieces[row][col]==("white", "castle"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in knightSet:
        (row, col)=coord
        if app.pieces[row][col]==("white", "knight"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in bishopSet:
        (row, col)=coord
        if app.pieces[row][col]==("white", "bishop"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in queenSet:
        (row, col)=coord
        if app.pieces[row][col]==("white", "queen"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in kingSet:
        (row, col)=coord
        if app.pieces[row][col]==("white", "king"):
            app.whiteKZ[currR][currC]=True
            return
    app.whiteKZ[currR][currC]=False

# Backtrack pawn check for killzone updates
def isValidPawnBackTrack(app, currR, currC, row, col, color):
    if color=="black":
        if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                return True
        else: return False
    elif color=="white":
        if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
            return True
        else: return False
            
def mousePressed(app, event):
    x=event.x
    y=event.y
    (row, col)=selectCell(app, x, y)
    if app.makingMove is False:
        elem=selectPiece(app, row, col)
        if elem!=None:
            color=elem[0]
            updateKZOutlines(app, color)
            updateValidMoves(app)
        else:
            clearValidMoves(app)
            clearKZOutlines(app)
    else:
        if isValidMove(app, row, col):
            makeMove(app, row, col)
            clearValidMoves(app)
            clearKZOutlines(app)
        else:
            unselectPiece(app)
            clearValidMoves(app)
            clearKZOutlines(app)

# Updates outlines for the killzones
def updateKZOutlines(app, color):
    if color=="white":
        app.kzOutlines=copy.deepcopy(app.blackKZ)
    elif color=="black":
        app.kzOutlines=copy.deepcopy(app.whiteKZ)

# Clears outlines and killzones
def clearKZOutlines(app):
    for row in range(8):
        for col in range(8):
            app.kzOutlines[row][col]=False

def timerFired(app):
    update_killzones(app)

# Selects a cell on the chessboard
def selectCell(app, x, y):
    for row in range(8):
        for col in range(8):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if (x in range(int(x0), int(x1))) and (y in range(int(y0), int(y1))):
                return (row, col)

# Unselect the selected piece
def unselectPiece(app):
    app.selectedPiece=None
    app.currLoc=None
    app.selectedPiece=None
    app.makingMove=False

# Selects a chess piece if the user clicks on one
def selectPiece(app, row, col):
    if app.pieces[row][col]!=("empty", "empty"):
        app.selectedPiece=app.pieces[row][col]
        app.currLoc=(row, col)
        app.makingMove=True
        return app.selectedPiece
    else:
        return None

# Moves the selected chess piece to the destination cell
def makeMove(app, row, col):
    currR=app.currLoc[0]
    currC=app.currLoc[1]
    app.pieces[currR][currC]=("empty", "empty")
    app.pieces[row][col]=app.selectedPiece
    app.selectedPiece=None
    app.currLoc=None
    app.makingMove=False

# Clear valid moves
def clearValidMoves(app):
    for row in range(8):
        for col in range(8):
            app.validMoves[row][col]=False

# Updates valid moves for selected piece in [currR][currC]
def updateValidMoves(app):
    for row in range(8):
        for col in range(8):
            if isValidMove(app, row, col):
                app.validMoves[row][col]=True

# Checks if [row][col] is a valid move from [currR][currC]
def isValidMove(app, row, col):
    currR=app.currLoc[0]
    currC=app.currLoc[1]
    color=app.selectedPiece[0]
    piece=app.selectedPiece[1]
    # Checks for friendly piece collision
    if app.pieces[row][col][0]==color: return False
    # Checks valid moves based on piece type
    if piece=="pawn":
        return isValidPawnMove(app, currR, currC, row, col, color)
    elif piece=="castle":
        return isValidCastleMove(app, currR, currC, row, col)
    elif piece=="knight":
        return isValidKnightMove(currR, currC, row, col)
    elif piece=="bishop":
        return isValidBishopMove(app, currR, currC, row, col)
    elif piece=="queen":
        return isValidQueenMove(app, currR, currC, row, col)
    elif piece=="king":
        return isValidKingMove(app, currR, currC, row, col, color)

# Checks if [row][col] is a valid start pawn move from [currR][currC]
def isValidStartPawnMove(app, currR, currC, row, col, color):
    pass

# Checks if [row][col] is a valid normal pawn move from [currR][currC]
def isValidPawnMove(app, currR, currC, row, col, color):
    if color=="black":
        # Empty cells move set
        if app.pieces[row][col]==("empty", "empty"):
            if (col==currC) and (currR==row-1):
                return True
            else: return False
        # Enemy eating movement set
        else:
            if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
                return True
            else: return False
    else:
        # Empty cells move set
        if app.pieces[row][col]==("empty", "empty"):
            if (col==currC) and (currR==row+1):
                return True
            else: return False
        # Enemy eating movement set
        else:
            if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                return True
            else: return False

# Checks if [row][col] is a valid castle move from [currR][currC]
def isValidCastleMove(app, currR, currC, row, col):
    # Gets the furthest possible column positions
    leftC, rightC=nearestPieceOnRow(app, currR, currC)
    # Gets the furthest possible row positions
    topR, botR=nearestPieceOnCol(app, currR, currC)
    if col==currC:
        if botR<=row<=topR:
            return True
        else: return False 
    elif row==currR:
        if leftC<=col<=rightC:
            return True
        else: return False 
    else: return False
 
 # Checks if [row][col] is a valid knight move from [currR][currC]
def isValidKnightMove(currR, currC, row, col):
    if (currR+1==row) or (currR-1==row):
        if (currC+2==col) or (currC-2==col):
            return True
    elif (currC+1==col) or (currC-1==col):
        if (currR+2==row) or (currR-2==row):
            return True
    return False

# Checks if [row][col] is a valid bishop move from [currR][currC]
def isValidBishopMove(app, currR, currC, row, col):
    leftD, Lindex=Ldiag(currR, currC)
    Lleft, Lright=nearestPieceLDiag(app, currR, currC)
    rightD, Rindex=Rdiag(currR, currC)
    Rleft, Rright=nearestPieceRDiag(app, currR, currC)
    for coord in rightD[Rleft:Rright+1]:
        if (row, col)==coord:
            return True
    for coord in leftD[Lleft:Lright+1]:
        if (row, col)==coord:
            return True
    return False

# Checks if [row][col] is a valid queen move from [currR][currC]
def isValidQueenMove(app, currR, currC, row, col):
    return (isValidBishopMove(app, currR, currC, row, col) or
                isValidCastleMove(app, currR, currC, row, col))

# Checks if [row][col] is a valid king move from [currR][currC]
def isValidKingMove(app, currR, currC, row, col, color):
    # Checks if destination is in killzone
    if color=="black":
        if app.whiteKZ[row][col] is True:
            return False
    elif color=="white":
        if app.blackKZ[row][col] is True:
            return False
    if (((currR+1==row) or (currR-1==row) or (currR==row)) 
        and ((currC+1==col) or (currC-1==col) or (currC==col))):
        return True
    else: return False

# Returns the coordinates of the closest pieces to [currR][currC] 
# on the same left diagonal
def nearestPieceLDiag(app, currR, currC):
    diag, index=Ldiag(currR, currC)
    left=0
    right=len(diag)-1
    i=index-1
    while i>=0:
        (row, col)=diag[i]
        if app.pieces[row][col]!=("empty", "empty"):
            left=i
            break
        i-=1
    i=index+1
    while i<len(diag):
        (row, col)=diag[i]
        if app.pieces[row][col]!=("empty", "empty"):
            right=i
            break
        i+=1
    return left, right

# Returns the coordinates of the closest pieces to [currR][currC] 
# on the same right diagonal
def nearestPieceRDiag(app, currR, currC):
    diag, index=Rdiag(currR, currC)
    left=0
    right=len(diag)-1
    i=index-1
    while i>=0:
        (row, col)=diag[i]
        if app.pieces[row][col]!=("empty", "empty"):
            left=i
            break
        i-=1
    i=index+1
    while i<len(diag):
        (row, col)=diag[i]
        if app.pieces[row][col]!=("empty", "empty"):
            right=i
            break
        i+=1
    return left, right
    
# Returns left diagonal of [currR][currC] as a list
def Ldiag(currR, currC):
    result=[]
    row=currR-1
    col=currC-1
    while row>=0 and col>=0:
        result.append((row, col))
        row-=1
        col-=1
    index=len(result)
    result.reverse()
    result.append((currR, currC))
    row=currR+1
    col=currC+1
    while row<8 and col<8:
        result.append((row, col))
        row+=1
        col+=1
    return result, index

# Returns right diagonal of [currR][currC] as a list
def Rdiag(currR, currC):
    result=[]
    row=currR+1
    col=currC-1
    while row<8 and col>=0:
        result.append((row, col))
        row+=1
        col-=1
    index=len(result)
    result.reverse()
    result.append((currR, currC))
    row=currR-1
    col=currC+1
    while row>=0 and col<8:
        result.append((row, col))
        row-=1
        col+=1
    return result, index

# Returns the row of the closest piece to [currR][currC] on the same column
def nearestPieceOnRow(app, currR, currC):
    rightC=7
    leftC=0
    i=currC+1
    while i<8:
        if app.pieces[currR][i]!=("empty", "empty"):
            rightC=i
            break
        i+=1
    i=currC-1
    while i>=0:
        if app.pieces[currR][i]!=("empty", "empty"):
            leftC=i
            break
        i-=1
    return leftC, rightC

# Returns the col of the closest piece to [currR][currC] on the same row
def nearestPieceOnCol(app, currR, currC):
    topR=7
    botR=0
    i=currR+1
    while i<8:
        if app.pieces[i][currC]!=("empty", "empty"):
            topR=i
            break
        i+=1
    i=currR-1
    while i>=0:
        if app.pieces[i][currC]!=("empty", "empty"):
            botR=i
            break
        i-=1
    return topR, botR

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
    if app.kzOutlines[row][col] is True:
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='red', 
                                width=4)
    elif app.validMoves[row][col] is True:
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='green', 
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