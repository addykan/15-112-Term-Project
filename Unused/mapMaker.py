import random
from objectData import *

# Make a 2D list of all the rooms, then connect them randomly and map them all to a grid with dimensions of the max sum of the lengths of the longest row of rooms and max sum of the heights of the
# tallest stack of rooms

# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

class room(object):
    def __init__(self, length, height, difficulty):
        self.length = length
        self.height = height
        self.items = self.getItemsInRoom(difficulty)

    def getItemsInRoom(self, difficulty):
        items = []
        weaponList = [Pistol, Rocket, Sword]
        for weapon in weaponList:
            if random.randint(1, 10) > difficulty:
                items.append(weapon(difficulty))
                break
        for i in range(difficulty):
            items.append(Enemy(difficulty))
        if random.randint(1, 10) > difficulty:  # No more hearts after level 10
            items.append(Heart(difficulty))
        return items


class level(object):
    tunnelDimensions = 5
    def __init__(self, difficulty):
        self.rooms = self.make2dListOfRooms(difficulty, difficulty, difficulty)
        self.connections = self.connectRooms(self.rooms)
        self.length = self.getLength(self.rooms)
        self.height = self.getHeight(self.rooms)

    # Make 2D list modified from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
    def make2dListOfRooms(self, rows, cols, difficulty):
        roomList = make2dList(rows, cols)
        for row in range(len(roomList)):
            for col in range(len(roomList[0])):
                roomList[row][col] = room(random.randint(1, 10), random.randint(1, 10), difficulty)
        return roomList
        #return [([room(random.randint(1, 10), random.randint(1, 10), difficulty)] * cols) for row in range(rows)]

    def connectRooms(self, rooms):
        connections = []
        rows = len(rooms)
        cols = len(rooms[0])
        for row in range(rows):
            for col in range(cols):
                if random.randint(1, 5) > 3 and row < rows - 1 and col < cols - 1:  # 40% chance of a connection between two rooms horizontally/vertically adjacent to each other
                    connections.append(((row, col), (row + 1, col)))
                if random.randint(1, 5) > 3 and row < rows - 1 and col < cols - 1:
                    connections.append(((row, col), (row, col + 1)))

        if random.randint(1, 2) == 2:  # Connect the final room to one of the adjacent rooms
            connections.append(((rows - 2, cols - 1), (rows - 1, cols - 1)))
        else:
            connections.append(((rows - 1, cols - 2), (rows - 1, cols -1)))

        if self.canTraverse(rooms, connections):  # Check if you can make it through the rooms - no optimal path necessary.
            return connections
        else:
            return self.connectRooms(rooms)  # If you can't make it through the rooms, make a new list of connections between rooms

    def canTraverse(self, rooms, connections, row = 0, col = 0):
        rows = len(rooms)
        cols = len(rooms[0])
        if row >= rows or col >= cols:
            return False
        if row == rows - 1 and col == cols - 1:  # If we're at the final room
            return True
        else:
            for drow in [0, 1]:
                for dcol in [0, 1]:
                    if (drow != 0 or dcol != 0) and ((row, col), (row + drow, col + dcol)) in connections:
                        return self.canTraverse(rooms, connections, row + drow, col + dcol)
            return False

    def getLength(self, rooms):
        maxLength = 0
        for row in rooms:
            rowLength = 0
            for room in row:
                rowLength += room.length
            if rowLength > maxLength:
                maxLength = rowLength
        #maxLength += level.tunnelDimensions * (len(rooms[0]) - 1)  # Account for the tunnels between rooms - 1 less tunnel than the number of rooms in a column, at most. Length of tunnel is set at 10
        return maxLength

    def getHeight(self, rooms):
        maxHeight = 0
        for col in range(len(rooms[0])):
            colHeight = 0
            for i in range(len(rooms)):
                colHeight += rooms[i][col].length
            if colHeight > maxHeight:
                maxHeight = colHeight
        #maxHeight += level.tunnelDimensions * (len(rooms) - 1)
        return maxHeight


