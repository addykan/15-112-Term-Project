from primMapMaker import *
from cmu_112_graphics import *

def appStarted(app):
    app.isPaused = False
    app.startScreen = True
    app.gameStarted = False
    app.inInventory = False
    app.difficulty = 10
    app.level = level(app.difficulty)
    app.player = player('Mario')
    app.level.grid[0][0].contents = app.player
    app.screenBounds = 4
    app.currentCenter = (0, 0)


def keyPressed(app, event):
    if app.startScreen:
        app.gameStarted = True
    if app.gameStarted and not app.isPaused and event.key == 'W':
        movePlayerUp(app)
    if app.gameStarted:
        pass

def movePlayerUp(app):
    pass

def movePlayerDown(app):
    pass

def movePlayerLeft(app):
    pass

def movePlayerRight(app):
    pass

def moveEnemy(app, location, direction):
    pass


def drawPlayer(app, canvas):
    headTopLeftX = app.width // 2 - (app.width // 30)
    headTopLeftY = (app.height // 2 - (app.height // 30)) - app.height // 20
    headBottomRightX = app.width // 2 + (app.width // 30)
    headBottomRightY = (app.height // 2 + (app.height // 30)) - app.height // 20
    canvas.create_oval(headTopLeftX, headTopLeftY, headBottomRightX, headBottomRightY, fill = 'green')
    canvas.create_line(app.width//2, headBottomRightY, app.width // 2, app.height//2 + app.height//20)
    canvas.create_line(app.width//2 - app.width//20, app.height//2, app.width//2 + app.width//20, app.height//2)


def drawMap(app, canvas):
    centerCellRow = app.currentCenter[0]
    centerCellCol = app.currentCenter[1]
    minRow = centerCellRow - app.screenBounds
    minCol = centerCellCol - app.screenBounds
    maxRow = centerCellRow + app.screenBounds
    maxCol = centerCellCol + app.screenBounds
    numCells = 2 * app.screenBounds + 1
    cellStartX = 0
    cellStartY = 0
    for row in range(minRow, maxRow + 1):
        for col in range(minCol, maxCol + 1):
            if (row < 0 or col < 0 or row >= len(app.level.grid) or col >= len(app.level.grid[0])) or not app.level.grid[row][col].status:  # Outside the grid, or a wall
                canvas.create_rectangle(cellStartX, cellStartY, cellStartX + app.width // numCells, cellStartY + app.width // numCells, fill = 'black')
            else:  # In the grid, not a wall
                canvas.create_rectangle(cellStartX, cellStartY, cellStartX + app.width // numCells, cellStartY + app.width // numCells, fill='white')
            cellStartX += app.width // numCells
        cellStartY += app.height // numCells
        cellStartX = 0


def drawEnemies(app, canvas):
    pass

def drawLevel(app, canvas):
    drawMap(app, canvas)
    drawEnemies(app, canvas)
    drawPlayer(app, canvas)

def redrawAll(app, canvas):
    if app.gameStarted and not app.isPaused:
        drawLevel(app, canvas)


width = 600
height = 600

runApp(width = width, height=height)