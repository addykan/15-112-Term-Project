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

    '''
    Pick a random Cell, set it to state Passage and Compute its frontier cells. A frontier cell of a Cell is a cell with distance 2 in state Blocked and within the grid.
    While the list of frontier cells is not empty:
    Pick a random frontier cell from the list of frontier cells.
    Let neighbors(frontierCell) = All cells in distance 2 in state Passage. Pick a random neighbor and connect the frontier cell with the neighbor by setting the cell in-between to state Passage. 
    Compute the frontier cells of the chosen frontier cell and add them to the frontier list. Remove the chosen frontier cell from the list of frontier cells.
    '''
    def convertToMaze(self, grid):
        startCellRow = random.randint(0, len(grid) - 1)
        startCellCol = random.randint(0, len(grid[0]) - 1)
        grid[startCellRow][startCellCol].status = True # Randomly set the cell to begin the algorithm from
        print('start', startCellRow, startCellCol)
        frontierCells = set()
        neighbors = self.getNeighbors(grid, startCellRow, startCellCol, False)
        for neighbor in neighbors:
            frontierCells.add(neighbor)
        while len(frontierCells) > 0:
            frontierList = list(frontierCells)  # Slightly inefficient but easiest way to get a random element while maintaining set properties
            nextCell = frontierList[random.randint(0, len(frontierList) - 1)]
            nextCellPassages = self.getNeighbors(grid, nextCell[0], nextCell[1], True) # Need to figure out why it's picking a cell that has no frontiers that are currently passages
            #print(len(nextCellPassages))
            print(nextCellPassages)
            passage = nextCellPassages[random.randint(0, len(nextCellPassages) - 1)]
            middleCellRow = (nextCell[0] + passage[0]) // 2
            middleCellCol = (nextCell[1] + passage[1]) // 2
            print(f'MiddleCells: {middleCellRow}, {middleCellCol}')
            grid[middleCellRow][middleCellCol].status = True
            frontierCellNeighbors = self.getNeighbors(grid, middleCellRow, middleCellCol, False)  # Swapping to middleCell might work, need to write a quick print2DList function to verify using T/F
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

# {(26, 11), (28, 13), (26, 15)}
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

level5 = level(50)
print2dList(level5.grid)