import tkinter, pickle
from cmu_112_graphics import *
from network import Network

#######################################################
# Landing Page #
#######################################################

def landingPage_redrawAll(app, canvas):
    centerX=app.width/2
    btnXSize=200
    btnYSize=100
    btn1Y0=(app.height/2)+100
    btn1X1=centerX-100
    btn1X0=btn1X1-btnXSize
    btn1Y1=btn1Y0+btnYSize
    btn1CenterX=(btn1X0+btn1X1)/2
    btn1CenterY=(btn1Y0+btn1Y1)/2
    btn2X0=centerX+100
    btn2Y0=(app.height/2)+100
    btn2X1=btn2X0+btnXSize
    btn2Y1=btn2Y0+btnYSize
    btn2CenterX=(btn2X0+btn2X1)/2
    btn2CenterY=(btn2Y0+btn2Y1)/2
    canvas.create_text(app.width/2, app.height/2, text='Welcome To Chess!', font='Times 26 bold')
    canvas.create_rectangle(btn1X0, btn1Y0, btn1X1, btn1Y1, fill="white")
    canvas.create_rectangle(btn2X0, btn2Y0, btn2X1, btn2Y1, fill="black")
    canvas.create_text(btn1CenterX, btn1CenterY, text='Play as White', fill='black', font='Times 13')
    canvas.create_text(btn2CenterX, btn2CenterY, text='Play as Black', fill='white', font='Times 13')

def landingPage_mousePressed(app, event):
    x=event.x
    y=event.y
    btnXSize=200
    btnYSize=100
    centerX=app.width/2
    btn1Y0=(app.height/2)+100
    btn1X1=centerX-100
    btn1X0=btn1X1-btnXSize
    btn1Y1=btn1Y0+btnYSize
    btn2X0=centerX+100
    btn2Y0=(app.height/2)+100
    btn2X1=btn2X0+btnXSize
    btn2Y1=btn2Y0+btnYSize
    if (x in range(int(btn1X0), int(btn1X1))) and (y in range(int(btn1Y0), int(btn1Y1))):
        app.player=0
        app.n.connect(app.player)
        app.pieces=init_piece(app)
        app.kingLoc=(7, 4)
        app.mode="wait"
        print("playing as:", app.player)
    elif (x in range(int(btn2X0), int(btn2X1))) and (y in range(int(btn2Y0), int(btn2Y1))):
        app.player=1
        app.n.connect(app.player)
        app.pieces=init_piece(app)
        app.kingLoc=(7, 4)
        app.mode="wait"
        print("playing as:", app.player)
    else:pass

def landingPage_keyPressed(app, event):
    pass

#######################################################
# Rejected Page #
#######################################################

def rejected_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/2, 
                        text='No white player online yet, please try again later', font='Times 26 bold')

def rejected_keyPressed(app, event):
    pass

#######################################################
# Waiting Page #
#######################################################

def wait_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/2, 
            text='Waiting for other player...', font='Times 26 bold')

def wait_timerFired(app):
    try:
    # Tries to get game from server
        app.game=app.n.send("get")
    except:
        app.mode="disconnected"
    if app.game.connected():
        app.mode="gameMode"

#######################################################
# Disconnected Page #
#######################################################

def disconnected_redrawAll(app, canvas):
    font = 'Times 26 bold'
    canvas.create_text(app.width/2, app.height/2, 
                        text='Your Opponent Disconnected', font=font)
    canvas.create_text(app.width/2, (app.height/2)+100, 
                        text='Closing the game now', font=font)

def disconnected_keyPressed(app, event):
    pass

#######################################################
# Victory Page #
#######################################################

def victory_redrawAll(app, canvas):
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    canvas.create_text(app.width/2, 900, text='You won!', font='Times 26 bold')

#######################################################
# Defeat Page #
#######################################################

def defeat_redrawAll(app, canvas):
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    canvas.create_text(app.width/2, 900, text='You lost!', font='Times 26 bold')

#######################################################
# Pawn Promotion Page #
#######################################################

