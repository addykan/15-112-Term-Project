from primMapMaker import *
from cmu_112_graphics import *

def appStarted(app):
    app.isPaused = True
    app.startScreen = True
    app.gameStarted = False
    app.inInventory = False
    app.difficulty = 15
    app.level = level(app.difficulty)
    app.Player = Player('Link', app.difficulty)
    app.level.grid[0][0].contents = app.Player
    app.screenBounds = 5  # This many cells are rendered on all sides of the player - so 4 * 2 + player cell = 4 * 2 + 1 = 9x9 grid
    app.currentCenter = [0, 0]
    app.lastDir = None  # Used for determining which direction to fire weapons in
    app.onWeapon = False  # Standing on weapon
    app.enemyCount = app.difficulty
    app.timerDelay = 500
    app.gameOver = False
    app.frameCount = 0
    app.score = 0
    app.controlsText = 'Controls:\nPress r to reset\nUse wasd to move\nPress space to fire weapon or use sword\nPress tab to swap weapons\nPress x to drop active weapon\nPress Enter to pick up new ' \
                   'weapon\nPress p to pause and unpause\nPress n to skip to next level'

    # Image stuff
    app.goomba = app.loadImage(Enemy.path)
    app.scaledGoomba = app.scaleImage(app.goomba, 0.05)
    app.link = app.loadImage(app.Player.path)
    app.scaledLink = app.scaleImage(app.link, 0.15)
    app.Heart = app.loadImage(Heart.path)
    app.scaledHeart = app.scaleImage(app.Heart, 0.1)

def nextLevel(app):  # Maintains a lot of existing data, but primarily generates a new level
    app.score += app.difficulty ** 2
    app.difficulty += 5
    app.level = level(app.difficulty)
    app.level.grid[0][0].contents = app.Player
    app.currentCenter = [0, 0]
    app.lastDir = None
    app.onWeapon = False
    app.enemyCount = app.difficulty
    if app.screenBounds > 3:  # Constrict the camera to make it harder to see what the maze looks like
        app.screenBounds -= 1
    if app.timerDelay > 100:
        app.timerDelay -= 50  # Make everything faster

def keyPressed(app, event):
    if event.key == 'r':  # Reset
        appStarted(app)
    if app.startScreen:  # Start game
        app.gameStarted = True
        app.isPaused = False
        app.startScreen = False
    if app.gameStarted:
        if event.key == 'p':
            app.isPaused = not app.isPaused
        elif event.key == 'x':  # Drop active Weapon
            app.Player.gear = app.Player.gear[1:]
            app.Player.activeWeapon = app.Player.gear[0]
        elif event.key == 'n':
            nextLevel(app)
        elif not app.isPaused:
            if event.key in 'wasd':  # Movement
                app.lastDir = event.key
                if event.key == 'w':
                    movePlayer(app, -1, 0)  # drow, dcol - checking happens in the function itself
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


def killEnemy(app):  # Keeps track of enemies and moves to the next level as necessary
    app.enemyCount -= 1
    app.score += app.difficulty
    if app.enemyCount == 0:
        nextLevel(app)


def swapWeapons(app):  # Allows player to rotate between stored weapons on demand by pressing Tab
    if len(app.Player.gear) > 1:
        app.Player.gear = app.Player.gear[1:] + [app.Player.gear[0]]
        app.Player.activeWeapon = app.Player.gear[0]


def pickUpWeapon(app):
    if isinstance(app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents, Weapon):
        if len(app.Player.gear) < 5:
            app.Player.gear.append(app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents)
            app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = None
            lastCells = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}
            app.level.grid[app.currentCenter[0] + lastCells[app.lastDir][0]][app.currentCenter[1] + lastCells[app.lastDir][1]].contents = None  # Remove the player from the cell they were in before


