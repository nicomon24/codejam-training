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
# ----------------------------------
cases = []
N = int(input_rows[0])
for i in range(0,N):
    case = {}
    case["credit"] = int(input_rows[(i*3) + 1])
    case["nitems"] = int(input_rows[(i*3) + 2])
    case["items"] = map(int, input_rows[(i*3) + 3].split(' '))
    cases.append(case)

# -------------
# Solve problem
# -------------
for c in range(0,len(cases)):
    items = cases[c]["items"]
    for i in range(0, len(items)):
        for j in range(i+1, len(items)):
            summer = items[i] + items[j]
            if summer == cases[c]["credit"]:
                cases[c]["solution"] = "Case #" + str(c+1) + ": " + str(i+1) + " " + str(j+1)

# -------------------------
# Write to file the results
# -------------------------
output_file = open('output.txt', 'w')
for c in range(0,len(cases)):
    output_file.write(cases[c]["solution"] + "\n")
output_file.close()