def pawnPromotion_loadPieces(app, canvas):
    y=890
    possiblePieces=["queen", "bishop", "knight", "rook"]
    for index in range(4):
        if app.player==0:
            piece=possiblePieces[index]
            sprite=app.whitePieces[piece]
            x=(app.width/5)*(index+1)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(sprite))
        elif app.player==1:
            piece=possiblePieces[index]
            sprite=app.blackPieces[piece]
            x=(app.width/5)*(index+1)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(sprite))

def pawnPromotion_mousePressed(app, event):
    x=event.x
    y=event.y
    currR=app.promotingPawn[0]
    currC=app.promotingPawn[1]
    row=app.promotingPawn[2]
    col=app.promotingPawn[3]
    queenBtn=((app.width/5)-(app.cellSize/2), ((app.width/5))+(app.cellSize/2), 
                890-(app.cellSize/2), 890+(app.cellSize/2))
    bishopBtn=(((app.width/5)*2)-(app.cellSize/2), ((app.width/5)*2)+(app.cellSize/2), 
                890-(app.cellSize/2), 890+(app.cellSize/2))
    knightBtn=(((app.width/5)*3)-(app.cellSize/2), ((app.width/5)*3)+(app.cellSize/2), 
                890-(app.cellSize/2), 890+(app.cellSize/2))
    rookBtn=(((app.width/5)*4)-(app.cellSize/2), ((app.width/5)*4)+(app.cellSize/2), 
                890-(app.cellSize/2), 890+(app.cellSize/2))
    if x in range(int(queenBtn[0]), int(queenBtn[1])) and y in range(int(queenBtn[2]), int(queenBtn[3])):
        app.pieces[row][col]=(app.player, "queen")
        app.n.send("promotedPawnToQueen")
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        app.promotingPawn=None
        app.mode="gameMode"
    elif x in range(int(bishopBtn[0]), int(bishopBtn[1])) and y in range(int(bishopBtn[2]), int(bishopBtn[3])):
        app.pieces[row][col]=(app.player, "bishop")
        app.n.send("promotedPawnToBishop")
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        app.promotingPawn=None
        app.mode="gameMode"
    elif x in range(int(knightBtn[0]), int(knightBtn[1])) and y in range(int(knightBtn[2]), int(knightBtn[3])):
        app.pieces[row][col]=(app.player, "knight")
        app.n.send("promotedPawnToKnight")
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        app.promotingPawn=None
        app.mode="gameMode"
    elif x in range(int(rookBtn[0]), int(rookBtn[1])) and y in range(int(rookBtn[2]), int(rookBtn[3])):
        app.pieces[row][col]=(app.player, "rook")
        app.n.send("promotedPawnToRook")
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        app.promotingPawn=None
        app.mode="gameMode"

def pawnPromotion_redrawAll(app, canvas):
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    pawnPromotion_loadPieces(app, canvas)
    canvas.create_text(app.width/2, 950, text='Pawn Promotion', font='Times 26 bold')

#######################################################
# Waiting Page #
#######################################################

def waiting_redrawAll(app, canvas):
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    canvas.create_text(app.width/2, 900, text="Waiting for Opponent's Move", font='Times 26 bold')

def waiting_timerFired(app):
    try:
    # Tries to get game from server
        app.game=app.n.send("get")
    except:
        app.mode="disconnected"
    if not app.game.getWent(app.player):
        app.mode="gameMode"

#######################################################
# Game Mode #
#######################################################

def gameMode_mousePressed(app, event):
    x=event.x
    y=event.y
    if not app.game.getWent(app.player) and not app.checkMate:
        cell=selectCell(app, x, y)
        if cell!=None:
            (row, col)=cell
            # If user is not currently making a move
            # Either select a piece or clear moves/outlines
            if app.makingMove is False:
                piece=selectPiece(app, row, col)
                updateKZOutlines(app, app.player)
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
    else:
        pass

