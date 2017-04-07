import sys

if len(sys.argv) != 2:
    print "ERROR. Correct usage: python scipt.py file"
    sys.exit(0)

#Get the first parameter a.k.a. the input file
FILE_NAME = sys.argv[1]

#Read the file
input_file = open(FILE_NAME, 'r')
input_rows = list(input_file)

output_file = open('output.txt', 'w')

# ----------------------------------
# Parsing input file to problem vars
# READ SINGLE INT: int(input_rows[])
# READ INT LIST: map(int, input_rows[].split(' '))
# ----------------------------------

# -------------
# Solve problem
# -------------
N = int(input_rows[0])
i = 0
for line in input_rows[1:]:
    i += 1
    smax = int(line.split(' ')[0])
    s = map(int, list(line.split(' ')[1])[:-1])
    k = 0
    added = 0
    standing = 0
    print s
    while k <= smax:
        if standing >= k:
            standing += s[k]
            k += 1
        else:
            standing += 1
            added += 1
    output_file.write("Case #" + str(i) + ": " + str(added) + "\n")

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------


output_file.close()
