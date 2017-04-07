import sys, operator
import numpy as np
from collections import defaultdict

# Put a mine in position (x,y) and update all neighbours
def putMine(m, x, y):
    mat = np.copy(m)
    if (mat[x,y]>=0):
        mat[x,y] = -1
        xmin = max(0, x-1)
        xmax = min(np.shape(mat)[0], x+2)
        ymin = max(0, y-1)
        ymax = min(np.shape(mat)[1], y+2)
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                if not (x==i and y==j) and mat[i,j] >= 0:
                    mat[i,j]+=1
    return mat

def fillBorder(m, depth):
    mat = np.copy(m)
    for i in range(0, np.shape(mat)[0]):
        mat = putMine(mat, i, depth)
    for j in range(0, np.shape(mat)[1]):
        mat = putMine(mat, depth, j)
    return mat

def fillCol(m , depth):
    mat = np.copy(m)
    for i in range(0, np.shape(mat)[0]):
        mat = putMine(mat, i, depth)
    return mat

def fillRow(m , depth):
    mat = np.copy(m)
    for i in range(0, np.shape(mat)[1]):
        mat = putMine(mat, depth, i)
    return mat

def exploding(mat):
    mines = len(np.where(mat == -1)[0])
    cell_count = np.shape(mat)[0] * np.shape(mat)[1]
    if (mines + 1 == cell_count):
        return True
    cells = []
    zeros = []
    idx = np.where(mat==0)
    if len(idx[0])>0 and len(idx[1])>0:
        zeros.append((idx[0][0], idx[1][0]))
    else:
        return False
    # Get neighbours cells
    for cell in zeros:
        xmin = max(0, cell[0]-1)
        xmax = min(np.shape(mat)[0], cell[0]+2)
        ymin = max(0, cell[1]-1)
        ymax = min(np.shape(mat)[1], cell[1]+2)
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                if not (cell[0]==i and cell[1]==j):
                    if mat[i,j] > 0 and (i,j) not in cells:
                        cells.append((i,j))
                    elif mat[i,j] == 0 and (i,j) not in zeros:
                        zeros.append((i,j))
    return ((cell_count - mines) == (len(cells) + len(zeros)))

def prettyPrint(mat):
    if mat is None:
        return "Impossible\n"
    text = ""
    idx = np.where(mat==0)
    if len(idx[0])<=0 or len(idx[1])<=0:
        # Check if exploding anyway
        if exploding(mat):
            idx = np.where(mat>=0)
        else:
            return "Impossible\n"
    fzero = (idx[0][0], idx[1][0])
    for i in range(0,np.shape(mat)[0]):
        for j in range(0,np.shape(mat)[1]):
            if i==fzero[0] and j==fzero[1]:
                text += "c"
            elif mat[i,j]>=0:
                text += "."
            else:
                text += "*"
        text += "\n"
    return text

def isRowComplete(mat, row):
    if np.shape(mat)[0] <= row:
        return False
    for cell in mat[row, :]:
        if cell != -1:
            return False
    return True

def isColComplete(mat, col):
    if np.shape(mat)[1] <= col:
        return False
    for cell in mat[:, col]:
        if cell != -1:
            return False
    return True