def gameMode_timerFired(app):
    try:
    # Tries to get game from server
        app.game=app.n.send("get")
    except:
        app.mode="disconnected"
    if app.game==None: 
        app.mode="rejected"
    else:
        if app.game.over:
            if app.game.winner==app.player:
                app.mode="victory"
            else:
                app.mode="defeat"
        # If local board is not up to date
        elif not app.game.updated[app.player]:
            # Get the move and make the move on local board
            move=app.game.getMove(app.player)
            if move!=():
                print("Other player made a move", move)
                (currR, currC, row, col)=move
                # Mirror the move 
                currR=7-currR
                row=7-row
                piece=selectPiece(app, currR, currC)
                makeMove(app, row, col, currR, currC)
                status=app.game.getCastlingStatus(app.player)
                # Delete the piece if En Passant
                if app.game.getEnPassant(app.player):
                    app.pieces[currR][col]=(None, "empty")
                # If the other player just made a castling move:
                elif status[0]:
                    # Move the rook for right castling
                    if status[1]=="right":
                        rook=app.pieces[row][col+1]
                        app.pieces[row][col-1]=rook
                        app.pieces[row][col+1]=(None, "empty")
                    # Move the rook for left castling
                    elif status[1]=="left":
                        rook=app.pieces[row][col-2]
                        app.pieces[row][col+1]=rook
                        app.pieces[row][col-2]=(None, "empty")
                elif app.game.promotingPawnToQueen:
                    print("promoting pawn to queen")
                    color=app.pieces[row][col][0]
                    app.pieces[row][col]=(color, "queen")
                    app.n.send("resetPawnPromotion")
                elif app.game.promotingPawnToBishop:
                    color=app.pieces[row][col][0]
                    app.pieces[row][col]=(color, "bishop")
                    app.n.send("resetPawnPromotion")
                elif app.game.promotingPawnToKnight:
                    color=app.pieces[row][col][0]
                    app.pieces[row][col]=(color, "knight")
                    app.n.send("resetPawnPromotion")
                elif app.game.promotingPawnToRook:
                    color=app.pieces[row][col][0]
                    app.pieces[row][col]=(color, "rook")
                    app.n.send("resetPawnPromotion")
                app.lastMove=(piece, currR, currC, row, col)
                update_killzones(app)
                # Checks if there is a checkmate
                if checkMate(app):
                    app.checkMate=True
                    app.n.send("Checkmate")
                    app.mode="defeat"
                    print("CheckMate")
                app.n.send("Updated")
                print("Your Turn")
            else:
                pass

def gameMode_redrawAll(app, canvas):
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    if app.game==None: 
        pass
    else:
        if app.game.getWent(app.player):
            canvas.create_text(app.width/2, 900, text="Waiting for Opponent's Move", font='Times 26 bold')
        else:
            canvas.create_text(app.width/2, 900, text="Your Move", font='Times 26 bold')

#######################################################
# # Main App #
#######################################################

def appStarted(app):
    app.n=Network()
    app.player=None
    app.game=None
    app.mode = 'landingPage'
    app.board=[[]for i in range(8)]
    # Initates boolean variable to detect whether a king is being checked
    app.check=False
    app.checkMate=False
    # Initiates variables to check for castling eligibility
    app.rightCastling=True
    app.leftCastling=True
    app.leftRookMoved=False
    app.rightRookMoved=False
    app.kingMoved=False
    # Initiates a variable to store the location of the king
    app.kingLoc=None 
    app.pieces=None
    # Initiates 2D lists to represent killzones
    app.whiteKZ=[[False, False, False, False, 
                False, False, False, False]for i in range(8)]
    app.blackKZ=[[False, False, False, False, 
                False, False, False, False]for i in range(8)]
    app.cellSize=min(app.width, app.height)/8
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
    # Initiates a vairable that keeps track of the latest move by an opponent
    app.lastMove=None
    # Initiates a variable to store the location of the current pawn being promoted
    app.promotingPawn=None

