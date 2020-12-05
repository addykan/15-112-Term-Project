from primMapMaker import *
from cmu_112_graphics import *

def appStarted(app):
    app.isPaused = False
    app.startScreen = True
    app.gameStarted = False
    app.inInventory = False
    app.difficulty = 15
    app.level = level(app.difficulty)
    app.player = player('Mario')
    app.level.grid[0][0].contents = app.player
    app.screenBounds = 4
    app.currentCenter = [0, 0]
    app.lastDir = None
    app.onWeapon = False
    app.enemyCount = app.difficulty
    app.timerDelay = 250

def nextLevel(app):
    app.difficulty += 5
    app.level = level(app.difficulty)
    app.level.grid[0][0].contents = app.player
    app.currentCenter = [0, 0]
    app.lastDir = None
    app.onWeapon = False
    app.enemyCount = app.difficulty

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
    if app.startScreen:
        app.gameStarted = True
    if app.gameStarted:
        if event.key == 'esc':
            app.isPaused = not app.isPaused
        elif app.isPaused:
            pass
        elif not app.isPaused:
            if event.key in 'wasd':
                app.lastDir = event.key
                if event.key == 'w':
                    movePlayer(app, -1, 0)
                elif event.key == 'a':
                    movePlayer(app, 0, -1)
                elif event.key == 's':
                    movePlayer(app, 1, 0)
                elif event.key == 'd':
                    movePlayer(app, 0, 1)
            elif event.key == 'Space':
                useWeapon(app)
            elif event.key == 'Tab':
                swapWeapons(app)
            elif event.key == 'Enter':
                pickUpWeapon(app)


def mousePressed(app, event):  # press any key including the mouse to start, but mouse has no use otherwise
    if app.startScreen:
        app.gameStarted = True


def killEnemy(app):
    app.enemyCount -= 1
    if app.enemyCount == 0:
        nextLevel(app)


def swapWeapons(app):
    if len(app.player.gear) > 1:
        app.player.gear = app.player.gear[1:] + app.player.gear[0]
        app.player.activeWeapon = app.player.gear[0]


def pickUpWeapon(app):
    if isinstance(app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents, weapon):
        if len(app.player.gear) < 5:
            app.player.gear.append(app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents)
            app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = app.player


def movePlayer(app, drow, dcol):
    if app.currentCenter[0] + drow < 0 or app.currentCenter[0] + drow >= len(app.level.grid) or app.currentCenter[1] + dcol < 0 or app.currentCenter[1] + dcol >= len(app.level.grid):
        return
    if app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].status:  # If it's a tunnel where an object can be
        if app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents is None:
            app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents = app.player  # Place the player in the new location
            if not app.onWeapon:
                app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = None  # Clear the old location
            app.currentCenter[0] += drow  # Move the camera and stored location of player
            app.currentCenter[1] += dcol
            app.onWeapon = False
        elif isinstance(app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents, heart):  # If there's a heart in the cell player wants to move into
            # Automatically pick up heart
            app.player.health += app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents.health
            app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents = app.player  # Place the player in the new location
            if not app.onWeapon:
                app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = None  # Clear the old location
            app.currentCenter[0] += drow  # Move the camera and stored location of player
            app.currentCenter[1] += dcol
            app.onWeapon = False
        elif isinstance(app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents, weapon):
            app.onWeapon = True
            #print('standing on a weapon', app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents)
            app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = None  # Clear the old location
            app.currentCenter[0] += drow  # Move the camera and stored location of player
            app.currentCenter[1] += dcol


def useWeapon(app):
    print('weapon used')
    if isinstance(app.player.activeWeapon, pistol) or isinstance(app.player.activeWeapon, rocket):
        useProjectileWeapon(app)
    elif isinstance(app.player.activeWeapon, sword):
        useSword(app)


