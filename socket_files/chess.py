import tkinter, pickle
from cmu_112_graphics import *
from network import Network

def appStarted(app):
    app.n=Network()
    app.player=int(app.n.connect())
    app.game=None
    app.board=[[]for i in range(8)]
    # Initates boolean variable to detect whether a king is being checked
    app.check=False
    app.checkMate=False
    # Initiates a variable to store the location of the king
    app.kingLoc=initiateKingLoc(app, app.player)
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
    # Initiates a variable that indicates whether a player is making a move
    app.makingMove=False
    # Initiates a variable that stores the current location of the selected piece
    app.oldLoc=None
    # Initiates a variable that keeps track of whether the local board is updated
    app.updated=False

# Initiates the correct king location based on which player we are
def initiateKingLoc(app, player):
    if player==0:
        return (7, 4)
    elif player==1:
        return (0, 4)

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
# 0 stands for white, 1 stands for black
def init_pieces():
    pieces=[
        [(1, "castle"), (1, "knight"), (1, "bishop"), 
        (1, "queen"), (1, "king"), (1, "bishop"), 
        (1, "knight"), (1, "castle")],
        [(1, "pawn")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(0, "pawn")for i in range(8)], 
        [(0, "castle"), (0, "knight"), (0, "bishop"), 
        (0, "queen"), (0, "king"), (0, "bishop"), 
        (0, "knight"), (0, "castle")]
        ]
    return pieces

# Updates killzones based on piece positions
def update_killzones(app):
    for row in range(8):
        for col in range(8):
            elem=app.pieces[row][col]
            color=elem[0]
            piece=elem[1]
            # Gets all possible threat origins for white side
            (BpawnSet, BcastleSet, BknightSet, 
            BbishopSet, BqueenSet, BkingSet)=blackMoves(app, row, col)
            # Gets all possible threat origins for black side
            (WpawnSet, WcastleSet, WknightSet, 
            WbishopSet, WqueenSet, WkingSet)=whiteMoves(app, row, col)
            # Updates killzone accordingly
            update_blackKZ(app, BpawnSet, BcastleSet, BknightSet, 
            BbishopSet, BqueenSet, BkingSet, row, col)
            update_whiteKZ(app, WpawnSet, WcastleSet, WknightSet, 
            WbishopSet, WqueenSet, WkingSet, row, col)

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
            if row==currR and col==currC:
                continue
            else:
                if isValidPawnBackTrack(app, currR, currC, row, col, 1):
                    pawnSet.append((row, col))
                if isValidCastleMove(app, currR, currC, row, col, 1):
                    castleSet.append((row, col))
                if isValidKnightMove(app, currR, currC, row, col, 1):
                    knightSet.append((row, col))
                if isValidBishopMove(app, currR, currC, row, col, 1):
                    bishopSet.append((row, col))
                if isValidQueenMove(app, currR, currC, row, col, 1):
                    queenSet.append((row, col))
                if isValidKingMove(app, currR, currC, row, col, 1):
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
            if isValidPawnBackTrack(app, currR, currC, row, col, 0):
                pawnSet.append((row, col))
            if isValidCastleMove(app, currR, currC, row, col, 0):
                castleSet.append((row, col))
            if isValidKnightMove(app, currR, currC, row, col, 0):
                knightSet.append((row, col))
            if isValidBishopMove(app, currR, currC, row, col, 0):
                bishopSet.append((row, col))
            if isValidQueenMove(app, currR, currC, row, col, 0):
                queenSet.append((row, col))
            if isValidKingMove(app, currR, currC, row, col, 0):
                kingSet.append((row, col))
    return pawnSet, castleSet, knightSet, bishopSet, queenSet, kingSet