# Original code inspired by https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#loadImageUsingUrl
# Loads chess sprites and stores them in dicts
def init_sprites(app):
    app.chessSprites=app.scaleImage(app.chessSprites, 0.25)
    width, height=app.chessSprites.size
    possiblePieces=["king0", "queen1", "bishop2", "knight3", "rook4", "pawn5"]
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
def init_piece(app):
    Wpieces=[
        [(1, "rook"), (1, "knight"), (1, "bishop"), 
        (1, "queen"), (1, "king"), (1, "bishop"), 
        (1, "knight"), (1, "rook")],
        [(1, "pawn")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(0, "pawn")for i in range(8)], 
        [(0, "rook"), (0, "knight"), (0, "bishop"), 
        (0, "queen"), (0, "king"), (0, "bishop"), 
        (0, "knight"), (0, "rook")]
        ]
    Bpieces=[
        [(0, "rook"), (0, "knight"), (0, "bishop"), 
        (0, "queen"), (0, "king"), (0, "bishop"), 
        (0, "knight"), (0, "rook")],
        [(0, "pawn")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(None, "empty")for i in range(8)], 
        [(1, "pawn")for i in range(8)], 
        [(1, "rook"), (1, "knight"), (1, "bishop"), 
        (1, "queen"), (1, "king"), (1, "bishop"), 
        (1, "knight"), (1, "rook")]
        ]
    if app.player==0:
        return Wpieces
    elif app.player==1:
        return Bpieces

# Updates killzones based on piece positions
def update_killzones(app):
    for row in range(8):
        for col in range(8):
            elem=app.pieces[row][col]
            color=elem[0]
            piece=elem[1]
            # Gets all possible threat origins for white side
            (BpawnSet, BrookSet, BknightSet, 
            BbishopSet, BqueenSet, BkingSet)=blackMoves(app, row, col)
            # Gets all possible threat origins for black side
            (WpawnSet, WrookSet, WknightSet, 
            WbishopSet, WqueenSet, WkingSet)=whiteMoves(app, row, col)
            # Updates killzone accordingly
            update_blackKZ(app, BpawnSet, BrookSet, BknightSet, 
            BbishopSet, BqueenSet, BkingSet, row, col)
            update_whiteKZ(app, WpawnSet, WrookSet, WknightSet, 
            WbishopSet, WqueenSet, WkingSet, row, col)

# returns black moves from [currR][currC]
def blackMoves(app, currR, currC):
    pawnSet=[]
    rookSet=[]
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
                if isValidRookMove(app, currR, currC, row, col, 1):
                    rookSet.append((row, col))
                if isValidKnightMove(app, currR, currC, row, col, 1):
                    knightSet.append((row, col))
                if isValidBishopMove(app, currR, currC, row, col, 1):
                    bishopSet.append((row, col))
                if isValidQueenMove(app, currR, currC, row, col, 1):
                    queenSet.append((row, col))
                if isValidKingBackTrack(app, currR, currC, row, col, 1):
                    kingSet.append((row, col))
    return pawnSet, rookSet, knightSet, bishopSet, queenSet, kingSet

# returns white moves from [currR][currC]
def whiteMoves(app, currR, currC):
    pawnSet=[]
    rookSet=[]
    knightSet=[]
    bishopSet=[]
    queenSet=[]
    kingSet=[]
    for row in range(8):
        for col in range(8):
            if isValidPawnBackTrack(app, currR, currC, row, col, 0):
                pawnSet.append((row, col))
            if isValidRookMove(app, currR, currC, row, col, 0):
                rookSet.append((row, col))
            if isValidKnightMove(app, currR, currC, row, col, 0):
                knightSet.append((row, col))
            if isValidBishopMove(app, currR, currC, row, col, 0):
                bishopSet.append((row, col))
            if isValidQueenMove(app, currR, currC, row, col, 0):
                queenSet.append((row, col))
            if isValidKingBackTrack(app, currR, currC, row, col, 0):
                kingSet.append((row, col))
    return pawnSet, rookSet, knightSet, bishopSet, queenSet, kingSet