def movePlayer(app, drow, dcol):
    if not isInGrid(app, app.currentCenter[0] + drow, app.currentCenter[1] + dcol):
        return
    if app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].status:  # If it's a tunnel where an object can be
        if app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents is None:
            app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents = app.Player  # Place the Player in the new location
            if not app.onWeapon:
                app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = None  # Clear the old location
            app.currentCenter[0] += drow  # Move the camera and stored location of Player
            app.currentCenter[1] += dcol
            app.onWeapon = False
        elif isinstance(app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents, Heart):  # If there's a Heart in the cell Player wants to move into
            if app.Player.health < 100:  # Automatically pick up Heart if health is not full
                app.Player.health += app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents.health
                if app.Player.health > 100:
                    app.Player.health = 100
            app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents = app.Player  # Place the Player in the new location
            if not app.onWeapon:
                app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = None  # Clear the old location
            app.currentCenter[0] += drow  # Move the camera and stored location of Player
            app.currentCenter[1] += dcol
            app.onWeapon = False
        elif isinstance(app.level.grid[app.currentCenter[0] + drow][app.currentCenter[1] + dcol].contents, Weapon):
            app.onWeapon = True
            app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = None  # Clear the old location
            app.currentCenter[0] += drow  # Move the camera and stored location of Player
            app.currentCenter[1] += dcol


def isInGrid(app, row, col):
    rows = len(app.level.grid)
    cols = len(app.level.grid[0])
    return row >= 0 and col >= 0 and row < rows and col < cols


def useWeapon(app):
    projectileDirs = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}
    app.Player.activeWeapon.ammo -= 1
    if app.lastDir is not None and isInGrid(app, app.currentCenter[0] + projectileDirs[app.lastDir][0], app.currentCenter[1] + projectileDirs[app.lastDir][1]):  # Uses the last move player made to
        # determine direction to fire in
        if app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].status:
            if app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents is None and not isinstance(
                    app.Player.activeWeapon, Sword): # Swords can't make projectiles, only pistols and swords
                app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents = Projectile(projectileDirs[app.lastDir][0],
                                                                                                                                                                   projectileDirs[app.lastDir][1],
                                                                                                                                                                   app.Player.activeWeapon.damage,
                                                                                                                                                                   app.Player.activeWeapon.travelSpeed)
                # Projectiles are initialized with a direction, damage, and velocity, and stored in the cell - they get moved each time the timer fires
            elif isinstance(app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents, Enemy):
                # Point blank damage - all weapons can use this method, but swords can't use projectiles
                app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents.health -= app.Player.activeWeapon.damage
                if app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents.health <= 0:
                    app.level.grid[app.currentCenter[0] + projectileDirs[app.lastDir][0]][app.currentCenter[1] + projectileDirs[app.lastDir][1]].contents = None
                    killEnemy(app)
    if app.Player.activeWeapon.ammo <= 0:
        app.Player.gear = app.Player.gear[1:]
        if app.Player.gear == []:
            app.gameOver = True
        else:
            app.Player.activeWeapon = app.Player.gear[0]

def moveProjectiles(app):
    for row in range(len(app.level.grid)):
        for col in range(len(app.level.grid[0])):
            if isinstance(app.level.grid[row][col].contents, Projectile) and app.level.grid[row][col].contents.Enemy == False:
                moveProjectile(app, row, col)
            elif isinstance(app.level.grid[row][col].contents, Projectile) and app.level.grid[row][col].contents.Enemy == True:
                moveEnemyProjectile(app, row, col)

def moveProjectile(app, row, col):
    for _ in range(app.level.grid[row][col].contents.speed):  # Move it 1 unit in given direction for as many times as speed
        drow = app.level.grid[row][col].contents.drow
        dcol = app.level.grid[row][col].contents.dcol
        if isInGrid(app, row+drow, col+dcol):  # Check if it's in the grid
            if app.level.grid[row+drow][col+dcol].status:  # Check if it's not a wall
                if isinstance(app.level.grid[row+drow][col+dcol].contents, Enemy) and app.level.grid[row][col].contents.Enemy is False:  # If we hit an Enemy and if it's a player projectile
                    app.level.grid[row + drow][col + dcol].contents.health -= app.level.grid[row][col].contents.damage
                    if app.level.grid[row + drow][col + dcol].contents.health <= 0:
                        app.level.grid[row + drow][col + dcol].contents = None
                        killEnemy(app)
                elif app.level.grid[row+drow][col+dcol].contents is None:
                    app.level.grid[row + drow][col + dcol].contents = app.level.grid[row][col].contents
    app.level.grid[row][col].contents = None

