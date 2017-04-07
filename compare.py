import sys

if len(sys.argv) != 3:
    print "ERROR. Correct usage: python scipt.py file"
    sys.exit(0)

#Get the first parameter a.k.a. the input file
FILE_1 = sys.argv[1]
FILE_2 = sys.argv[2]

#Read the file
input1 = open(FILE_1, 'r')
input2 = open(FILE_2, 'r')
rows1 = list(input1)[1:]
rows2 = list(input2)[1:]

for i in range(0,len(rows1)):
    l1 = rows1[i].split(':')[1]
    l2 = rows2[i].split(':')[1]
    if l1!=l2:
        print rows1[i].split(':')[0] + " differ!"