# Updates killzones for black pieces
def update_blackKZ(app, pawnSet, rookSet, knightSet, 
                bishopSet, queenSet, kingSet, currR, currC):
    for coord in pawnSet:
        (row, col)=coord
        if app.pieces[row][col]==(1, "pawn"):
            app.blackKZ[currR][currC]=True
            return 
    for coord in rookSet:
        (row, col)=coord
        if app.pieces[row][col]==(1, "rook"):
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
def update_whiteKZ(app, pawnSet, rookSet, knightSet, 
                bishopSet, queenSet, kingSet, currR, currC):
    for coord in pawnSet:
        (row, col)=coord
        if app.pieces[row][col]==(0, "pawn"):
            app.whiteKZ[currR][currC]=True
            return
    for coord in rookSet:
        (row, col)=coord
        if app.pieces[row][col]==(0, "rook"):
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

# Updates castling eligibility
def updateCastlingEligibility(app):
    if app.kingMoved:
        app.rightCastling=False
        app.leftCastling=False
    elif app.leftRookMoved:
        app.leftCastling=False
    elif app.rightRookMoved:
        app.rightCastling=False

# Backtrack pawn check for killzone updates
def isValidPawnBackTrack(app, currR, currC, row, col, color):
    if color!=app.player:
        if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                return True
        else: return False
    elif color==app.player:
        if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
            return True
        else: return False

# Try the move to see if it will break the check
def isGoodMove(app, row, col, currR, currC):
    if isValidMove(app, row, col, currR, currC):
        return tryMove(app, row, col, currR, currC)
    else: return False

# Tries the move from [currR][currC] to [row][col]
# returns true if the move breaks the check
# False otherwise
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
        app.kingMoved=True
    elif piece[0]==app.player and piece[1]=="rook" and piece[0]==0:
        if currC==0:
            app.leftRookMoved=True
        elif currC==7:
            app.rightRookMoved=True
    elif piece[0]==app.player and piece[1]=="rook" and piece[0]==1:
        if currC==0:
            app.rightRookMoved=True
        elif currC==7:
            app.leftRookMoved=True
    app.pieces[currR][currC]=(None, "empty")
    app.pieces[row][col]=piece
    update_killzones(app)
    updateCastlingEligibility(app)
    app.oldLoc=None
    app.makingMove=False

# Make the move based on the piece the user selected 
# and send data to the server
def movePiece(app, row, col, currR, currC):
    if isValidMove(app, row, col, currR, currC):
        # Checks if the move just made enables the player to promote a pawn
        if ((app.pieces[currR][currC][1]=="pawn") and
            (row==0)):
            app.mode="pawnPromotion"
            app.promotingPawn=(currR, currC, row, col)
            app.n.send("resetSpecialMoves")
            makeMove(app, row, col, currR, currC)
            clearOutlines(app)
        else:
            app.n.send((currR, currC, row, col))
            app.n.send("setWent")
            app.updated=False
            # En Passant
            if ((app.pieces[currR][currC][1]=="pawn") and 
                (col!=currC) and 
                (app.pieces[row][col][0]==None)):
                # Kill the piece during an En Passant
                app.pieces[currR][col]=(None, "empty")
                print("EnPassant at:", currR, currC, row, col)
                app.n.send("EnPassant")
            elif app.pieces[currR][currC][1]=="king":
                # Moves the rook in right castling
                if (row==currR) and (col==currC+2):
                    rook=app.pieces[row][col+1]
                    app.pieces[row][col-1]=rook
                    app.pieces[row][col+1]=(None, "empty")
                    app.n.send("RightCastling")
                # Moves the rook in left castling
                elif (row==currR) and (col==currC-2):
                    rook=app.pieces[row][col-2]
                    app.pieces[row][col+1]=rook
                    app.pieces[row][col-2]=(None, "empty")
                    app.n.send("LeftCastling")
            else:
                app.n.send("resetSpecialMoves")
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
    return None

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
        if currR==6:
            return isValidStartPawnMove(app, currR, currC, row, col, color)
        else:
            return isValidPawnMove(app, currR, currC, row, col, color)
    elif piece=="rook":
        return isValidRookMove(app, currR, currC, row, col, color)
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
    # Empty cells move set
    if app.pieces[row][col]==(None, "empty"):
        if (col==currC) and (currR==row+1):
            return True
        else: 
            # En Passant
            if app.lastMove!=None:
                (elem, originR, originC, dRow, dCol)=app.lastMove
                c=elem[0]
                piece=elem[1]
                if ((currR==3) and (color!=c) and (piece=="pawn") and 
                    (originR==1) and (dRow==3) and ((originC==currC+1) or (originC==currC-1))):
                    if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                        return True
                    else: return False
                else:return False
            else: return False
    # Enemy eating movement set
    else:
        if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
            return True
        else: return False

