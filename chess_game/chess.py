"""Local Chess Client"""

import tkinter, pickle, random, time, os
from cmu_112_graphics import *
from network import Network
from _thread import *

#######################################################
# Landing Page #
#######################################################

def landingPage_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/18)
    fontSize2=int(min(app.height, app.width)/37)
    if app.connecting:
        canvas.create_text(app.width/2, app.height/2, 
                        text='Connecting to server...', font=f'Times {fontSize1} bold')
    else:
        centerX=app.width/2
        btnXSize=int(app.width/3.2)
        btnYSize=int(app.width/12)
        AIBtn=(centerX-(app.width//9.6)-btnXSize, (app.height/2)+(app.height//6), 
                centerX-(app.width//9.6), (app.height/2)+(app.height//6)+btnYSize)
        MultBtn=(centerX+(app.width//9.6), (app.height/2)+(app.height//6), 
                centerX+(app.width//9.6)+btnXSize, (app.height/2)+(app.height//6)+btnYSize)
        AIBtnCenter=((AIBtn[0]+AIBtn[2])/2, (AIBtn[1]+AIBtn[3])/2)
        MultBtnCenter=((MultBtn[0]+MultBtn[2])/2, (MultBtn[1]+MultBtn[3])/2)
        canvas.create_text(app.width/2, app.height/2, text='Welcome To Chess!', font=f'Times {fontSize1} bold')
        canvas.create_rectangle(AIBtn[0], AIBtn[1], AIBtn[2], AIBtn[3], fill="alice blue")
        canvas.create_rectangle(MultBtn[0], MultBtn[1], MultBtn[2], MultBtn[3], fill="white")
        canvas.create_text(AIBtnCenter[0], AIBtnCenter[1], text='Play against AI', fill='black', font=f'Times {fontSize2}')
        canvas.create_text(MultBtnCenter[0], MultBtnCenter[1], text='Play Multiplayer', fill='black', font=f'Times {fontSize2}')

def landingPage_mousePressed(app, event):
    x=event.x
    y=event.y
    centerX=app.width/2
    btnXSize=int(app.width/3.2)
    btnYSize=int(app.width/12)
    AIBtn=(centerX-(app.width//9.6)-btnXSize, (app.height/2)+(app.height//6), 
            centerX-(app.width//9.6), (app.height/2)+(app.height//6)+btnYSize)
    MultBtn=(centerX+(app.width//9.6), (app.height/2)+(app.height//6), 
            centerX+(app.width//9.6)+btnXSize, (app.height/2)+(app.height//6)+btnYSize)
    if (x in range(int(AIBtn[0]), int(AIBtn[2]))) and (y in range(int(AIBtn[1]), int(AIBtn[3]))):
        app.mode="single"
    elif (x in range(int(MultBtn[0]), int(MultBtn[2]))) and (y in range(int(MultBtn[1]), int(MultBtn[3]))):
        app.mode="multi"
    else:pass

#######################################################
# Multiplayer Page #
#######################################################

def multi_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/18)
    fontSize2=int(min(app.height, app.width)/37)
    if app.connecting:
        canvas.create_text(app.width/2, app.height/2, 
                        text='Connecting to server...', font='Times 26 bold')
    else:
        centerX=app.width/2
        btnXSize=int(app.width/3.2)
        btnYSize=int(app.width/12)
        whiteBtn=(centerX-(app.width//9.6)-btnXSize, (app.height/2)+(app.height//6), 
                centerX-(app.width//9.6), (app.height/2)+(app.height//6)+btnYSize)
        blackBtn=(centerX+(app.width//9.6), (app.height/2)+(app.height//6), 
                centerX+(app.width//9.6)+btnXSize, (app.height/2)+(app.height//6)+btnYSize)
        backBtn=(centerX-(btnXSize/2), (app.height/2)+(app.height//4), 
            centerX+(btnXSize/2), (app.height/2)+(app.height//4)+btnYSize)
        whiteBtnCenter=((whiteBtn[0]+whiteBtn[2])/2, (whiteBtn[1]+whiteBtn[3])/2)
        blackBtnCenter=((blackBtn[0]+blackBtn[2])/2, (blackBtn[1]+blackBtn[3])/2)
        backBtnCenter=((backBtn[0]+backBtn[2])/2, (backBtn[1]+backBtn[3])/2)
        canvas.create_text(app.width/2, (app.height/2)-(app.height//3), text='Multiplayer Mode', font=f'Times {fontSize1} bold')
        canvas.create_text(app.width/2, (app.height/2)-(app.height//6), text='Please choose your side', font=f'Times {fontSize1} bold')
        canvas.create_rectangle(whiteBtn[0], whiteBtn[1], whiteBtn[2], whiteBtn[3], fill="white")
        canvas.create_rectangle(blackBtn[0], blackBtn[1], blackBtn[2], blackBtn[3], fill="black")
        canvas.create_rectangle(backBtn[0], backBtn[1], backBtn[2], backBtn[3], fill="light blue")
        canvas.create_text(whiteBtnCenter[0], whiteBtnCenter[1], text='Play as White', fill='black', font=f'Times {fontSize2}')
        canvas.create_text(blackBtnCenter[0], blackBtnCenter[1], text='Play as Black', fill='white', font=f'Times {fontSize2}')
        canvas.create_text(backBtnCenter[0], backBtnCenter[1], text='Return', fill='white', font=f'Times {fontSize2}')

def multi_mousePressed(app, event):
    x=event.x
    y=event.y
    centerX=app.width/2
    btnXSize=int(app.width/3.2)
    btnYSize=int(app.width/12)
    whiteBtn=(centerX-(app.width//9.6)-btnXSize, (app.height/2)+(app.height//6), 
            centerX-(app.width//9.6), (app.height/2)+(app.height//6)+btnYSize)
    blackBtn=(centerX+(app.width//9.6), (app.height/2)+(app.height//6), 
            centerX+(app.width//9.6)+btnXSize, (app.height/2)+(app.height//6)+btnYSize)
    backBtn=(centerX-(btnXSize/2), (app.height/2)+(app.height//4), 
        centerX+(btnXSize/2), (app.height/2)+(app.height//4)+btnYSize)
    if (x in range(int(whiteBtn[0]), int(whiteBtn[2]))) and (y in range(int(whiteBtn[1]), int(whiteBtn[3]))):
        app.connecting=True
        app.player=0
        # Try to connect the player
        status=app.n.connect(app.player)
        if status==False:
            app.mode="failed"
        else:
            app.pieces=init_piece(app)
            app.kingLoc=[(7, 4), (0, 4)]
            app.mode="wait"
    elif (x in range(int(blackBtn[0]), int(blackBtn[2]))) and (y in range(int(blackBtn[1]), int(blackBtn[3]))):
        app.player=1
        app.connecting=True
        # Try to connect the player
        status=app.n.connect(app.player)
        if status==False:
            app.mode="failed"
        else:
            app.pieces=init_piece(app)
            app.kingLoc=[(0, 4), (7, 4)]
            app.mode="wait"
    elif (x in range(int(backBtn[0]), int(backBtn[2]))) and (y in range(int(backBtn[1]), int(backBtn[3]))):
        app.mode="landingPage"
    else:pass

#######################################################
# Single player Page #
#######################################################

def single_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/18)
    fontSize2=int(min(app.height, app.width)/37)
    centerX=app.width/2
    btnXSize=int(app.width/3.2)
    btnYSize=int(app.width/12)
    whiteBtn=(centerX-(app.width//9.6)-btnXSize, (app.height/2)+(app.height//6), 
            centerX-(app.width//9.6), (app.height/2)+(app.height//6)+btnYSize)
    blackBtn=(centerX+(app.width//9.6), (app.height/2)+(app.height//6), 
            centerX+(app.width//9.6)+btnXSize, (app.height/2)+(app.height//6)+btnYSize)
    backBtn=(centerX-(btnXSize/2), (app.height/2)+(app.height//4), 
        centerX+(btnXSize/2), (app.height/2)+(app.height//4)+btnYSize)
    whiteBtnCenter=((whiteBtn[0]+whiteBtn[2])/2, (whiteBtn[1]+whiteBtn[3])/2)
    blackBtnCenter=((blackBtn[0]+blackBtn[2])/2, (blackBtn[1]+blackBtn[3])/2)
    backBtnCenter=((backBtn[0]+backBtn[2])/2, (backBtn[1]+backBtn[3])/2)
    canvas.create_text(app.width/2, (app.height/2)-(app.height//3), text='Singleplayer Mode', font=f'Times {fontSize1} bold')
    canvas.create_text(app.width/2, (app.height/2)-(app.height//6), text='Please choose your side', font=f'Times {fontSize1} bold')
    canvas.create_rectangle(whiteBtn[0], whiteBtn[1], whiteBtn[2], whiteBtn[3], fill="white")
    canvas.create_rectangle(blackBtn[0], blackBtn[1], blackBtn[2], blackBtn[3], fill="black")
    canvas.create_rectangle(backBtn[0], backBtn[1], backBtn[2], backBtn[3], fill="light blue")
    canvas.create_text(whiteBtnCenter[0], whiteBtnCenter[1], text='Play as White', fill='black', font=f'Times {fontSize2}')
    canvas.create_text(blackBtnCenter[0], blackBtnCenter[1], text='Play as Black', fill='white', font=f'Times {fontSize2}')
    canvas.create_text(backBtnCenter[0], backBtnCenter[1], text='Return', fill='white', font=f'Times {fontSize2}')

def single_mousePressed(app, event):
    x=event.x
    y=event.y
    centerX=app.width/2
    btnXSize=int(app.width/3.2)
    btnYSize=int(app.width/12)
    whiteBtn=(centerX-(app.width//9.6)-btnXSize, (app.height/2)+(app.height//6), 
            centerX-(app.width//9.6), (app.height/2)+(app.height//6)+btnYSize)
    blackBtn=(centerX+(app.width//9.6), (app.height/2)+(app.height//6), 
            centerX+(app.width//9.6)+btnXSize, (app.height/2)+(app.height//6)+btnYSize)
    backBtn=(centerX-(btnXSize/2), (app.height/2)+(app.height//4), 
        centerX+(btnXSize/2), (app.height/2)+(app.height//4)+btnYSize)
    if (x in range(int(whiteBtn[0]), int(whiteBtn[2]))) and (y in range(int(whiteBtn[1]), int(whiteBtn[3]))):
        app.player=0
        app.AIPlayer=1
        app.pieces=init_piece(app)
        app.kingLoc=[(7, 4), (0, 4)]
        app.mode="localMode"
    elif (x in range(int(blackBtn[0]), int(blackBtn[2]))) and (y in range(int(blackBtn[1]), int(blackBtn[3]))):
        app.AIPlayer=0
        app.player=1
        app.pieces=init_piece(app)
        app.kingLoc=[(0, 4), (7, 4)]
        app.mode="localMode"
    elif (x in range(int(backBtn[0]), int(backBtn[2]))) and (y in range(int(backBtn[1]), int(backBtn[3]))):
        app.mode="landingPage"
    else:pass

#######################################################
# Failed Page #
#######################################################

def failed_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/18)
    fontSize2=int(min(app.height, app.width)/27)
    centerX=app.width/2
    btnXSize=app.width//4.8
    btnYSize=app.height//12
    quitBtn=(centerX-(btnXSize/2), (app.height/2)+(app.height//4), 
            centerX+(btnXSize/2), (app.height/2)+(app.height//4)+btnYSize)
    quitBtnCenter=((quitBtn[0]+quitBtn[2])/2, (quitBtn[1]+quitBtn[3])/2)
    canvas.create_text(app.width/2, (app.height/2)-(app.height//4), 
                        text='Failed to connect to server', font=f'Times {fontSize1} bold')
    canvas.create_text(app.width/2, (app.height/2)-(app.height//12), 
                        text='Check server status/IP Address/Port settings', font=f'Times {fontSize2} bold')
    canvas.create_rectangle(quitBtn[0], quitBtn[1], quitBtn[2], quitBtn[3], fill="light blue")
    canvas.create_text(quitBtnCenter[0], quitBtnCenter[1], 
                        text='Quit', font=f'Times {fontSize2}')
    
def failed_mousePressed(app, event):
    x=event.x
    y=event.y
    centerX=app.width/2
    btnXSize=app.width//4.8
    btnYSize=app.height//12
    quitBtn=(centerX-(btnXSize/2), (app.height/2)+(app.height//4), 
            centerX+(btnXSize/2), (app.height/2)+(app.height//4)+btnYSize)
    if ((x in range(int(quitBtn[0]), int(quitBtn[2]))) and 
        (y in range(int(quitBtn[1]), int(quitBtn[3])))):
        exit()

#######################################################
# Waiting Page #
#######################################################

def wait_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/18)
    canvas.create_text(app.width/2, app.height/2, 
            text='Waiting for other player...', font=f'Times {fontSize1} bold')

def wait_timerFired(app):
    try:
    # Tries to get game from server
        app.game=app.n.send("get")
    except:
        app.mode="disconnected"
    if app.game.connected():
        app.mode="onlineMode"

#######################################################
# Disconnected Page #
#######################################################

def disconnected_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/18)
    fontSize2=int(min(app.height, app.width)/27)
    centerX=app.width/2
    btnXSize=app.width//4.8
    btnYSize=app.height//12
    quitBtn=(centerX-(btnXSize/2), (app.height/2)+(app.height//4), 
            centerX+(btnXSize/2), (app.height/2)+(app.height//4)+btnYSize)
    quitBtnCenter=((quitBtn[0]+quitBtn[2])/2, (quitBtn[1]+quitBtn[3])/2)
    canvas.create_text(app.width/2, (app.height/2)-(app.height//4), 
                        text='Your Opponent Disconnected', font=f'Times {fontSize1} bold')
    canvas.create_text(app.width/2, (app.height/2)-(app.height//12), 
                        text='Closing the game now', font=f'Times {fontSize1} bold')
    canvas.create_rectangle(quitBtn[0], quitBtn[1], quitBtn[2], quitBtn[3], fill="light blue")
    canvas.create_text(quitBtnCenter[0], quitBtnCenter[1], 
                        text='Quit', font=f'Times {fontSize2}')

def disconnected_mousePressed(app, event):
    x=event.x
    y=event.y
    centerX=app.width/2
    btnXSize=app.width//4.8
    btnYSize=app.height//12
    quitBtn=(centerX-(btnXSize/2), (app.height/2)+(app.height//4), 
            centerX+(btnXSize/2), (app.height/2)+(app.height//4)+btnYSize)
    if ((x in range(int(quitBtn[0]), int(quitBtn[2]))) and 
        (y in range(int(quitBtn[1]), int(quitBtn[3])))):
        exit()

#######################################################
# Victory Page #
#######################################################

def victory_redrawAll(app, canvas):
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    fontSize1=int(min(app.height, app.width)/18)
    fontSize2=int(min(app.height, app.width)/24)
    canvas.create_text(app.width/2, app.height-(app.height/7.5), text='You won!', font=f'Times {fontSize1} bold')
    quitBtn=((app.width/2)-(app.width/4.8), (app.height-(app.height/12)), 
            (app.width/2)+(app.width/4.8), (app.height-(app.height/30)))
    quitBtnCenter=((quitBtn[0]+quitBtn[2])/2, (quitBtn[1]+quitBtn[3])/2)
    canvas.create_rectangle(quitBtn[0], quitBtn[1], quitBtn[2], quitBtn[3], fill="light blue")
    canvas.create_text(quitBtnCenter[0], quitBtnCenter[1], text='Quit', font=f'Times {fontSize2}')

def victory_mousePressed(app, event):
    quitBtn=((app.width/2)-(app.width/4.8), (app.height-(app.height/12)), 
            (app.width/2)+(app.width/4.8), (app.height-(app.height/30)))
    x=event.x
    y=event.y
    if ((x in range(int(quitBtn[0]), int(quitBtn[2]))) and
        y in range(int(quitBtn[1]), int(quitBtn[3]))):
        exit()

def victory_timerFired(app):
    app.cellSize=min(app.width, (app.height/6)*4.8)/8
    scale=app.cellSize/90
    sprites=app.loadImage(os.path.join(sys.path[0], "chessSprites.png"))
    app.chessSprites=app.scaleImage(sprites, scale)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict() 
    init_sprites(app)

#######################################################
# Defeat Page #
#######################################################

def defeat_redrawAll(app, canvas):
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    fontSize1=int(min(app.height, app.width)/18)
    fontSize2=int(min(app.height, app.width)/24)
    canvas.create_text(app.width/2, app.height-(app.height/7.5), text='You lost!', font=f'Times {fontSize1} bold')
    quitBtn=((app.width/2)-(app.width/4.8), (app.height-(app.height/12)), 
            (app.width/2)+(app.width/4.8), (app.height-(app.height/30)))
    quitBtnCenter=((quitBtn[0]+quitBtn[2])/2, (quitBtn[1]+quitBtn[3])/2)
    canvas.create_rectangle(quitBtn[0], quitBtn[1], quitBtn[2], quitBtn[3], fill="light blue")
    canvas.create_text(quitBtnCenter[0], quitBtnCenter[1], text='Quit', font=f'Times {fontSize2}')

def defeat_mousePressed(app, event):
    quitBtn=((app.width/2)-(app.width/4.8), (app.height-(app.height/12)), 
            (app.width/2)+(app.width/4.8), (app.height-(app.height/30)))
    x=event.x
    y=event.y
    if ((x in range(int(quitBtn[0]), int(quitBtn[2]))) and
        y in range(int(quitBtn[1]), int(quitBtn[3]))):
        exit()

def defeat_timerFired(app):
    app.cellSize=min(app.width, (app.height/6)*4.8)/8
    scale=app.cellSize/90
    sprites=app.loadImage(os.path.join(sys.path[0], "chessSprites.png"))
    app.chessSprites=app.scaleImage(sprites, scale)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict() 
    init_sprites(app)

#######################################################
# Multiplayer Pawn Promotion Page #
#######################################################

def onlinePawnPromotion_loadPieces(app, canvas):
    y=app.height-(app.height//7.5)
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

def onlinePawnPromotion_mousePressed(app, event):
    x=event.x
    y=event.y
    center=app.height-(app.height//7.5)
    currR=app.promotingPawn[0]
    currC=app.promotingPawn[1]
    row=app.promotingPawn[2]
    col=app.promotingPawn[3]
    queenBtn=((app.width/5)-(app.cellSize/2), ((app.width/5))+(app.cellSize/2), 
                center-(app.cellSize/2), center+(app.cellSize/2))
    bishopBtn=(((app.width/5)*2)-(app.cellSize/2), ((app.width/5)*2)+(app.cellSize/2), 
                center-(app.cellSize/2), center+(app.cellSize/2))
    knightBtn=(((app.width/5)*3)-(app.cellSize/2), ((app.width/5)*3)+(app.cellSize/2), 
                center-(app.cellSize/2), center+(app.cellSize/2))
    rookBtn=(((app.width/5)*4)-(app.cellSize/2), ((app.width/5)*4)+(app.cellSize/2), 
                center-(app.cellSize/2), center+(app.cellSize/2))
    if x in range(int(queenBtn[0]), int(queenBtn[1])) and y in range(int(queenBtn[2]), int(queenBtn[3])):
        app.pieces[row][col]=(app.player, "queen")
        app.n.send("promotedPawnToQueen")
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        app.promotingPawn=None
        app.mode="onlineMode"
    elif x in range(int(bishopBtn[0]), int(bishopBtn[1])) and y in range(int(bishopBtn[2]), int(bishopBtn[3])):
        app.pieces[row][col]=(app.player, "bishop")
        app.n.send("promotedPawnToBishop")
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        app.promotingPawn=None
        app.mode="onlineMode"
    elif x in range(int(knightBtn[0]), int(knightBtn[1])) and y in range(int(knightBtn[2]), int(knightBtn[3])):
        app.pieces[row][col]=(app.player, "knight")
        app.n.send("promotedPawnToKnight")
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        app.promotingPawn=None
        app.mode="onlineMode"
    elif x in range(int(rookBtn[0]), int(rookBtn[1])) and y in range(int(rookBtn[2]), int(rookBtn[3])):
        app.pieces[row][col]=(app.player, "rook")
        app.n.send("promotedPawnToRook")
        app.n.send((currR, currC, row, col))
        app.n.send("setWent")
        app.updated=False
        app.promotingPawn=None
        app.mode="onlineMode"

def onlinePawnPromotion_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/27)
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    onlinePawnPromotion_loadPieces(app, canvas)
    canvas.create_text(app.width/2, app.height-(app.height//20), text='Pawn Promotion', font=f'Times {fontSize1} bold')

def onlinePawnPromotion_timerFired(app):
    app.cellSize=min(app.width, (app.height/6)*4.8)/8
    scale=app.cellSize/90
    sprites=app.loadImage(os.path.join(sys.path[0], "chessSprites.png"))
    app.chessSprites=app.scaleImage(sprites, scale)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict() 
    init_sprites(app)

#######################################################
# Singleplayer Pawn Promotion Page #
#######################################################

def localPawnPromotion_loadPieces(app, canvas):
    y=app.height-(app.height//7.5)
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

def localPawnPromotion_mousePressed(app, event):
    x=event.x
    y=event.y
    center=app.height-(app.height//7.5)
    currR=app.promotingPawn[0]
    currC=app.promotingPawn[1]
    row=app.promotingPawn[2]
    col=app.promotingPawn[3]
    queenBtn=((app.width/5)-(app.cellSize/2), ((app.width/5))+(app.cellSize/2), 
                center-(app.cellSize/2), center+(app.cellSize/2))
    bishopBtn=(((app.width/5)*2)-(app.cellSize/2), ((app.width/5)*2)+(app.cellSize/2), 
                center-(app.cellSize/2), center+(app.cellSize/2))
    knightBtn=(((app.width/5)*3)-(app.cellSize/2), ((app.width/5)*3)+(app.cellSize/2), 
                center-(app.cellSize/2), center+(app.cellSize/2))
    rookBtn=(((app.width/5)*4)-(app.cellSize/2), ((app.width/5)*4)+(app.cellSize/2), 
                center-(app.cellSize/2), center+(app.cellSize/2))
    if x in range(int(queenBtn[0]), int(queenBtn[1])) and y in range(int(queenBtn[2]), int(queenBtn[3])):
        app.pieces[row][col]=(app.player, "queen")
        print("Pawn promoted")
        app.lastMove=(app.pieces[row][col], currR, currC, row, col)
        app.localWent=app.player
        app.updated=False
        app.promotingPawn=None
        update_killzones(app)
        app.mode="localMode"
    elif x in range(int(bishopBtn[0]), int(bishopBtn[1])) and y in range(int(bishopBtn[2]), int(bishopBtn[3])):
        app.pieces[row][col]=(app.player, "bishop")
        app.lastMove=(app.pieces[row][col], currR, currC, row, col)
        app.localWent=app.player
        app.updated=False
        app.promotingPawn=None
        update_killzones(app)
        app.mode="localMode"
    elif x in range(int(knightBtn[0]), int(knightBtn[1])) and y in range(int(knightBtn[2]), int(knightBtn[3])):
        app.pieces[row][col]=(app.player, "knight")
        app.lastMove=(app.pieces[row][col], currR, currC, row, col)
        app.localWent=app.player
        app.updated=False
        app.promotingPawn=None
        update_killzones(app)
        app.mode="localMode"
    elif x in range(int(rookBtn[0]), int(rookBtn[1])) and y in range(int(rookBtn[2]), int(rookBtn[3])):
        app.pieces[row][col]=(app.player, "rook")
        app.lastMove=(app.pieces[row][col], currR, currC, row, col)
        app.localWent=app.player
        app.updated=False
        app.promotingPawn=None
        update_killzones(app)
        app.mode="localMode"

def localPawnPromotion_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/27)
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    localPawnPromotion_loadPieces(app, canvas)
    canvas.create_text(app.width/2, app.height-(app.height//20), text='Pawn Promotion', font=f'Times {fontSize1} bold')

def localPawnPromotion_timerFired(app):
    app.cellSize=min(app.width, (app.height/6)*4.8)/8
    scale=app.cellSize/90
    sprites=app.loadImage(os.path.join(sys.path[0], "chessSprites.png"))
    app.chessSprites=app.scaleImage(sprites, scale)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict() 
    init_sprites(app)

#######################################################
# Waiting Page #
#######################################################

def waiting_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/27)
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    canvas.create_text(app.width/2, app.height-(app.height//12), text="Waiting for Opponent's Move", font=f'Times {fontSize1} bold')

def waiting_timerFired(app):
    app.cellSize=min(app.width, (app.height/6)*4.8)/8
    scale=app.cellSize/90
    sprites=app.loadImage(os.path.join(sys.path[0], "chessSprites.png"))
    app.chessSprites=app.scaleImage(sprites, scale)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict() 
    init_sprites(app)
    try:
    # Tries to get game from server
        app.game=app.n.send("get")
    except:
        app.mode="disconnected"
    if not app.game.getWent(app.player):
        app.mode="onlineMode"

#######################################################
# Singleplayer Game Mode #
#######################################################

def localMode_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/48)
    fontSize2=int(min(app.height, app.width)/27)
    fontSize3=int(min(app.height, app.width)/40)
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    easyBtn=((app.width/2)-(app.width//4.8), (app.height-(app.height//7.5)), 
            (app.width/2)+(app.width//4.8), (app.height-(app.height//12)))
    easyBtnCenter=((easyBtn[0]+easyBtn[2])/2, (easyBtn[1]+easyBtn[3])/2)
    canvas.create_rectangle(easyBtn[0], easyBtn[1], easyBtn[2], easyBtn[3], fill="light blue")
    canvas.create_text(easyBtnCenter[0], easyBtnCenter[1]+(app.height//24), text="*Move Assistance highlight valid moves in green", font=f'Times {fontSize1}')
    canvas.create_text(easyBtnCenter[0], easyBtnCenter[1]+(app.height//15), text="and danger zone in red when you select a piece", font=f'Times {fontSize1}')
    if app.AIdrawing:
        canvas.create_text(app.width/2, app.height-(app.height//6), text="Waiting for AI to make a move", font=f'Times {fontSize2} bold')
    else:
        canvas.create_text(app.width/2, app.height-(app.height//6), text="Your Move", font=f'Times {fontSize2} bold')
    if app.easyMode:
        canvas.create_text(easyBtnCenter[0], easyBtnCenter[1], text="Move Assistance On", font=f'Times {fontSize3}')
    else:
        canvas.create_text(easyBtnCenter[0], easyBtnCenter[1], text="Move Assistance Off", font=f'Times {fontSize3}')


def localMode_mousePressed(app, event):
    x=event.x
    y=event.y
    print("number:", pieceNum(app, app.pieces))
    easyBtn=((app.width/2)-(app.width//4.8), (app.height-(app.height//7.5)), 
            (app.width/2)+(app.width//4.8), (app.height-(app.height//12))) 
    if ((x in range(int(easyBtn[0]), int(easyBtn[2]))) and 
        y in range(int(easyBtn[1]), int(easyBtn[3]))):
        app.easyMode=not app.easyMode
    if (not app.checkMate[app.player]) and (not app.localWent==app.player):
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
                currR=app.oldLoc[0]
                currC=app.oldLoc[1]
                if not isChecked(app, app.player):
                    app.AIdrawing=True
                    localMovePiece(app, row, col, currR, currC)
                    update_killzones(app)
                else:
                    if isGoodMove(app, row, col, currR, currC):
                        selectPiece(app, currR, currC)
                        app.AIdrawing=True
                        localMovePiece(app, row, col, currR, currC)
                        update_killzones(app)
                    else:
                        unselectPiece(app)
                        clearOutlines(app)
        else:
            pass
    else:
        pass

def localMode_timerFired(app):
    app.cellSize=min(app.width, (app.height/6)*4.8)/8
    scale=app.cellSize/90
    sprites=app.loadImage(os.path.join(sys.path[0], "chessSprites.png"))
    app.chessSprites=app.scaleImage(sprites, scale)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict() 
    init_sprites(app)
    if app.localWent==app.player:
        if app.AIdrawing:
            app.AIdrawing=False
        # Check if the player achieved a checkmate
        if checkMate(app, app.AIPlayer):
            app.checkMate[app.AIPlayer]=True
            app.mode="victory"
        else:
            # Have the AI make a move
            (AIcurrR, AIcurrC, AIrow, AIcol)=minimax(app, app.AIPlayer)
            print("move returned by minimax")
            if not isChecked(app, app.AIPlayer):
                AIMovePiece(app, AIrow, AIcol, AIcurrR, AIcurrC)
                print("AI moved:", AIrow, AIcol, AIcurrR, AIcurrC)
                update_killzones(app)
                # Checks if the AI achieved a checkmate
                if checkMate(app, app.player):
                    app.checkMate[app.player]=True
                    app.mode="defeat"
            else:
                if isGoodMove(app, AIrow, AIcol, AIcurrR, AIcurrC):
                    AIMovePiece(app, AIrow, AIcol, AIcurrR, AIcurrC)
    else:
        pass

#######################################################
# Online Game Mode #
#######################################################

def onlineMode_mousePressed(app, event):
    x=event.x
    y=event.y
    easyBtn=((app.width/2)-(app.width//4.8), (app.height-(app.height//7.5)), 
            (app.width/2)+(app.width//4.8), (app.height-(app.height//12)))
    if ((x in range(int(easyBtn[0]), int(easyBtn[2]))) and 
        y in range(int(easyBtn[1]), int(easyBtn[3]))):
        app.easyMode=not app.easyMode
    if not app.game.getWent(app.player) and not app.checkMate[app.player]:
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
                    if not isChecked(app, app.player):
                        onlineMovePiece(app, row, col, currR, currC)
                    else:
                        if isGoodMove(app, row, col, currR, currC):
                            selectPiece(app, currR, currC)
                            onlineMovePiece(app, row, col, currR, currC)
                        else:
                            unselectPiece(app)
                            clearOutlines(app)
                else:
                    pass
        else:
            pass
    else:
        pass

def onlineMode_timerFired(app):
    app.cellSize=min(app.width, (app.height/6)*4.8)/8
    scale=app.cellSize/90
    sprites=app.loadImage(os.path.join(sys.path[0], "chessSprites.png"))
    app.chessSprites=app.scaleImage(sprites, scale)
    # Initates dicts that store the sprites of chess pieces
    app.blackPieces=dict()
    app.whitePieces=dict() 
    init_sprites(app)
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
                otherPlayer=app.game.getOtherPlayer(app.player)
                print("Other player made a move", move)
                (currR, currC, row, col)=move
                # Mirror the move 
                currR=7-currR
                row=7-row
                piece=selectPiece(app, currR, currC)
                makeMove(app, app.pieces, row, col, currR, currC)
                # Updates the other player's king location if they moved their king
                if (app.pieces[currR][currC][1]=="king"):
                    app.kingLoc[otherPlayer]=(currR, currC)
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
                if checkMate(app, app.player):
                    app.checkMate[app.player]=True
                    app.n.send("Checkmate")
                    app.mode="defeat"
                    print("CheckMate")
                app.n.send("Updated")
                print("Your Turn")
            else:
                pass

def onlineMode_redrawAll(app, canvas):
    fontSize1=int(min(app.height, app.width)/35)
    fontSize3=int(min(app.height, app.width)/40)
    easyBtn=((app.width/2)-(app.width//4.8), (app.height-(app.height//7.5)), 
            (app.width/2)+(app.width//4.8), (app.height-(app.height//12)))
    easyBtnCenter=((easyBtn[0]+easyBtn[2])/2, (easyBtn[1]+easyBtn[3])/2)
    canvas.create_rectangle(easyBtn[0], easyBtn[1], easyBtn[2], easyBtn[3], fill="light blue")
    canvas.create_text(easyBtnCenter[0], easyBtnCenter[1]+(app.height//24), text="*Move Assistance highlight valid moves in green", font=f'Times {fontSize1}')
    canvas.create_text(easyBtnCenter[0], easyBtnCenter[1]+(app.height//15), text="and danger zone in red when you select a piece", font=f'Times {fontSize1}')
    drawBoard(app, canvas)
    loadPieces(app, canvas)
    if app.easyMode:
        canvas.create_text(easyBtnCenter[0], easyBtnCenter[1], text="Move Assistance On", font=f'Times {fontSize3}')
    else:
        canvas.create_text(easyBtnCenter[0], easyBtnCenter[1], text="Move Assistance Off", font=f'Times {fontSize3}')
    if app.game==None: 
        pass
    else:
        if app.game.getWent(app.player):
            canvas.create_text(app.width/2, app.height-(app.height//6), text="Waiting for Opponent's Move", font=f'Times {fontSize1} bold')
        else:
            canvas.create_text(app.width/2, app.height-(app.height//6), text="Your Move", font=f'Times {fontSize1} bold')

#######################################################
# # Main App # #
#######################################################

def appStarted(app):
    # Initiate server connection settings
    app.n=Network()
    app.player=None
    app.connecting=False
    app.game=None
    app.mode = 'landingPage'
    app.board=[[]for i in range(8)]
    # Initates boolean variable to detect whether a king is being checked
    app.check=False
    app.checkMate=[False, False]
    # Initiates variables to check for castling eligibility
    app.rightCastling=[True, True]
    app.leftCastling=[True, True]
    app.leftRookMoved=[False, False]
    app.rightRookMoved=[False, False]
    app.kingMoved=[False, False]
    # Initiates a variable to store the location of the king
    app.kingLoc=None 
    app.pieces=None
    # Initiates 2D lists to represent killzones
    app.whiteKZ=[[False, False, False, False, 
                False, False, False, False]for i in range(8)]
    app.blackKZ=[[False, False, False, False, 
                False, False, False, False]for i in range(8)]
    app.cellSize=min(app.width, app.height)/8
    scale=app.cellSize/90
    sprites=app.loadImage(os.path.join(sys.path[0], "chessSprites.png"))
    app.chessSprites=app.scaleImage(sprites, scale)
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
    # Initiate the values of chess pieces and store it in a dictionary
    app.values=init_values()
    # Initiates variable to keep track of which local player is due to move
    app.localWent=1
    # Initiates variable to store whether the player wants to play in easy mode or not
    app.easyMode=False
    # Initiate Zobrist hash table
    app.zobTable=init_Zob()
    # Initiate checkMate dict
    app.checkDict=init_check()
    # Initialize value multipliers list for minimax
    app.valueMultipliers=init_multipliers()
    app.AIdrawing=False

###############################################################################
# Initialization Functions

# Initialize value multipliers list for minimax
def init_multipliers():
    result=[[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], 
            [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7], 
            [1, 1, 1, 1.2, 1.2, 1, 1, 1], 
            [1.2, 1.2, 1.5, 2, 2, 1.5, 1.2, 1.2], 
            [1.2, 1.2, 1.5, 2, 2, 1.5, 1.2, 1.2],
            [1, 1, 1, 1.2, 1.2, 1, 1, 1], 
            [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7], 
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]
    return result

# Initiate checkMate dict from file
def init_check():
    file=open(os.path.join(sys.path[0], "check.pkl"), "rb")
    result=pickle.load(file)
    file.close()
    return result

"""
Zobrist Hashing concept from 
https://medium.com/@SereneBiologist/the-anatomy-of-a-chess-ai-2087d0d565
"""
# Initiate Zob table from file
def init_Zob():
    file = open(os.path.join(sys.path[0], "zobTable.pkl"),"rb")
    result=pickle.load(file)
    return result

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
    
# Initiates the values of each piece as a dictionary
def init_values():
    values={
        (0, "pawn"):-10,
        (0, "rook"):-50,
        (0, "knight"):-30,
        (0, "bishop"):-30, 
        (0, "queen"):-90, 
        (0, "king"):-900,
        (1, "pawn"):10,
        (1, "rook"):50, 
        (1, "knight"):30, 
        (1, "bishop"):30, 
        (1, "queen"):90,
        (1, "king"):900, 
    }
    return values

###############################################################################
# Minimax Algorithm

# Returns the value of a given board based on pieces
# Pieces are worth more if they are close to the center
def value(app, board):
    result=0
    for row in range(8):
        for col in range(8):
            color=board[row][col][0]
            piece=board[row][col][1]
            if color!=None:
                val=app.values[(color, piece)]
                result+=val
    return result

"""
Alpha-Beta Pruning concept from
https://medium.com/@SereneBiologist/the-anatomy-of-a-chess-ai-2087d0d565
"""
# Minmax algo where white is minimizing and black is maximizing
# Returns the optimal move for the current player on the board
def minimax(app, player):
    alpha=float("-inf")
    beta=float("inf")
    if app.checkMate[player]:
        return None
    # White move (minimize)
    elif player==0:
        optimal_move, value=minimize(app, app.pieces, 0, alpha, beta)
    # Black move (maximize)
    elif player==1:
        optimal_move, value=maximize(app, app.pieces, 0, alpha, beta)
    print("board value:", value)
    return optimal_move

"""
Alpha-Beta Pruning concept from
https://medium.com/@SereneBiologist/the-anatomy-of-a-chess-ai-2087d0d565
"""
# Returns the optimal move and the value of the resulting board 
# for the maximizing player
def maximize(app, board, depth, alpha, beta):
    print("depth=", depth)
    if depth>=2: 
        return (None, value(app, board))
    best_value=float("-inf")
    optimal_move=None
    moves=allValidMoves(app, board, 1)
    # Move sorting on the first level depth
    if depth==0:
        moves=sortMoves(app, moves, board)
    for move in moves:
        (currR, currC, row, col)=move
        board=result(app, board, currR, currC, row, col)
        minMove, minValue=minimize(app, board, depth+1, alpha, beta)
        if not isChecked(app, 1):
            if minValue>best_value:
                best_value=minValue
                optimal_move=move
            # Alpha-Beta Pruning
            alpha=max(alpha, best_value)
            if beta<=alpha: break
        else:  
            if (minValue>best_value) and isGoodMove(app, row, col, currR, currC):
                best_value=minValue
                optimal_move=move
            # Alpha-Beta Pruning
            alpha=max(alpha, best_value)
            if beta<=alpha: break
    return (optimal_move, best_value)

"""
Alpha-Beta Pruning concept from
https://medium.com/@SereneBiologist/the-anatomy-of-a-chess-ai-2087d0d565
"""
# Returns the optimal move and the value of the resulting board 
# for the minimizing player
def minimize(app, board, depth, alpha, beta):
    print("depth=", depth)
    if depth>=2: 
        return (None, value(app, board))
    best_value=float("inf")
    optimal_move=None
    moves=allValidMoves(app, board, 0)
    # Move sorting on the first level depth
    if depth==0:
        moves=sortMoves(app, moves, board)
    for move in moves:
        (currR, currC, row, col)=move
        board=result(app, board, currR, currC, row, col)
        minMove, maxValue=maximize(app, board, depth+1, alpha, beta)
        if not isChecked(app, 0):
            if maxValue<best_value:
                best_value=maxValue
                optimal_move=move
            beta=min(beta, best_value)
            # Alpha-Beta pruning
            if beta<=alpha:break
        else:
            if maxValue<best_value and isGoodMove(app, row, col, currR, currC):
                best_value=maxValue
                optimal_move=move
            # Alpha-Beta pruning
            beta=min(beta, best_value)
            if beta<=alpha:break
    return (optimal_move, best_value)

# Returns the board that results from making a move [currR][currR] to [row][col]
def result(app, board, currR, currC, row, col):
    currBoard=copy.deepcopy(board)
    makeMove(app, currBoard, row, col, currR, currC)
    return currBoard
    
# Returns a random valid move
def randomizer(app, player):
    moves=allValidMoves(app, app.pieces, player)
    if isChecked(app, player):
        while True:
            (currR, currC, row, col)=moves.pop()
            if isGoodMove(app, row, col, currR, currC):
                move=(currR, currC, row, col)
                break
    else:
        move=moves.pop()
    return move
    
# Returns the number of pieces on the board
def pieceNum(app, board):
    result=0
    for row in range(8):
        for col in range(8):
            if board[row][col][0]!=None:
                result+=1
    return result

# Sorts the moves based on if they result in piece eating
def sortMoves(app, moves, board):
    sortedMoves=list()
    oldCount=pieceNum(app, board)
    for move in moves:
        (currR, currC, row, col)=move
        resultBoard=result(app, board, currR, currC, row, col)
        newCount=pieceNum(app, resultBoard)
        if newCount<oldCount:
            sortedMoves.append(move)
            moves.remove(move)
    for move in moves:
        sortedMoves.append(move)
    return sortedMoves

# Returns a set of all valid moves 
def allValidMoves(app, board, player):
    result=list()
    for row in range(8):
        for col in range(8):
            if board[row][col][0]==player:
                result.extend(validMovesFromRowCol(app, board, player, row, col))
            else: continue
    return result

# Returns a set of valid moves from [row][col]
def validMovesFromRowCol(app, board, player, currR, currC):
    result=list()
    for row in range(8):
        for col in range(8):
            piece=board[currR][currC][1]
            # Checks for friendly piece collision
            if board[row][col][0]==player: continue
            # Checks valid moves based on piece type
            if piece=="pawn": 
                if currR==6 and player==app.player:
                    if isValidStartPawnMove(app, board, currR, currC, row, col, player):
                        result.append((currR, currC, row, col))
                    else: continue
                elif currR==1 and player!=app.player:
                    if isValidStartPawnMove(app, board, currR, currC, row, col, player):
                        result.append((currR, currC, row, col))
                    else: continue
                else:
                    if isValidPawnMove(app, board, currR, currC, row, col, player):
                        result.append((currR, currC, row, col))
                    else: continue
            elif piece=="rook":
                if isValidRookMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
            elif piece=="knight":
                if isValidKnightMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
            elif piece=="bishop":
                if isValidBishopMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
            elif piece=="queen":
                if isValidQueenMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
            elif piece=="king":
                if AIisValidKingMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
    return result

###############################################################################
# Status Update Functions

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
                if isValidRookMove(app, app.pieces, currR, currC, row, col, 1):
                    rookSet.append((row, col))
                if isValidKnightMove(app, app.pieces, currR, currC, row, col, 1):
                    knightSet.append((row, col))
                if isValidBishopMove(app, app.pieces, currR, currC, row, col, 1):
                    bishopSet.append((row, col))
                if isValidQueenMove(app, app.pieces, currR, currC, row, col, 1):
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
            if isValidRookMove(app, app.pieces, currR, currC, row, col, 0):
                rookSet.append((row, col))
            if isValidKnightMove(app, app.pieces, currR, currC, row, col, 0):
                knightSet.append((row, col))
            if isValidBishopMove(app, app.pieces, currR, currC, row, col, 0):
                bishopSet.append((row, col))
            if isValidQueenMove(app, app.pieces, currR, currC, row, col, 0):
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
def updateCastlingEligibility(app, player):
    if app.kingMoved[player]:
        app.rightCastling[player]=False
        app.leftCastling[player]=False
    elif app.leftRookMoved[player]:
        app.leftCastling[player]=False
    elif app.rightRookMoved[player]:
        app.rightCastling[player]=False

###############################################################################
# Board Cosmetic Functions

# Update board outlines for display
def updateOutlines(app, player, currR, currC):
    updateKZOutlines(app, player)
    updateValidMoves(app, currR, currC)

# Clear all board outlines
def clearOutlines(app):
    clearValidMoves(app)
    clearKZOutlines(app)

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

# Clear valid moves
def clearValidMoves(app):
    for row in range(8):
        for col in range(8):
            app.validMoves[row][col]=False

# Updates valid moves for selected piece in [currR][currC]
def updateValidMoves(app, currR, currC):
    for row in range(8):
        for col in range(8):
            if isValidMove(app, app.pieces, row, col, currR, currC):
                app.validMoves[row][col]=True

###############################################################################
# Board Hashing

# Updates the hash file after the app closes
def update_hash(app):
    file=open(os.path.join(sys.path[0], "check.pkl"), "wb")
    pickle.dump(app.checkDict, file)
    file.close()

# Hash function that reduces a chess board into a zobrist hash code
def hashBoard(app, board):
    result=0
    for row in range(8):
        for col in range(8):
            if board[row][col][0]!=None:
                piece=board[row][col]
                value=map_pieces(piece)
                result^=app.zobTable[row][col][value]
    return result

# Maps each chess piece to a value for hashing purposes
def map_pieces(piece):
    color=piece[0]
    piece=piece[1]
    if color==0:
        if piece=="pawn":
            return 0
        elif piece=="rook":
            return 1
        elif piece=="knight":
            return 2
        elif piece=="bishop":
            return 3
        elif piece=="queen":
            return 4
        elif piece=="king":
            return 5
    elif color==1:
        if piece=="pawn":
            return 6
        elif piece=="rook":
            return 7
        elif piece=="knight":
            return 8
        elif piece=="bishop":
            return 9
        elif piece=="queen":
            return 10
        elif piece=="king":
            return 11

###############################################################################
# Move Validity Functions

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
    if isValidMove(app, app.pieces, row, col, currR, currC):
        return tryMove(app, row, col, currR, currC)
    else: return False

# Tries the move from [currR][currC] to [row][col]
# returns true if the move breaks the check
# False otherwise
def tryMove(app, row, col, currR, currC):
    myPiece=app.pieces[currR][currC]
    otherPiece=app.pieces[row][col]
    player=myPiece[0]
    # Update the king's location if the player is moving his king
    if myPiece[1]=="king":
        app.kingLoc[player]=(row, col)
    app.pieces[currR][currC]=(None, "empty")
    app.pieces[row][col]=myPiece
    update_killzones(app)
    if isChecked(app, player):
        result=False
    else:
        result=True
    # Reset the move
    if myPiece[1]=="king":
        app.kingLoc[player]=(currR, currC)
    app.pieces[row][col]=otherPiece
    app.pieces[currR][currC]=myPiece
    update_killzones(app)
    print("Move tried:", currR, currC, row, col, result)
    return result

# Returns the number of pieces on the board
def pieceNum(app, board):
    result=0
    for row in range(8):
        for col in range(8):
            if board[row][col][0]!=None:
                result+=1
    return result

# Sorts the moves based on if they result in piece eating
def sortMoves(app, moves, board):
    sortedMoves=list()
    oldCount=pieceNum(app, board)
    for move in moves:
        (currR, currC, row, col)=move
        resultBoard=result(app, board, currR, currC, row, col)
        newCount=pieceNum(app, resultBoard)
        if newCount<oldCount:
            sortedMoves.append(move)
            moves.remove(move)
    for move in moves:
        sortedMoves.append(move)
    return sortedMoves

# Returns a set of all valid moves 
def allValidMoves(app, board, player):
    result=list()
    for row in range(8):
        for col in range(8):
            if board[row][col][0]==player:
                result.extend(validMovesFromRowCol(app, board, player, row, col))
            else: continue
    return result

# Returns a set of valid moves from [row][col]
def validMovesFromRowCol(app, board, player, currR, currC):
    result=list()
    for row in range(8):
        for col in range(8):
            piece=board[currR][currC][1]
            # Checks for friendly piece collision
            if board[row][col][0]==player: continue
            # Checks valid moves based on piece type
            if piece=="pawn":
                if currR==6 and player==app.player:
                    if isValidStartPawnMove(app, board, currR, currC, row, col, player):
                        result.append((currR, currC, row, col))
                    else: continue
                elif currR==1 and player!=app.player:
                    if isValidStartPawnMove(app, board, currR, currC, row, col, player):
                        result.append((currR, currC, row, col))
                    else: continue
                else:
                    if isValidPawnMove(app, board, currR, currC, row, col, player):
                        result.append((currR, currC, row, col))
                    else: continue
            elif piece=="rook":
                if isValidRookMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
            elif piece=="knight":
                if isValidKnightMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
            elif piece=="bishop":
                if isValidBishopMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
            elif piece=="queen":
                if isValidQueenMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
            elif piece=="king":
                if AIisValidKingMove(app, board, currR, currC, row, col, player):
                    result.append((currR, currC, row, col))
                else: continue
    return result

# Checks if [row][col] is a valid move from [currR][currC]
def isValidMove(app, board, row, col, currR, currC):
    color=app.pieces[currR][currC][0]
    piece=app.pieces[currR][currC][1]
    # Checks for friendly piece collision
    if app.pieces[row][col][0]==color: return False
    # Checks valid moves based on piece type
    if piece=="pawn":
        if currR==6:
            return isValidStartPawnMove(app, board, currR, currC, row, col, color)
        else:
            return isValidPawnMove(app, board, currR, currC, row, col, color)
    elif piece=="rook":
        return isValidRookMove(app, board, currR, currC, row, col, color)
    elif piece=="knight":
        return isValidKnightMove(app, board, currR, currC, row, col, color)
    elif piece=="bishop":
        return isValidBishopMove(app, board, currR, currC, row, col, color)
    elif piece=="queen":
        return isValidQueenMove(app, board, currR, currC, row, col, color)
    elif piece=="king":
        return isValidKingMove(app, board, currR, currC, row, col, color)

# Checks if [row][col] is a valid start pawn move from [currR][currC]
def isValidStartPawnMove(app, board, currR, currC, row, col, color):
    if color==app.player:
        # Empty cells move set
        if board[row][col]==(None, "empty"):
            if ((col==currC) and 
                ((currR==row+1)or (currR==row+2)) and
                (board[currR-1][currC]==(None, "empty"))):
                return True
            else: return False
        # Enemy eating movement set
        else:
            if (currR==row+1) and ((col==currC-1) or (col==currC+1)):
                return True
            else: return False
    else:
        # Empty cells move set
        if board[row][col]==(None, "empty"):
            if ((col==currC) and 
                ((currR==row-1)or (currR==row-2)) and
                (board[currR+1][currC]==(None, "empty"))):
                return True
            else: return False
        # Enemy eating movement set
        else:
            if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
                return True
            else: return False

# Checks if [row][col] is a valid normal pawn move from [currR][currC]
def isValidPawnMove(app, board, currR, currC, row, col, color):
    if color==app.player:
        # Empty cells move set
        if board[row][col]==(None, "empty"):
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
    else:
        # Empty cells move set
        if board[row][col]==(None, "empty"):
            if (col==currC) and (currR==row-1):
                return True
            else: 
                # En Passant
                if app.lastMove!=None:
                    (elem, originR, originC, dRow, dCol)=app.lastMove
                    c=elem[0]
                    piece=elem[1]
                    if ((currR==4) and (color!=c) and (piece=="pawn") and 
                        (originR==6) and (dRow==4) and ((originC==currC+1) or (originC==currC-1))):
                        if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
                            return True
                        else: return False
                    else:return False
                else: return False
        # Enemy eating movement set
        else:
            if (currR==row-1) and ((col==currC-1) or (col==currC+1)):
                return True
            else: return False

# Checks if [row][col] is a valid rook move from [currR][currC]
def isValidRookMove(app, board, currR, currC, row, col, color):
    # Not moving is not a valid move
    if row==currR and col==currC: 
        return False
    else:
        # Gets the furthest possible column positions
        leftC, rightC=nearestPieceOnRow(app, board, currR, currC)
        # Gets the furthest possible row positions
        topR, botR=nearestPieceOncol(app, board, currR, currC)
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
def isValidKnightMove(app, board, currR, currC, row, col, color):
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
def isValidBishopMove(app, board, currR, currC, row, col, color):
    # Not moving is not a valid move
    if row==currR and col==currC: 
        return False
    else:
        leftD, Lindex=Ldiag(currR, currC)
        Lleft, Lright=nearestPieceLDiag(app, board, currR, currC)
        rightD, Rindex=Rdiag(currR, currC)
        Rleft, Rright=nearestPieceRDiag(app, board, currR, currC)
        for coord in rightD[Rleft:Rright+1]:
            if (row, col)==coord:
                return True
        for coord in leftD[Lleft:Lright+1]:
            if (row, col)==coord:
                return True
        return False

# Checks if [row][col] is a valid queen move from [currR][currC]
def isValidQueenMove(app, board, currR, currC, row, col, color):
    return (isValidBishopMove(app, board, currR, currC, row, col, color) or
                    isValidRookMove(app, board, currR, currC, row, col, color))

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

# Checks if [row][col] is a valid king move from [currR][currC] but without kzs
def AIisValidKingMove(app, board, currR, currC, row, col, color):
    # Not moving is not a valid move
    if row==currR and col==currC: return False
    else:
        if (((currR+1==row) or (currR-1==row) or (currR==row)) 
            and ((currC+1==col) or (currC-1==col) or (currC==col))):
            return True
        else:
            return False

# Checks if [row][col] is a valid king move from [currR][currC]
def isValidKingMove(app, board, currR, currC, row, col, color):
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
    if (app.rightCastling[0] and 
        (not isChecked(app, 0)) and 
        (app.pieces[row][col]==(None, "empty")) and 
        (app.pieces[row][col-1]==(None, "empty")) and 
        (not app.blackKZ[row][col]) and 
        (not app.blackKZ[row][col-1])):
        return True
    else: return False

# Checks if move from [currR][currC] to [row][col] is 
# a valid left white castling move
def isValidLeftWhiteCastling(app, currR, currC, row, col):
    if (app.leftCastling[1] and 
        (not isChecked(app, 0)) and
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
    if (app.rightCastling[1] and 
        (not isChecked(app, 1)) and 
        (app.pieces[row][col]==(None, "empty")) and 
        (app.pieces[row][col-1]==(None, "empty")) and 
        (not app.whiteKZ[row][col]) and 
        (not app.whiteKZ[row][col-1])):
        return True
    else: return False

# Checks if move from [currR][currC] to [row][col] is 
# a valid left black castling move
def isValidLeftBlackCastling(app, currR, currC, row, col):
    if (app.leftCastling[1] and 
        (not isChecked(app, 1)) and
        (app.pieces[row][col]==(None, "empty")) and 
        (app.pieces[row][col-1]==(None, "empty")) and 
        (app.pieces[row][col+1]==(None, "empty")) and 
        (not app.whiteKZ[row][col]) and 
        (not app.whiteKZ[row][col+1])):
        return True
    else: return False

# Returns the coordinates of the closest pieces to [currR][currC] 
# on the same left diagonal
def nearestPieceLDiag(app, board, currR, currC):
    diag, index=Ldiag(currR, currC)
    left=0
    right=len(diag)-1
    i=index-1
    while i>=0:
        (row, col)=diag[i]
        if board[row][col]!=(None, "empty"):
            left=i
            break
        i-=1
    i=index+1
    while i<len(diag):
        (row, col)=diag[i]
        if board[row][col]!=(None, "empty"):
            right=i
            break
        i+=1
    return left, right

# Returns the coordinates of the closest pieces to [currR][currC] 
# on the same right diagonal
def nearestPieceRDiag(app, board, currR, currC):
    diag, index=Rdiag(currR, currC)
    left=0
    right=len(diag)-1
    i=index-1
    while i>=0:
        (row, col)=diag[i]
        if board[row][col]!=(None, "empty"):
            left=i
            break
        i-=1
    i=index+1
    while i<len(diag):
        (row, col)=diag[i]
        if board[row][col]!=(None, "empty"):
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
def nearestPieceOnRow(app, board, currR, currC):
    rightC=7
    leftC=0
    i=currC+1
    while i<8:
        if board[currR][i]!=(None, "empty"):
            rightC=i
            break
        i+=1
    i=currC-1
    while i>=0:
        if board[currR][i]!=(None, "empty"):
            leftC=i
            break
        i-=1
    return leftC, rightC

# Returns the col of the closest piece to [currR][currC] on the same row
def nearestPieceOncol(app, board, currR, currC):
    topR=7
    botR=0
    i=currR+1
    while i<8:
        if board[i][currC]!=(None, "empty"):
            topR=i
            break
        i+=1
    i=currR-1
    while i>=0:
        if board[i][currC]!=(None, "empty"):
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

###############################################################################
# Move Making Functions

# Moves the selected chess piece to the destination cell on the designated board
def makeMove(app, board, row, col, currR, currC):
    piece=board[currR][currC]
    player=piece[0]
    # Update the king's location if the player is moving his king
    if piece[1]=="king" and board is app.pieces:
        app.kingLoc[player]=(row, col)
        app.kingMoved[player]=True
    elif piece[1]=="rook" and player==0 and board is app.pieces:
        if currC==0:
            app.leftRookMoved[player]=True
        elif currC==7:
            app.rightRookMoved[player]=True
    elif piece[1]=="rook" and player==1 and board is app.pieces:
        if currC==0:
            app.rightRookMoved[player]=True
        elif currC==7:
            app.leftRookMoved[app.player]=True
    board[currR][currC]=(None, "empty")
    board[row][col]=piece
    update_killzones(app)
    updateCastlingEligibility(app, app.player)
    app.oldLoc=None
    app.makingMove=False

# Moves the piece for the AI based on its input
def AIMovePiece(app, row, col, currR, currC):
    makeMove(app, app.pieces, row, col, currR, currC)
    app.lastMove=(app.pieces[row][col], currR, currC, row, col)
    app.localWent=app.AIPlayer

# Makes the move based on the piece the user selected locally
def localMovePiece(app, row, col, currR, currC):
    if isValidMove(app, app.pieces, row, col, currR, currC):
        player=app.pieces[currR][currC][0]
        # Checks if the move just made enables the player to promote a pawn
        if ((app.pieces[currR][currC][1]=="pawn") and
            (row==0)):
            app.mode="localPawnPromotion"
            app.promotingPawn=(currR, currC, row, col)
            makeMove(app, app.pieces, row, col, currR, currC)
            update_killzones(app)
            clearOutlines(app)
        else:
            # En Passant
            if ((app.pieces[currR][currC][1]=="pawn") and 
                (col!=currC) and 
                (app.pieces[row][col][0]==None)):
                # Kill the piece during an En Passant
                app.pieces[currR][col]=(None, "empty")
                print("EnPassant at:", currR, currC, row, col)
            elif app.pieces[currR][currC][1]=="king":
                # Moves the rook in right castling
                if (row==currR) and (col==currC+2):
                    rook=app.pieces[row][col+1]
                    app.pieces[row][col-1]=rook
                    app.pieces[row][col+1]=(None, "empty")
                # Moves the rook in left castling
                elif (row==currR) and (col==currC-2):
                    rook=app.pieces[row][col-2]
                    app.pieces[row][col+1]=rook
                    app.pieces[row][col-2]=(None, "empty")
            makeMove(app, app.pieces, row, col, currR, currC)
            clearOutlines(app)
            update_killzones(app)
            app.lastMove=(app.pieces[row][col], currR, currC, row, col)
            app.localWent=player
    # Clear outlines
    else:
        unselectPiece(app)
        clearOutlines(app)

# Make the move based on the piece the user selected 
# and send data to the server
def onlineMovePiece(app, row, col, currR, currC):
    if isValidMove(app, app.pieces, row, col, currR, currC):
        # Checks if the move just made enables the player to promote a pawn
        if ((app.pieces[currR][currC][1]=="pawn") and
            (row==0)):
            app.mode="onlinePawnPromotion"
            app.promotingPawn=(currR, currC, row, col)
            app.n.send("resetSpecialMoves")
            makeMove(app, app.pieces, row, col, currR, currC)
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
            makeMove(app, app.pieces, row, col, currR, currC)
            clearOutlines(app)
    # Clear outlines
    else:
        unselectPiece(app)
        clearOutlines(app)

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

###############################################################################
# CheckMate Detection Functions

# Returns True if there is a move that breaks the check
# False otherwise
def checkMate(app, player):
    if app.checkMate[player]: return True
    else:
        if isChecked(app, player):
            h=hashBoard(app, app.pieces)
            if h in app.checkDict:
                return app.checkDict[h]
            else:
                for row in range(8):
                    for col in range(8):
                        if app.pieces[row][col][0]==player:
                            if checkMovesFromRowCol(app, row, col):
                                app.checkDict[h]=False
                                update_hash(app)
                                return False
                app.checkMate[player]=True
                app.checkDict[h]=True
                update_hash(app)
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
def isChecked(app, player):
    (row, col)=app.kingLoc[player]
    if player==0:
        if app.blackKZ[row][col]: return True
        else: return False
    elif player==1:
        if app.whiteKZ[row][col]: return True
        else: return False

###############################################################################
# Drawing Functions

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
    if app.easyMode:
        if app.kzOutlines[row][col] is True:
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='red', 
                                    width=4)
        elif app.validMoves[row][col] is True:
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='green', 
                                    width=4)
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='black', 
                                    width=3)
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
    runApp(width=480, height=600, mvcCheck=False)

if __name__=="__main__":
    chessAnimation()