class levelGrid(object):
    def __init__(self, level, player):
        self.roomGrid = self.getRoomGrid(level)
        self.itemGrid = self.placeItems(level, player)

    def getRoomGrid(self, level):
        buffer = 20  # Makes the grid larger than necessary to prevent index errors
        roomGrid = make2dList(level.height + buffer, level.length + buffer)
        #print(len(roomGrid), len(roomGrid[0]))
        currentRow = currentCol = 0
        for row in range(len(level.rooms)):
            for col in range(len(level.rooms[0])):  # Get down to each room
                for x in range(level.rooms[row][col].height):
                    for y in range(level.rooms[row][col].length):
                        #print(currentRow + x, currentCol + y)
                        roomGrid[currentRow + x][currentCol + y] = True
                        #print(x, y)
                currentCol += level.rooms[row][col].length  # + level.tunnelDimensions
            currentRow += level.rooms[row][col].height  # + level.tunnelDimensions
            currentCol = 0  # Reset back to left side
            #print(currentRow, currentCol)
        #self.connectRooms(level, roomGrid)
        return roomGrid

    def placeItems(self, level, player):  # Place items on the same grid as the room grid
        itemLocations = make2dList(len(self.roomGrid), len(self.roomGrid[0]))
        itemLocations[0][0] = player
        currentRow = currentCol = 0
        for row in range(len(level.rooms)):
            for col in range(len(level.rooms[0])):  # Get down to each room
                currentRowRange = level.rooms[row][col].height
                currentColRange = level.rooms[row][col].length
                for item in level.rooms[row][col].items:
                    itemRow = random.randint(currentRow, currentRow + currentRowRange)
                    itemCol = random.randint(currentCol, currentCol + currentColRange)
                    while itemLocations[itemRow][itemCol] != 0:
                        itemRow = random.randint(currentRow, currentRow + currentRowRange)
                        itemCol = random.randint(currentCol, currentCol + currentColRange)
                    itemLocations[itemRow][itemCol] = item
                currentCol += level.rooms[row][col].length
            currentRow += level.rooms[row][col].height
            currentCol = 0
        return itemLocations


                # itemGrid


# Taken from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html

def maxItemLength(a):
    maxLen = 0
    for row in range(len(a)):
        for col in range(len(a[row])):
            maxLen = max(maxLen, len(repr(a[row][col])))
    return maxLen

def print2dList(a):
    if a == []:
        print([])
        return
    print()
    rows, cols = len(a), len(a[0])
    maxCols = max([len(row) for row in a])
    fieldWidth = max(maxItemLength(a), len(f'col={maxCols-1}'))
    rowLabelSize = 5 + len(str(rows-1))
    rowPrefix = ' '*rowLabelSize+' '
    rowSeparator = rowPrefix + '|' + ('-'*(fieldWidth+3) + '|')*maxCols
    print(rowPrefix, end='  ')
    # Prints the column labels centered
    for col in range(maxCols):
        print(f'col={col}'.center(fieldWidth+2), end='  ')
    print('\n' + rowSeparator)
    for row in range(rows):
        # Prints the row labels
        print(f'row={row}'.center(rowLabelSize), end=' | ')
        # Prints each item of the row flushed-right but the same width
        for col in range(len(a[row])):
            print(repr(a[row][col]).center(fieldWidth+1), end=' | ')
        # Prints out missing cells in each column in case the list is ragged
        missingCellChar = chr(10006)
        for col in range(len(a[row]), maxCols):
            print(missingCellChar*(fieldWidth+1), end=' | ')
        print('\n' + rowSeparator)
    print()

level5 = level(5)

level5Grid = levelGrid(level5, Player('Mario'))

print2dList(level5Grid.roomGrid)

print2dList(level5Grid.itemGrid)

def checkObjectPositions(rooms, items):
    if len(rooms) == len(items) and len(rooms[0]) == len(items[0]):
        print('list dimensions equal')
    return True