# Checks if [row][col] is a valid rook move from [currR][currC]
def isValidRookMove(app, currR, currC, row, col, color):
    # Not moving is not a valid move
    if row==currR and col==currC: 
        return False
    else:
        # Gets the furthest possible column positions
        leftC, rightC=nearestPieceOnRow(app, currR, currC)
        # Gets the furthest possible row positions
        topR, botR=nearestPieceOncol(app, currR, currC)
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
                    isValidRookMove(app, currR, currC, row, col, color))

# Backtracking king used to update killzones
# Exclude castling move
def isValidKingBackTrack(app, currR, currC, row, col, color):
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
        else: 
            return False

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
        # Castling Moves
        elif (currR==row) and (currC+2==col):
            if color==0: 
                return isValidRightWhiteCastling(app, currR, currC, row, col)
            elif color==1:
                return isValidRightBlackCastling(app, currR, currC, row, col)
        elif (currR==row) and (col==currC-2):
            if color==0: 
                return isValidLeftWhiteCastling(app, currR, currC, row, col)
            elif color==1:
                return isValidLeftBlackCastling(app, currR, currC, row, col)
        else: 
            return False

# Checks if move from [currR][currC] to [row][col] is 
# a valid right white castling move
def isValidRightWhiteCastling(app, currR, currC, row, col):
    if (app.rightCastling and 
        (not isChecked(app)) and 
        (app.pieces[row][col]==(None, "empty")) and 
        (app.pieces[row][col-1]==(None, "empty")) and 
        (not app.blackKZ[row][col]) and 
        (not app.blackKZ[row][col-1])):
        return True
    else: return False

# Checks if move from [currR][currC] to [row][col] is 
# a valid left white castling move
def isValidLeftWhiteCastling(app, currR, currC, row, col):
    if (app.leftCastling and 
        (not isChecked(app)) and
        (app.pieces[row][col]==(None, "empty")) and 
        (app.pieces[row][col-1]==(None, "empty")) and 
        (app.pieces[row][col+1]==(None, "empty")) and 
        (not app.blackKZ[row][col]) and 
        (not app.blackKZ[row][col+1])):
        return True
    else: return False

# Checks if move from [currR][currC] to [row][col] is 
# a valid right black castling move
def isValidRightBlackCastling(app, currR, currC, row, col):
    if (app.rightCastling and 
        (not isChecked(app)) and 
        (app.pieces[row][col]==(None, "empty")) and 
        (app.pieces[row][col-1]==(None, "empty")) and 
        (not app.whiteKZ[row][col]) and 
        (not app.whiteKZ[row][col-1])):
        return True
    else: return False

# Checks if move from [currR][currC] to [row][col] is 
# a valid left black castling move
def isValidLeftBlackCastling(app, currR, currC, row, col):
    if (app.leftCastling and 
        (not isChecked(app)) and
        (app.pieces[row][col]==(None, "empty")) and 
        (app.pieces[row][col-1]==(None, "empty")) and 
        (app.pieces[row][col+1]==(None, "empty")) and 
        (not app.whiteKZ[row][col]) and 
        (not app.whiteKZ[row][col+1])):
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
def nearestPieceOncol(app, currR, currC):
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

def chessAnimation():
    runApp(width=800, height=1000)

if __name__=="__main__":
    chessAnimation()