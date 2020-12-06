from objectData import *
import math, random


# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
def make2dList(rows, cols):
    return [([0] * cols) for row in range(rows)]

class cell(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.adjacentCells = {(row - 1, col), (row + 1, col), (row, col + 1), (row, col - 1)}
        self.contents = None
        self.status = False  # True if it is a passage/tunnel, false if it is a wall

class level(object):
    def __init__(self, difficulty):
        self.grid = self.make2dListofCells(difficulty, difficulty)
        self.convertToMaze(self.grid)
        self.cellStatus = self.testCells(self.grid)
        self.fillCells(self.grid)

    def make2dListofCells(self, rows, cols):
        grid = make2dList(rows, cols)
        for row in range(rows):
            for col in range(cols):
                grid[row][col] = cell(row, col)
                if row == 0:  # Remove adjacent cells not present in the grid
                    grid[row][col].adjacentCells.remove((row - 1, col))
                if col == 0:
                    grid[row][col].adjacentCells.remove((row, col - 1))
                if rows + 1 == rows:
                    grid[row][col].adjacentCells.remove((row + 1, col))
                if cols + 1 == cols:
                    grid[row][col].adjacentCells.remove((row, col + 1))
        return grid

    # Theoretical information from https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm
    # More general theoretical information from https://en.wikipedia.org/wiki/Prim%27s_algorithm
    # 2-cell frontier idea from https://stackoverflow.com/questions/29739751/implementing-a-randomly-generated-maze-using-prims-algorithm
    # 1-cell frontier is possible, but the mazes it generates do not look as nice (see second image at the top of the stack overflow link)
    # Swapped to entirely using cells without walls because it would also make it graphically easier to render without losing the complexity of the maze generator in the process
    # Easier to store both cells AND walls as cells in a grid, rather than storing the walls of the grid in a separate data format

    def convertToMaze(self, grid):
        startCellRow = 0  # random.randint(0, len(grid) - 1)
        startCellCol = 0  # random.randint(0, len(grid[0]) - 1)
        grid[startCellRow][startCellCol].status = True  # Always start from top left corner - doesn't really change the algorithm, but makes character placement later
        #print('start', startCellRow, startCellCol)
        frontierCells = set()
        neighbors = self.getNeighbors(grid, startCellRow, startCellCol, False)
        for neighbor in neighbors:
            frontierCells.add(neighbor)
        while len(frontierCells) > 0:
            frontierList = list(frontierCells)  # Slightly inefficient but easiest way to get a random element while maintaining set properties
            nextCell = frontierList[random.randint(0, len(frontierList) - 1)]
            nextCellPassages = self.getNeighbors(grid, nextCell[0], nextCell[1], True) # Need to figure out why it's picking a cell that has no frontiers that are currently passages
            #print('len of next cell passages', len(nextCellPassages))
            #print(nextCellPassages)
            passage = nextCellPassages[random.randint(0, len(nextCellPassages) - 1)]
            middleCellRow = (nextCell[0] + passage[0]) // 2
            middleCellCol = (nextCell[1] + passage[1]) // 2
            #print(f'MiddleCells: {middleCellRow}, {middleCellCol}')
            grid[middleCellRow][middleCellCol].status = True
            grid[nextCell[0]][nextCell[1]].status = True
            frontierCellNeighbors = self.getNeighbors(grid, nextCell[0], nextCell[1], False)  # Swapping to middleCell might work, need to write a quick print2DList function to verify using T/F
            # states of each cell
            for neighbor in frontierCellNeighbors:
                frontierCells.add(neighbor)
            frontierCells.remove(nextCell)
            #print(frontierCells)

    def getNeighbors(self, grid, row, col, cellType):
        neighbors = []
        rows = len(grid)
        cols = len(grid[0])
        for drow in [-2, 0, 2]:
            for dcol in [-2, 0, 2]:
                if row + drow >= 0 and row + drow < rows and col + dcol >= 0 and col + dcol < cols and (drow == 0 or dcol == 0):
                    # If it's in the grid, if it's 2 cells in any of the compass directions
                    if cellType == grid[row + drow][col + dcol].status:  # If it matches the type of cell we want - false for walls, true for passages
                        neighbors.append((row + drow, col + dcol))
        return neighbors

    def testCells(self, grid):
        cells = make2dList(len(grid), len(grid[0]))
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                cells[row][col] = grid[row][col].status

        return cells

    def fillCells(self, grid):
        enemyCountToPlace = len(grid)
        heartCountToPlace = len(grid) // 10
        weaponCountToPlace = len(grid) // 5
        weaponList = [pistol, rocket, sword]
        self.placeObjects(grid, enemy, enemyCountToPlace)
        self.placeObjects(grid, heart, heartCountToPlace)
        self.placeObjects(grid, weaponList, weaponCountToPlace)


    def placeObjects(self, grid, entity, entityCount):
        while entityCount > 0:  # Keep randomly placing enemies in cells
            cellRow = random.randint(1, len(grid) - 1)
            cellCol = random.randint(1, len(grid) - 1)
            if grid[cellRow][cellCol].contents is None and grid[cellRow][cellCol].status:
                if entity is enemy:
                    grid[cellRow][cellCol].contents = entity('Stormtrooper', len(grid))
                elif entity is heart:
                    grid[cellRow][cellCol].contents = entity(len(grid))
                elif isinstance(entity, list):
                    grid[cellRow][cellCol].contents = entity[random.randint(0, len(entity)-1)](len(grid))
                entityCount -= 1


#level5 = level(20)  # Able to make a map that can be traversed
#print2dList(level5.cellStatus)