def moveEnemyProjectile(app, row, col):
    for _ in range(app.level.grid[row][col].contents.speed):
        drow = app.level.grid[row][col].contents.drow
        dcol = app.level.grid[row][col].contents.dcol
        if isInGrid(app, row+drow, col + dcol):
            if app.level.grid[row + drow][col + dcol].status:  # Check if it's not a wall
                if [row+drow, col+dcol] == app.currentCenter:  # If we hit the Player
                    app.Player.health -= app.level.grid[row][col].contents.damage
                    if app.Player.health <= 0:
                        app.gameOver = True
                elif app.level.grid[row + drow][col + dcol].contents is None:
                    app.level.grid[row + drow][col + dcol].contents = app.level.grid[row][col].contents
    app.level.grid[row][col].contents = None

def checkProjectiles(app):  # Sometimes projectiles appear in the same cell as the player but are not calculated - this stops that from happening
    if isinstance(app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents, Projectile):
        app.player.health -= app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents.damage
        app.level.grid[app.currentCenter[0]][app.currentCenter[1]].contents = None

def moveEnemy(app, location, direction, first = True):  # Try moving Enemy in the prescribed direction but if it doesn't work, move it in a different direction instead - no stationary enemies
    newRow = int(location[0] + direction[0])
    newCol = int(location[1] + direction[1])
    if isInGrid(app, newRow, newCol) and app.level.grid[newRow][newCol].contents is None and app.level.grid[newRow][newCol].status: # check if new position is none, then move it
        app.level.grid[newRow][newCol].contents, app.level.grid[location[0]][location[1]].contents = app.level.grid[location[0]][location[1]].contents, app.level.grid[newRow][newCol].contents
        return True
    elif first == True:
        for dir in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if moveEnemy(app, location, dir, first = False) == True:
                break

