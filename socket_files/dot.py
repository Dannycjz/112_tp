from cmu_112_graphics import *
import math, pickle
from network import Network

def s21MidtermAnimation_appStarted(app):
    app.n=Network("172.26.18.51")
    # Sets parameters for app objects
    app.dots=pickle.loads(app.n.dots)
    app.currDot=None

# def s21MidtermAnimation_keyPressed(app, event):
#     # Reset the animation if the user presses r
#     if event.key=='r':
#         s21MidtermAnimation_appStarted(app)

def s21MidtermAnimation_mousePressed(app, event):
    # Creates a dot at the location of the mounse click
    x=event.x
    y=event.y
    app.currDot=(x, y)

def s21MidtermAnimation_timerFired(app):
    if app.currDot==None:
        pass
    else:
        currDot=app.currDot
        app.dots=app.n.send(currDot)

def s21MidtermAnimation_redrawAll(app, canvas):
    # Draw all points 
    for point in app.dots:
        r=20
        cx=point[0]
        cy=point[1]
        fill=point[2]
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=fill)

def s21Midterm1Animation():
    runApp(width=400, height=400, fnPrefix='s21MidtermAnimation_')

if __name__=="__main__":
    s21Midterm1Animation()