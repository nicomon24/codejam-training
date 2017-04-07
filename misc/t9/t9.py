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
current_key = 2
counter = 0
translation = {}
for c in range(ord('a'),ord('z')+1):
    trans = str(current_key) * (counter+1)
    if current_key == 7 or current_key == 9:
        counter = (counter + 1) % 4
    else:
        counter = (counter + 1) % 3
    if counter == 0:
        current_key += 1
    translation[chr(c)] = trans

translation[' '] = '0'

def translate(char):
    return translation[char]

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------
output_file = open('output.txt', 'w')
for i in range(0,N):
    line = list(input_rows[i+1][:-1])
    res = ""
    for j in range(0, len(line)):
        trans = translation[line[j]]
        if res[::-1][:1] == trans[:1]:
            res += ' '
        res += trans
    output_file.write("Case #" + str(i+1) + ": " + res + "\n")

output_file.close()
