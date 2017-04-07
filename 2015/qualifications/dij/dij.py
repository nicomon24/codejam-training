import sys

sys.setrecursionlimit(10000)

if len(sys.argv) != 2:
    print "ERROR. Correct usage: python scipt.py file"
    sys.exit(0)

#Get the first parameter a.k.a. the input file
FILE_NAME = sys.argv[1]

#Read the file
output_file = open('output.txt', 'w')
input_file = open(FILE_NAME, 'r')
input_rows = list(input_file)[1:]

# ----------------------------------
# Parsing input file to problem vars
# READ SINGLE INT: int(input_rows[])
# READ INT LIST: map(int, input_rows[].split(' '))
# ----------------------------------
# i=2, j=3, k=4

mul_mat = [[1,2,3,4],[2,-1,4,-3],[3,-4,-1,2],[4,3,-2,-1]]

def multiply(x1, x2):
    if x1 < 0:
        return -multiply(-x1,x2)
    if x2 < 0:
        return -multiply(x1,-x2)
    return mul_mat[x1-1][x2-1]

def condense(vect):
    if len(vect) <= 0:
        return 0
    elif len(vect) == 1:
        return vect[0]
    elif len(vect) == 2:
        return multiply(vect[0],vect[1])
    else:
        half = len(vect) / 2
        return multiply(condense(vect[:half]),condense(vect[half:]))

def convert(s):
    conv = {
        '1' : 1,
        'i' : 2,
        'j' : 3,
        'k' : 4
    }
    return conv[s]

def solve(vect):
    return solve_i(vect)

def solve_i(vect):
    print "Solving i for " + str(len(vect))
    if len(vect) <= 0:
        return 0
    curr = 1
    for index in range(0,len(vect)):
        curr = multiply(curr, vect[index])
        if curr == 2:
            if solve_j(vect[index+1:])==1:
                print "FIND I of len: " + str(len(vect[:index+1]))
                return 1
    return 0

def solve_j(vect):
    #print "Solving j for " + str(vect)
    if len(vect) <= 0:
        return 0
    curr = 1
    for index in range(0,len(vect)):
        curr = multiply(curr, vect[index])
        if curr == 3:
            y = solve_k(vect[index+1:])
            if y==1:
                print "FIND J of len: " + str(len(vect[:index+1]))
                return 1
    return 0

def solve_k(vect):
    #print "Solving k for " + str(vect)
    if len(vect) <= 0:
        return 0
    curr = 1
    for index in range(0,len(vect)):
        curr = multiply(curr, vect[index])
    if curr == 4:
        print "FIND K of len: " + str(len(vect))
        return 1
    return 0

c = 0
for i in range(0,len(input_rows), 2):
    c += 1
    x = int(input_rows[i].split(' ')[1])
    s = input_rows[i+1][:-1]
    complete = s * x
    comp_int = map(convert, complete)
    x = 0
    if condense(comp_int) == -1:
        x = solve(comp_int)
    b = 'YES'
    if x == 0:
        b = 'NO'
    print "Case #" + str(c) + ": " + str(b)
    output_file.write("Case #" + str(c) + ": " + str(b) + "\n")

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------


output_file.close()
