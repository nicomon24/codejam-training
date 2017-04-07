import sys, math

#sys.setrecursionlimit(10000)

if len(sys.argv) != 2:
    print "ERROR. Correct usage: python scipt.py file"
    sys.exit(0)

#Get the first parameter a.k.a. the input file
FILE_NAME = sys.argv[1]

#Read the file
input_file = open(FILE_NAME, 'r')
input_rows = list(input_file)

output_file = open('output3.txt', 'w')

# ----------------------------------
# Parsing input file to problem vars
# READ SINGLE INT: int(input_rows[])
# READ INT LIST: map(int, input_rows[].split(' '))
# ----------------------------------

def stepper(plates, step):
    moves = 0
    for val in plates:
        if val > step:
            moves += math.ceil(val/float(step)) -1
    return int(step + moves)

def solve(plates):
    res = []
    for i in range(1, max(plates)+1):
        res.append(stepper(plates, i))
    return min(res)

i = 0
n = int(input_rows[0])
for k in range(0,n):
    line = input_rows[2*k+2]
    i += 1
    plates = map(int, line.split(' '))
    x = solve(plates)
    print i
    print str(plates) + " => " + str(x)
    output_file.write("Case #" + str(i) + ": " + str(x) + "\n")

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------

output_file.close()
