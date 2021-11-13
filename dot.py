from cmu_112_graphics import *
import math

def s21MidtermAnimation_appStarted(app):

    # Sets parameters for app objects

    app.dots=[]

    app.lines=[]

    app.pressed=0

    app.x=0

    app.y=0

    app.timerDelay=1000


def s21MidtermAnimation_keyPressed(app, event):

    # Reset the animation if the user presses r

    if event.key=='r':

        s21MidtermAnimation_appStarted(app)


def s21MidtermAnimation_mousePressed(app, event):

    # Creates a dot at the location of the mounse click

    app.x=event.x

    app.y=event.y

    app.pressed=0

    app.dots.append((app.x, app.y))

    dot=s21MidtermAnimation_findClosestDot(app, app.x, app.y)

    # Add a line to the nearest dot if there is another dot in existance

    if dot is not None:

        x=dot[0]

        y=dot[1]

        line=[x, y, app.x, app.y]

        app.lines.append(line)


def s21MidtermAnimation_timerFired(app):

    # Restart the game after 5 seconds

    app.pressed+=1

    if app.pressed>=5: 

        s21MidtermAnimation_appStarted(app)


# Returns the closest dot to cx, cy

def s21MidtermAnimation_findClosestDot(app, cx, cy): 

    smallestDist=float('inf')

    bestPoint=None

    # Iterates over the existing dots and find the one closest

    for point in app.dots:

        x=point[0]

        y=point[1]

        if x==cx and y==cy: 

            continue

        dist=math.sqrt(((x-cx)**2)+((y-cy)**2))

        if dist<smallestDist: 

            bestPoint=(x, y)

            smallestDist=dist

    return bestPoint


def s21MidtermAnimation_redrawAll(app, canvas):

    # Draw all points

    for point in app.dots:

        r=20

        cx=point[0]

        cy=point[1]

        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='green')

    # Draw all lines

    for line in app.lines:

        canvas.create_line(line[0],line[1], line[2], line[3])


def s21Midterm1Animation():
    runApp(width=400, height=400, fnPrefix='s21MidtermAnimation_')

if __name__=="__main__":
    s21Midterm1Animation()
