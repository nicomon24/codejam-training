import sys


def solve(C, F, X):
    r = 2
    t = X / r
    m = t + 1
    S = 0
    while t < m:
        m = t
        S += C / r
        r += F
        t = S + X / r
    return m

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

for i in range(N):
    line = input_rows[i+1].split(' ')
    x = solve(float(line[0]),float(line[1]),float(line[2]))
    output_file.write("Case #" + str(i+1) + ": " + str(x) + "\n")

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------


output_file.close()
