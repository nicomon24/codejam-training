import sys

sys.setrecursionlimit(10000)

if len(sys.argv) != 2:
    print "ERROR. Correct usage: python scipt.py file"
    sys.exit(0)

#Get the first parameter a.k.a. the input file
FILE_NAME = sys.argv[1]

#Read the file
output_file = open('output2.txt', 'w')
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

def divide_first(total, x):
    res = []
    for i in range(-4,5):
        if i!=0 and multiply(x, i) == total:
            res.append(i)
    if len(res) != 1:
        print "ERROROROROOROROROROOR\n\n\nn\n\n\nn\n\nn\n\nn\n\n"
        return 0
    return res[0]

def divide_second(total, x):
    res = []
    for i in range(-4,5):
        if i!=0 and multiply(i, x) == total:
            res.append(i)
    if len(res) != 1:
        print "ERROROROROOROROROROOR\n\n\nn\n\n\nn\n\nn\n\nn\n\n"
        return 0
    return res[0]

def condense(vect):
    if len(vect) <= 0:
        return 1
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

def solve(vect, times):
    if times <= 2:
        if condense(vect) == -1:
            return solve_i(vect)
        else:
            return 0
    # First check
    y = condense(vect)
    #print y
    if y == 1 or (times % 4 != 2 and not y==-1):
        return 0
    # Prepare
    sq = multiply(y,y)
    loop = [1, y, sq, multiply(y,sq)]
    #print loop
    diff = {}
    for i in range(0,4):
        diff[(i,0)] = loop[i]
        agg1 = loop[i]
        for j in range(1,len(vect)):
            agg1 = multiply(agg1, vect[j-1])
            diff[(i,j)] = agg1
        agg2 = loop[i]
        for j in range(-1, -(len(vect)), -1):
            agg2 = multiply(vect[j],agg2)
            diff[(i,j)] = agg2
    #for key in diff:
    #    print str(key) + " => " + str(diff[key])
    # Compute
    twos = [key for key in diff.keys() if diff[key]==2]
    #print twos
    totlen = len(vect) * times
    for i in twos:
        if i[1] >= 0:
            timesi = i[0]
            if i[1] > 0:
                timesi += 1
            resi = condense(vect[i[1]:])
            totalj = divide_first(3, resi)
            #print totalj
            js = [key for key in diff.keys() if diff[key]==totalj and key[1]>=0]
            '''
            print js
            print "Using i: " + str(i)
            print "Times-i: " + str(timesi)
            print "Residual-i: " + str(vect[i[1]:]) + " - " + str(resi)
            '''
            for jkey in js:
                timesj = timesi + jkey[0]
                #print timesj
                if jkey[1] > 0:
                    resj = condense(vect[jkey[1]:])
                else:
                    resj = 1
                #print resj
                nt = times - timesj
                if nt > 0:
                    nt = nt % 4
                    #print nt
                    if multiply(resj, loop[nt])==4:
                        return 1
            '''
            for k in fours:
                if k[1] <= 0:
                    timesk = k[0]
                    stepsk = k[1]
                    if k[1] < 0:
                        timesk += 1
                    resk = condense(vect[0:k[1]])
                    print "Using k: " + str(k)
                    print "Times-k: " + str(timesk)
                    print "Residual-k: " + str(vect[0:k[1]]) + " - " + str(resk)
                    # Verify j
                    nt = (times - timesi - timesk)
                    if nt > 0:
                        nt = nt % 4
                        a = multiply(resi, loop[nt])
                        print "NTimes: " + str(nt)
                        print a
                        print multiply(a, resk)
                        if multiply(a, resk) == 3 :
                            return 1
            '''
    return 0

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
    print "Case #" + str(c) + ": " + str(x) + " --- " + str(s)
    sint = map(convert, s)
    a = solve(sint, x)
    b = 'YES'
    if a == 0:
        b = 'NO'
    print "Case #" + str(c) + ": " + str(b)
    output_file.write("Case #" + str(c) + ": " + str(b) + "\n")

d = map(convert, 'ji')
print solve(d, 6)

# -------------------------
# Write to file the results
# WRITE LINE: output_file.write(line + "\n")
# -------------------------


output_file.close()
