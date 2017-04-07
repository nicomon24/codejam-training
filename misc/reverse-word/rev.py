import sys

if len(sys.argv) != 2:
    print "ERROR. Correct usage: python scipt.py file"
    sys.exit(0)

#Get the first parameter a.k.a. the input file
FILE_NAME = sys.argv[1]

#Read the file
input_file = open(FILE_NAME, 'r')
input_rows = list(input_file)

# ----------------------------------
# Parsing input file to problem vars
# READ SINGLE INT: int(input_rows[])
# READ INT LIST: map(int, input_rows[].split(' '))
# ----------------------------------
N = int(input_rows[0])

# -------------
# Solve problem
# -------------

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------
output_file = open('output.txt', 'w')
for i in range(0,N):
    line = input_rows[i+1]
    words = line[:-1].split(' ')
    output_file.write("Case #" + str(i+1) + ": " + " ".join(words[::-1]) + "\n")
output_file.close()
