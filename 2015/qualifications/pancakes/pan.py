import sys, math

sys.setrecursionlimit(10000)

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

def magic(plates, removing):
    max_val = max(plates)
    if max_val <= 1 or max_val == removing:
        return plates
    pl = plates[:]
    pl[pl.index(max_val)] -= removing
    pl.append(removing)
    return pl

def score(plates):
    s = sum(plates)
    mean = s / float(len(plates))
    var = 0.0
    for x in plates:
        var += abs(x-mean)
    var = var / float(len(plates))
    return var + mean

def solve(plates, step):
    print plates
    if step < 0:
        return max(plates)
    # Get max val
    max_val = max(plates)
    upper = int(math.floor(max_val/2)) + 1
    res = [max(plates)]
    plates_score = score(plates)
    for v in range(2, upper+2):
        m = magic(plates, v)
        #print m
        #print score(m)
        if len(m) != len(plates) and score(m) <= plates_score:
            x = solve(m, step-1) + 1
            res.append(x)
    return min(res)

i = 0
n = int(input_rows[0])
for k in range(0,n):
    line = input_rows[2*k+2]
    i += 1
    plates = map(int, line.split(' '))
    x = solve(plates, max(plates))
    print str(plates) + " => " + str(x)
    output_file.write("Case #" + str(i) + ": " + str(x) + "\n")

x =  map(int, "6 2 9".split(' '))
print score(x)
print solve(x, max(x))

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------

output_file.close()