def tryAllMinesSmart(mat, mines, tresx=0, tresy=0):
    #print("\n++++++++++++++++\n\nElaborating", mines, tresx, tresy)
    #print(prettyPrint(mat))
    #sys.stdin.readline()
    if mines <= 0:
        if exploding(mat):
            return mat
        else:
            return None
    # Check border
    Rt = np.shape(mat)[0] - tresx
    Ct = np.shape(mat)[1] - tresy
    maxborder = max(Rt, Ct)
    if maxborder == Rt:
        # The shape[0] (n of rows) is bigger than n of cols
        # Check if we can remove first col
        if (mines > Ct):
            return tryAllMinesSmart(fillRow(mat, tresx), mines-Ct, tresx+1, tresy)
    else:
        # The shape[1] (n of cols) is bigger than n of rows
        if (mines > Rt):
            return tryAllMinesSmart(fillCol(mat, tresy), mines-Rt, tresx, tresy+1)
    '''
    border = np.shape(mat)[0] - tresx + np.shape(mat)[1] - tresy -1
    if mines > border and tresx==tresy and tresx < min(np.shape(mat))-2:
        return tryAllMinesSmart(fillBorder(mat,tresx), mines-border, tresx+1, tresy+1)
    '''
    # Check first cell
    if mat[tresx,tresy] >= 0:
        return tryAllMinesSmart(putMine(mat, tresx, tresy), mines-1, tresx, tresy)
    # Check row
    for j in range(0,np.shape(mat)[1]):
        if mat[tresx,j]>=0 and mat[tresx,j-1]==-1:
            nm = putMine(mat, tresx, j)
            if isRowComplete(nm, tresx):
                if isColComplete(nm, tresx):
                    return tryAllMinesSmart(nm, mines-1, tresx+1, tresy)
                b = tryAllMinesSmart(nm, mines-1, tresx+1, tresy)
                if not b is None:
                    return b
            else:
                b = tryAllMinesSmart(nm, mines-1, tresx, tresy)
                if not b is None:
                    return b
    # Check col
    for i in range(0,np.shape(mat)[0]):
        if mat[i, tresy]>=0 and mat[i-1, tresy]==-1:
            nm = putMine(mat, i, tresy)
            if isColComplete(nm, tresy):
                if isRowComplete(nm, tresy):
                    return tryAllMinesSmart(nm, mines-1, tresx, tresy+1)
                b = tryAllMinesSmart(nm, mines-1, tresx, tresy+1)
                if not b is None:
                    return b
            else:
                b = tryAllMinesSmart(nm, mines-1, tresx, tresy)
                if not b is None:
                    return b
    return None

def tryAllMines(mat, mines):
    if mines <= 0:
        if exploding(mat):
            return mat
        else:
            return None
    for j in range(0,np.shape(mat)[1]):
        for i in range(0,np.shape(mat)[0]):
            if mat[i,j]>=0:
                b = tryAllMines(putMine(mat, i, j), mines-1)
                if not b is None:
                    return b
    return None

def solve(R,C,M):
    print("Solving:",R,C,M)
    if (R*C == M):
        return None
    mat = np.zeros((R,C))
    if M<=0:
        return mat
    return tryAllMinesSmart(mat, M)

'''
ALGO:
    start with the upper-left corner
    expand down till 2 cell to end
    expand right from corner till 2 cell to end
    put a mine in the lower-right corner if possible (R>=4 and C>=4 ?)
    remove previous and put 2 mines to complete an edge
    other mine in the corner?
    remove previous and put 2 mines to complete edge
    repeat on sub-field

    3x5:
    1:
    *....
    .....
    .....
    2:
    *....
    .....
    ....*


'''

#print(prettyPrint(solve(5,5,19)))

if len(sys.argv) != 2:
    print("ERROR. Correct usage: python scipt.py file")
    sys.exit(0)

#Get the first parameter a.k.a. the input file
FILE_NAME = sys.argv[1]

#Read the file
output_file = open('output.txt', 'w')
input_file = open(FILE_NAME, 'r')
input_rows = list(input_file)

# ----------------------------------
# Parsing input file to problem vars
# READ SINGLE INT: int(input_rows[])
# READ INT LIST: map(int, input_rows[].split(' '))
# ----------------------------------

N = int(input_rows[0])
for i in range(0,N):
    print("Test", i+1)
    line = input_rows[i+1].split(' ')
    x = solve(int(line[0]),int(line[1]),int(line[2]))
    output_file.write("Case #" + str(i+1) + ":\n")
    if x is None:
        output_file.write("Impossible\n")
    else:
        output_file.write(prettyPrint(x))

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------
output_file.close()
