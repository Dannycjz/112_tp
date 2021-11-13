from cmu_112_graphics import *

def appStarted(app):
    app.board=[[]for i in range(8)]
    app.cellSize=app.width//8

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
    canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline='black', 
                            width=3)

# Draws the board by calling drawCell on every individual cell
def drawBoard(app, canvas):
    for row in range(8): 
        for col in range(8): 
            drawCell(app, canvas, row, col)

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='white')
    drawBoard(app, canvas)

def chessAnimation():
    runApp(width=800, height=800)

if __name__=="__main__":
    chessAnimation()