# Updates killzones for black pieces
def update_blackKZ(app, pawnSet, castleSet, knightSet, 
                bishopSet, queenSet, kingSet, currR, currC):
    for coord in pawnSet:
        (row, col)=coord
        if app.pieces[row][col]==(1, "pawn"):
            app.blackKZ[currR][currC]=True
            return 
    for coord in castleSet:
        (row, col)=coord
        if app.pieces[row][col]==(1, "castle"):
            app.blackKZ[currR][currC]=True
            return
    for coord in knightSet:
        (row, col)=coord
        if app.pieces[row][col]==(1, "knight"):
            app.blackKZ[currR][currC]=True
            return
    for coord in bishopSet:
        (row, col)=coord
        if app.pieces[row][col]==(1, "bishop"):
            app.blackKZ[currR][currC]=True
            return
    for coord in queenSet:
        (row, col)=coord
        if app.pieces[row][col]==(1, "queen"):
            app.blackKZ[currR][currC]=True
            return
    for coord in kingSet:
        (row, col)=coord
        if app.pieces[row][col]==(1, "king"):
            app.blackKZ[currR][currC]=True
            return
    app.blackKZ[currR][currC]=False

# Updates killzones for white pieces
def update_whiteKZ(app, pawnSet, castleSet, knightSet, 
                bishopSet, queenSet, kingSet, currR, currC):
    for coord in pawnSet:
        (row, col)=coord
        if app.pieces[row][col]==(0, "pawn"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in castleSet:
        (row, col)=coord
        if app.pieces[row][col]==(0, "castle"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in knightSet:
        (row, col)=coord
        if app.pieces[row][col]==(0, "knight"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in bishopSet:
        (row, col)=coord
        if app.pieces[row][col]==(0, "bishop"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in queenSet:
        (row, col)=coord
        if app.pieces[row][col]==(0, "queen"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in kingSet:
        (row, col)=coord
        if app.pieces[row][col]==(0, "king"):
            app.whiteKZ[currR][currC]=True
            return
    app.whiteKZ[currR][currC]=False

# Backtrack pawn check for killzone updates
def isValidPawnBackTrack(app, currR, currC, row, col, color):
    if color==1:
        if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                return True
        else: return False
    elif color==0:
        if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
            return True
        else: return False
            
def mousePressed(app, event):
    x=event.x
    y=event.y
    if not app.game.getWent(app.player) and not app.checkMate:
        (row, col)=selectCell(app, x, y)
        # If user is not currently making a move
        # Either select a piece or clear moves/outlines
        if app.makingMove is False:
            piece=selectPiece(app, row, col)
            if piece is None: pass
            elif piece[0]!=app.player:
                unselectPiece(app)
                clearOutlines(app)
                app.makingMove=False
            else:
                updateOutlines(app, app.player, row, col)
                app.makingMove=True
        else:
            if app.game.connected():
                currR=app.oldLoc[0]
                currC=app.oldLoc[1]
                if not isChecked(app):
                    movePiece(app, row, col, currR, currC)
                else:
                    if isGoodMove(app, row, col, currR, currC):
                        selectPiece(app, currR, currC)
                        movePiece(app, row, col, currR, currC)
                    else:
                        unselectPiece(app)
                        clearOutlines(app)
            else:
                pass
    else:
        pass

# Try the move to see if it will break the check
def isGoodMove(app, row, col, currR, currC):
    if isValidMove(app, row, col, currR, currC):
        return tryMove(app, row, col, currR, currC)
    else: return False

def tryMove(app, row, col, currR, currC):
    myPiece=app.pieces[currR][currC]
    otherPiece=app.pieces[row][col]
    # Update the king's location if the player is moving his king
    if myPiece[0]==app.player and myPiece[1]=="king":
        app.kingLoc=(row, col)
    app.pieces[currR][currC]=(None, "empty")
    app.pieces[row][col]=myPiece
    update_killzones(app)
    if isChecked(app):
        result=False
    else:
        result=True
    # Reset the move
    if myPiece[0]==app.player and myPiece[1]=="king":
        app.kingLoc=(currR, currC)
    app.pieces[row][col]=otherPiece
    app.pieces[currR][currC]=myPiece
    update_killzones(app)
    print("Move tried:", currR, currC, row, col, result)
    return result

# Update board outlines for display
def updateOutlines(app, player, currR, currC):
    updateKZOutlines(app, player)
    updateValidMoves(app, currR, currC)

# Clear all board outlines
def clearOutlines(app):
    clearValidMoves(app)
    clearKZOutlines(app)

# Moves the selected chess piece to the destination cell
def makeMove(app, row, col, currR, currC):
    piece=app.pieces[currR][currC]
    # Update the king's location if the player is moving his king
    if piece[0]==app.player and piece[1]=="king":
        app.kingLoc=(row, col)
    app.pieces[currR][currC]=(None, "empty")
    app.pieces[row][col]=piece
    update_killzones(app)
    app.oldLoc=None
    app.makingMove=False

# Make the move based on the piece the user selected 
# and send data to the server
def movePiece(app, row, col, currR, currC):
    if isValidMove(app, row, col, currR, currC):
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        makeMove(app, row, col, currR, currC)
        clearOutlines(app)
    # Clear outlines
    else:
        unselectPiece(app)
        clearOutlines(app)

# Updates outlines for the killzones
def updateKZOutlines(app, player):
    if player==0:
        app.kzOutlines=copy.deepcopy(app.blackKZ)
    elif player==1:
        app.kzOutlines=copy.deepcopy(app.whiteKZ)

# Clears outlines and killzones
def clearKZOutlines(app):
    for row in range(8):
        for col in range(8):
            app.kzOutlines[row][col]=False

def timerFired(app):
    # update_killzones(app)
    try:
    # Tries to get game from server
        app.game=app.n.send("get")
    except:
        print("Couldn't get game")
        pass
    if not app.game.updated[app.player]:
        # Get the move and make the move on local board
        move=app.game.getMove(app.player)
        if move!=():
            (currR, currC, row, col)=move
            selectPiece(app, currR, currC)
            makeMove(app, row, col, currR, currC)
            update_killzones(app)
            # Checks if there is a checkmate
            if checkMate(app):
                app.checkMate=True
                print("CheckMate")
            app.n.send("Updated")
            print("Your Turn")
        else:
            pass

# Returns True if there is a move that breaks the check
# False otherwise
def checkMate(app):
    if app.checkMate: return True
    else:
        if isChecked(app):
            for row in range(8):
                for col in range(8):
                    if app.pieces[row][col][0]==app.player:
                        if checkMovesFromRowCol(app, row, col):
                            return False
            return True
        else:
            return False

# Returns True if there is a move that breaks the check from [currR][currC]
# False otherwise
def checkMovesFromRowCol(app, currR, currC):
    for row in range(8):
        for col in range(8):
            if isGoodMove(app, row, col, currR, currC):
                return True
    return False

# Checks if the player's king is being checked
def isChecked(app):
    (row, col)=app.kingLoc
    if app.player==0:
        if app.blackKZ[row][col]: return True
        else: return False
    elif app.player==1:
        if app.whiteKZ[row][col]: return True
        else: return False

# Selects a cell on the chessboard
def selectCell(app, x, y):
    for row in range(8):
        for col in range(8):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if (x in range(int(x0), int(x1))) and (y in range(int(y0), int(y1))):
                return (row, col)

# Unselect the selected piece
def unselectPiece(app):
    app.oldLoc=None
    app.makingMove=False

# Selects a chess piece if the user clicks on one
def selectPiece(app, row, col):
    if app.pieces[row][col]!=(None, "empty"):
        piece=app.pieces[row][col]
        app.oldLoc=(row, col)
        return piece
    else:
        return None

# Clear valid moves
def clearValidMoves(app):
    for row in range(8):
        for col in range(8):
            app.validMoves[row][col]=False

# Updates valid moves for selected piece in [currR][currC]
def updateValidMoves(app, currR, currC):
    for row in range(8):
        for col in range(8):
            if isValidMove(app, row, col, currR, currC):
                app.validMoves[row][col]=True

# Checks if [row][col] is a valid move from [currR][currC]
def isValidMove(app, row, col, currR, currC):
    color=app.pieces[currR][currC][0]
    piece=app.pieces[currR][currC][1]
    # Checks for friendly piece collision
    if app.pieces[row][col][0]==color: return False
    # Checks valid moves based on piece type
    if piece=="pawn":
        if color==1 and currR==1:
            return isValidStartPawnMove(app, currR, currC, row, col, color)
        elif color==0 and currR==6:
            return isValidStartPawnMove(app, currR, currC, row, col, color)
        else:
            return isValidPawnMove(app, currR, currC, row, col, color)
    elif piece=="castle":
        return isValidCastleMove(app, currR, currC, row, col, color)
    elif piece=="knight":
        return isValidKnightMove(app, currR, currC, row, col, color)
    elif piece=="bishop":
        return isValidBishopMove(app, currR, currC, row, col, color)
    elif piece=="queen":
        return isValidQueenMove(app, currR, currC, row, col, color)
    elif piece=="king":
        return isValidKingMove(app, currR, currC, row, col, color)

# Checks if [row][col] is a valid start pawn move from [currR][currC]
def isValidStartPawnMove(app, currR, currC, row, col, color):
    if color==1:
        # Empty cells move set
        if app.pieces[row][col]==(None, "empty"):
            if (col==currC) and ((currR==row-1)or (currR==row-2)):
                return True
            else: return False
        # Enemy eating movement set
        else:
            if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
                return True
            else: return False
    else:
        # Empty cells move set
        if app.pieces[row][col]==(None, "empty"):
            if (col==currC) and ((currR==row+1)or (currR==row+2)):
                return True
            else: return False
        # Enemy eating movement set
        else:
            if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                return True
            else: return False

# Checks if [row][col] is a valid normal pawn move from [currR][currC]
def isValidPawnMove(app, currR, currC, row, col, color):
    if color==1:
        # Empty cells move set
        if app.pieces[row][col]==(None, "empty"):
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
        if app.pieces[row][col]==(None, "empty"):
            if (col==currC) and (currR==row+1):
                return True
            else: return False
        # Enemy eating movement set
        else:
            if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                return True
            else: return False

# Checks if [row][col] is a valid castle move from [currR][currC]
def isValidCastleMove(app, currR, currC, row, col, color):
    # Not moving is not a valid move
    if row==currR and col==currC: 
        return False
    else:
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
def isValidKnightMove(app, currR, currC, row, col, color):
    # Not moving is not a valid move
    if row==currR and col==currC: return False
    else:
        if (currR+1==row) or (currR-1==row):
            if (currC+2==col) or (currC-2==col):
                return True
        elif (currC+1==col) or (currC-1==col):
            if (currR+2==row) or (currR-2==row):
                return True
        return False

# Checks if [row][col] is a valid bishop move from [currR][currC]
def isValidBishopMove(app, currR, currC, row, col, color):
    # Not moving is not a valid move
    if row==currR and col==currC: 
        return False
    else:
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
def isValidQueenMove(app, currR, currC, row, col, color):
    return (isValidBishopMove(app, currR, currC, row, col, color) or
                    isValidCastleMove(app, currR, currC, row, col, color))

# Checks if [row][col] is a valid king move from [currR][currC]
def isValidKingMove(app, currR, currC, row, col, color):
    # Not moving is not a valid move
    if row==currR and col==currC: return False
    else:
        # Checks if destination is in killzone
        if color==1:
            if app.whiteKZ[row][col] is True:
                return False
        elif color==0:
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
        if app.pieces[row][col]!=(None, "empty"):
            left=i
            break
        i-=1
    i=index+1
    while i<len(diag):
        (row, col)=diag[i]
        if app.pieces[row][col]!=(None, "empty"):
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
        if app.pieces[row][col]!=(None, "empty"):
            left=i
            break
        i-=1
    i=index+1
    while i<len(diag):
        (row, col)=diag[i]
        if app.pieces[row][col]!=(None, "empty"):
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
        if app.pieces[currR][i]!=(None, "empty"):
            rightC=i
            break
        i+=1
    i=currC-1
    while i>=0:
        if app.pieces[currR][i]!=(None, "empty"):
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
        if app.pieces[i][currC]!=(None, "empty"):
            topR=i
            break
        i+=1
    i=currR-1
    while i>=0:
        if app.pieces[i][currC]!=(None, "empty"):
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
            if color==1:
                sprite=app.blackPieces[piece]
            elif color==0:
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