def moveEnemies(app):
    for row in range(len(app.level.grid)):
        for col in range(len(app.level.grid[0])):
            if isinstance(app.level.grid[row][col].contents, Enemy):
                drow = app.currentCenter[0] - row
                dcol = app.currentCenter[1] - col
                if abs(drow) >= abs(dcol):  # If vertical distance is greater than horizontal distance
                    moveEnemy(app, (row, col), (drow//(abs(drow)), 0))
                else:
                    moveEnemy(app, (row, col), (0, dcol//(abs(dcol))))

def enemyAttack(app):
    for row in range(len(app.level.grid)):
        for col in range(len(app.level.grid[0])):
            if isinstance(app.level.grid[row][col].contents, Enemy):  # The rest of these if statements define the direction to fire the projectile in
                if row == app.currentCenter[0]:
                    if app.currentCenter[1] < col:
                        if app.level.grid[row][col-1].status and isInGrid(app, row, col-1):
                            app.level.grid[row][col - 1].contents = Projectile(0, -1, app.difficulty, 1, player=False)
                    elif app.currentCenter[1] > col:
                        if app.level.grid[row][col + 1].status and isInGrid(app, row, col+1):
                            app.level.grid[row][col + 1].contents = Projectile(0, 1, app.difficulty, 1, player=False)
                elif col == app.currentCenter[0]:
                    if app.currentCenter[0] < row:
                        if app.level.grid[row-1][col].status and isInGrid(app, row-1, col):
                            app.level.grid[row][col].contents = Projectile(-1, 0, app.difficulty, 1, player=False)
                    elif app.currentCenter[0] > row:
                        if app.level.grid[row+1][col].status and isInGrid(app, row+1, col):
                            app.level.grid[row+1][col].contents = Projectile(1, 0, app.difficulty, 1, player=False)


def countEnemies(app):  # Just in case there's a logic error earlier that doesn't trigger the next level, check it again here too
    enemyCount = 0
    for row in range(len(app.level.grid)):
        for col in range(len(app.level.grid[0])):
            if isinstance(app.level.grid[row][col].contents, Enemy):
                enemyCount += 1
    if enemyCount == 0:
        nextLevel(app)


def takeStep(app):
    moveEnemies(app)
    moveProjectiles(app)
    checkProjectiles(app)
    enemyAttack(app)
    app.frameCount += 1
    countEnemies(app)
    if app.Player.health <= 0:
        app.gameOver = True


def timerFired(app):
    if not app.isPaused:
        takeStep(app)







'''
Rendering
'''


def drawPlayer(app, canvas):  # Draw player and their equipped weapon
    canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.scaledLink))
    if isinstance(app.Player.activeWeapon, Pistol):
        drawPistol(app, canvas, app.width // 2, app.height // 2, int(0.9 * app.width//len(app.level.grid[0])), app.Player.activeWeapon, player = True)
    elif isinstance(app.Player.activeWeapon, Sword):
        drawSword(app, canvas, app.width // 2, app.height // 2, int(0.9 * app.width//len(app.level.grid[0])), app.Player.activeWeapon, player = True)
    elif isinstance(app.Player.activeWeapon, Rocket):
        drawRocket(app, canvas, app.width // 2, app.height // 2, int(0.9 * app.width//len(app.level.grid[0])), app.Player.activeWeapon, player = True)


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
    for row in range(minRow, maxRow + 1):  # Go through the map, draw a cell, draw the contents of the cell
        for col in range(minCol, maxCol + 1):
            if (row < 0 or col < 0 or row >= len(app.level.grid) or col >= len(app.level.grid[0])) or not app.level.grid[row][col].status:  # Outside the grid, or a wall
                canvas.create_rectangle(cellStartX, cellStartY, cellStartX + app.width // numCells, cellStartY + app.width // numCells, fill = 'black')
            else:  # In the grid, not a wall
                canvas.create_rectangle(cellStartX, cellStartY, cellStartX + app.width // numCells, cellStartY + app.width // numCells, fill='white')
                if app.level.grid[row][col].contents != None:  # Draw an object in the cell - Enemy, powerup, or Weapon
                    if isinstance(app.level.grid[row][col].contents, Enemy):
                        drawEnemy(app, canvas, cellStartX, cellStartY, app.width//numCells, app.level.grid[row][col].contents)
                    elif isinstance(app.level.grid[row][col].contents, Heart):
                        canvas.create_image(cellStartX + int(0.5*(app.width//numCells)), cellStartY + int(0.5*(app.height//numCells)), image=ImageTk.PhotoImage(app.scaledHeart))
                    elif isinstance(app.level.grid[row][col].contents, Weapon):
                        if isinstance(app.level.grid[row][col].contents, Pistol):
                            drawPistol(app, canvas, cellStartX, cellStartY, app.width//numCells, app.level.grid[row][col].contents)
                        elif isinstance(app.level.grid[row][col].contents, Rocket):
                            drawRocket(app, canvas, cellStartX, cellStartY, app.width // numCells, app.level.grid[row][col].contents)
                        elif isinstance(app.level.grid[row][col].contents, Sword):
                            drawSword(app, canvas, cellStartX, cellStartY, app.width // numCells, app.level.grid[row][col].contents)
                    elif isinstance(app.level.grid[row][col].contents, Projectile):
                        canvas.create_oval(cellStartX + (0.05 * (app.width//numCells)), cellStartY + (0.05 * (app.height//numCells)), cellStartX + (0.9 * app.width // numCells),
                                           cellStartY + (0.9 * (app.width // numCells)), fill='yellow')
            cellStartX += app.width // numCells
        cellStartY += app.height // numCells
        cellStartX = 0


def drawLevel(app, canvas):
    drawMap(app, canvas)
    drawPlayer(app, canvas)
    drawUI(app, canvas)

def drawUI(app, canvas):  # Draw the health bar in the corner
    healthBarLength = 0.2 * app.width
    healthProportion = app.Player.health / 100
    canvas.create_rectangle(0, app.height//20, healthBarLength, app.height//10, fill = 'white')
    canvas.create_rectangle(0, app.height // 20, int(healthBarLength * healthProportion), app.height // 10, fill='green')
    canvas.create_text(healthBarLength // 2, int(3/40 * app.height), text=f'{app.Player.health}', font='Helvetica 15 bold')

def drawInventory(app, canvas):  # Inventory/Pause menu
    margin = app.width // 16
    iconStartX = margin
    iconStartY = app.height//3
    side = 2 * (app.width // 16)
    canvas.create_text(app.width//2, app.height//6, text='Top number: Ammo\nBottom number: Damage', font = 'Helvetica 20 bold')
    canvas.create_text(app.width//2, app.height//4, text=f'Current Score: {app.score}', font='Helvetica 15 bold')
    for weapon in app.Player.gear:
        canvas.create_rectangle(iconStartX, iconStartY, iconStartX + side, iconStartY + side)
        if isinstance(weapon, Pistol):
            drawPistol(app, canvas, iconStartX, iconStartY, side, weapon)
        elif isinstance(weapon, Rocket):
            drawRocket(app, canvas, iconStartX, iconStartY, side, weapon)
        elif isinstance(weapon, Sword):
            drawSword(app, canvas, iconStartX, iconStartY, side, weapon)
        iconStartX += side + margin
    canvas.create_text(app.width//2, int(app.height * (5/6)), text=app.controlsText, font = 'Helvetica 12 bold')

def drawPistol(app, canvas, iconStartX, iconStartY, side, weapon, player = False):
    canvas.create_line(iconStartX + int(0.2*side), iconStartY + (int(0.3*side)), iconStartX + int(0.2*side), iconStartY + (int(0.8*side)))
    canvas.create_rectangle(iconStartX + int(0.2*side), iconStartY + (int(0.3*side)), iconStartX + int(0.8*side), iconStartY + (int(0.5*side)), fill='black')
    if not player:  # Only show ammo when in inventory - clogs up the screen during gameplay
        canvas.create_text(iconStartX + int(0.6*side), iconStartY + (int(0.75*side)),text=f'{weapon.ammo}\n{weapon.damage}', font='Helvetica 10 bold')

def drawRocket(app, canvas, iconStartX, iconStartY, side, weapon, player = False):
    canvas.create_oval(iconStartX + int(0.3*side), iconStartY + int(0.2*side), iconStartX + int(0.5*side), iconStartY + int(0.4*side), fill='red')
    canvas.create_rectangle(iconStartX+int(0.3*side), iconStartY + int(0.3*side), iconStartX + int(0.5*side), iconStartY + int(0.8*side), fill='red')
    if not player:
        canvas.create_text(iconStartX + int(0.8 * side), iconStartY + (int(0.7 * side)), text=f'{weapon.ammo}\n{weapon.damage}', font='Helvetica 10 bold')


def drawSword(app, canvas, iconStartX, iconStartY, side, weapon, player = False):
    canvas.create_line(iconStartX + int(0.3*side), iconStartY + int(0.2*side), iconStartX + int(0.2*side), iconStartY + int(0.3*side), fill='black')  # Is there a polygon command?
    canvas.create_line(iconStartX + int(0.3*side), iconStartY + int(0.2*side), iconStartX + int(0.4*side), iconStartY + int(0.3*side), fill='black')
    canvas.create_rectangle(iconStartX + int(0.2*side), iconStartY + int(0.3 * side), iconStartX + int(0.4*side), iconStartY + int(0.9*side), fill='black')
    canvas.create_rectangle(iconStartX + int(0.1*side), iconStartY + int(0.7*side), iconStartX + int(0.5*side), iconStartY + int(0.8*side), fill='black')
    if not player:
        canvas.create_text(iconStartX + int(0.8 * side), iconStartY + (int(0.7 * side)), text=f'{weapon.ammo}\n{weapon.damage}', font='Helvetica 10 bold')

def drawEnemy(app, canvas, startX, startY, side, enemy):
    endX = startX + side
    endY = startY + side
    midX = startX + side//2
    midY = startY + side//2
    canvas.create_image(midX, midY, image=ImageTk.PhotoImage(app.scaledGoomba))
    canvas.create_text(endX - int(0.2*side), endY -int(0.1*side), text = f'{enemy.health}', font='Helvetica 10 bold')

def drawSplashScreen(app, canvas):
    canvas.create_text(app.width//2, app.height//5, text='Primrunner', font = 'Helvetica 30 bold')
    canvas.create_text(app.width//2, app.height//4, text='Adhvik Kanagala F20', font='Helvetica 12 bold')
    canvas.create_text(app.width//2, app.height//3, text = 'Press any key to start', font = 'Helvetica 15 bold')
    canvas.create_text(app.width//2, int(2/3 * app.height), text = app.controlsText, font = 'Helvetica 15 bold')


def drawGameOver(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text='Game Over :( Good run!', font='Helvetica 20 bold')
    canvas.create_text(app.width // 2, int(app.height * 2/3), text=f'Score: {app.score}', font='Helvetica 20 bold')

def redrawAll(app, canvas):
    if app.gameStarted and not app.gameOver:
        if not app.isPaused:
            drawLevel(app, canvas)
        elif app.isPaused:
            drawInventory(app, canvas)
    elif app.gameOver:
        drawGameOver(app, canvas)
    else:
        drawSplashScreen(app, canvas)


width = 600
height = 600

runApp(width=width, height=height)

