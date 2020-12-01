from mapMaker import *
from cmu_112_graphics import *

def appStarted(app):
    app.isPaused = False
    app.startScreen = True
    app.gameStarted = False
    app.inInventory = False
    app.difficulty = 1
    app.level = level(app.difficulty)
    app.levelGrid = levelGrid(app.level)
    app.player = player('Mario')
    app.screenBounds = ((0,0), (10,10))


def keyPressed(app, event):
    if app.startScreen:
        app.gameStarted = True
    if app.gameStarted and not app.isPaused and event.key == 'W':
        movePlayerUp(app)
    if app.gameStarted:
        pass

def movePlayerUp(app):
    pass

def redrawAll(app, canvas):
    pass