def useProjectileWeapon(app):
    projectileDirs = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}
    if app.lastDir is not None:
        if app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].status:
            if app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents is None:
                app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents = projectile(projectileDirs[app.lastDir][0],
                                                                                                                                                                   projectileDirs[app.lastDir][1],
                                                                                                                                                                   app.player.activeWeapon.damage,
                                                                                                                                                                   app.player.activeWeapon.travelSpeed)
            elif isinstance(app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents, enemy):
                app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents.health -= app.player.activeWeapon.damage
                if app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents.health <= 0:
                    app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents = None
                    killEnemy(app)

def useSword(app):
    pass

def moveProjectiles(app):
    for row in range(len(app.level.grid)):
        for col in range(len(app.level.grid[0])):
            if isinstance(app.level.grid[row][col].contents, projectile):
                moveProjectile(app, row, col)

def moveProjectile(app, row, col):
    for _ in range(app.level.grid[row][col].contents.speed):
        drow = app.level.grid[row][col].contents.drow
        dcol = app.level.grid[row][col].contents.dcol
        if row + drow >= 0 and row + drow < len(app.level.grid) and col + dcol >= 0 and col + dcol < len(app.level.grid[0]):  # Check if it's in the grid
            if app.level.grid[row+drow][col+dcol].status:  # Check if it's not a wall
                if isinstance(app.level.grid[row+drow][col+dcol].contents, enemy):  # If we hit an enemy!
                    app.level.grid[row + drow][col + dcol].contents.health -= app.level.grid[row][col].contents.damage
                    if app.level.grid[row + drow][col + dcol].contents.health <= 0:
                        app.level.grid[row + drow][col + dcol].contents = None
                        killEnemy(app)
                elif app.level.grid[row+drow][col+dcol].contents is None:
                    app.level.grid[row + drow][col + dcol].contents = app.level.grid[row][col].contents
    app.level.grid[row][col].contents = None


def moveEnemy(app, location, direction):
    pass

def moveEnemies(app):
    pass

def takeStep(app):
    moveEnemies(app)
    moveProjectiles(app)
    pass  # Move enemies


def timerFired(app):
    if not app.isPaused:
        takeStep(app)

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
                if app.level.grid[row][col].contents != None: # and app.level.grid[row][col].contents != app.player:  # Draw an object in the cell - enemy, powerup, or weapon
                    #print('something should be printed')
                    #print(type(app.level.grid[row][col].contents))
                    if isinstance(app.level.grid[row][col].contents, enemy):
                        #print('making enemy')
                        canvas.create_oval(cellStartX, cellStartY, cellStartX + app.width // numCells, cellStartY + app.width // numCells, fill='red')
                    elif isinstance(app.level.grid[row][col].contents, heart):
                        #print('making heart')
                        canvas.create_oval(cellStartX, cellStartY, cellStartX + app.width // numCells, cellStartY + app.width // numCells, fill='green')
                    elif isinstance(app.level.grid[row][col].contents, weapon):
                        #print('making weapon')
                        canvas.create_oval(cellStartX, cellStartY, cellStartX + app.width // numCells, cellStartY + app.width // numCells, fill='blue')
                    elif isinstance(app.level.grid[row][col].contents, projectile):
                        canvas.create_oval(cellStartX, cellStartY, cellStartX + app.width // numCells, cellStartY + app.width // numCells, fill='yellow')
            cellStartX += app.width // numCells
        cellStartY += app.height // numCells
        cellStartX = 0


def drawEnemies(app, canvas):
    pass

def drawLevel(app, canvas):
    drawMap(app, canvas)
    drawEnemies(app, canvas)
    drawPlayer(app, canvas)

def drawInventory(app, canvas):
    pass

def redrawAll(app, canvas):
    if app.gameStarted:
        if not app.isPaused:
            drawLevel(app, canvas)
        elif app.isPaused:
            drawInventory(app, canvas)


width = 600
height = 600

runApp(width=width, height=height)
