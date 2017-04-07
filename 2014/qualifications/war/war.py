import sys, logging, random
import numpy as np
from collections import defaultdict

# ------- SETUP APPLICATION -----
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='%(levelname)s:%(message)s')

STEP = 0.00001

# Define what agent ken should choose when naomi
# Returns the block choosen by ken
def ken(kens, chosen_by_naomi):
    choice = 0
    biggers = [x for x in kens if x > chosen_by_naomi]
    if len(biggers) > 0:
        # I have a bigger block
        logging.debug("Ken has bigger block than %s", chosen_by_naomi)
        chosen_block = min(biggers)
    else:
        # No bigger block, choose the worst
        logging.debug("Ken has no bigger block %s", chosen_by_naomi)
        chosen_block = min(kens)
    index = np.argwhere(kens==chosen_block)[0][0]
    return index

# Order in
def naomiWins(naomis, kens):
    naomis_ordered = np.sort(naomis)[::-1]
    kens_ordered = np.sort(kens)[::-1]
    for i in range(0, len(naomis_ordered)):
        if naomis_ordered[i] < kens_ordered[i]:
            return False
    return True

# Returns (chosen, told) blocks
def naomi(naomis, kens, is_deceived=False):
    if not is_deceived:
        choice = random.randrange(0,len(naomis))
        return (choice, naomis[choice])
    else:
        # Find the second (in order of magnitude) block of ken
        if naomiWins(naomis, kens):
            # Naomi wins, choose wisely
            logging.debug("Naomi is in advantage")
            # If naomis says a number that is greater than its max, ken will choose his worst
            token = max(kens) + STEP/10
            # But present a block that is slightly greater than ken's worst
            biggers = [x for x in naomis if x > min(kens)]
            choice = np.argwhere(naomis==min(biggers))[0][0]
            return (choice, token)
        else:
            # Use deceiving strategy
            logging.debug("Naomi is in disadvantage")
            choice = np.argwhere(naomis==min(naomis))[0][0]
            token = max(kens) - STEP/10
            return (choice, token)


# Play a game, return the number of points (naomi, ken)
def play(blocks, is_deceived = False):
    naomis = blocks[0]
    kens = blocks[1]
    logging.info("Starting GAME")
    logging.info("Naomi: %s", naomis)
    logging.info("Ken: %s", kens)
    points = np.array([0,0])
    while len(naomis)>0:
        # Printing game state
        logging.debug("Naomi: %s", naomis)
        logging.debug("Ken: %s", kens)
        # Naomi plays
        nchosen = naomi(naomis, kens, is_deceived)
        logging.debug("Naomi chooses %f", naomis[nchosen[0]])
        logging.debug("Naomi says %f", nchosen[1])
        # Ken plays knowing what naomis told
        k = ken(kens, nchosen[1])
        # Evaluating
        logging.debug("Naomi plays %f ken plays %f", naomis[nchosen[0]], kens[k])
        if naomis[nchosen[0]] > kens[k]:
            # Naomi wins one point
            points[0] += 1
            logging.info("Naomi wins %s", points)
            # Looking at computations, when naomi wins in the deceived strategy
            # she is going to win every other match. So is safe to return directly
            # the remaining games as won by naomi
            if is_deceived:
                points[0] = len(naomis)
                return points
        else:
            # Ken wins one point
            points[1] += 1
            logging.info("Ken wins %s", points)
        # Remove played items
        naomis = np.delete(naomis, nchosen[0])
        kens = np.delete(kens, k)
    return points

# Return 2 arrays of length N (if defined, random otherwise when -1) with random values
def randomGame(N = -1):
    gameraw = np.arange(STEP,1,STEP)
    np.random.shuffle(gameraw)
    game = gameraw[:2*N]
    return (game[:N], game[N:])

def alotofgames():
    points = np.array([0,0])
    for i in range(0, 1000):
        points += play(randomGame(5))
    print(points)

# ---- INPUT / OUTPUT SETUP -----
if len(sys.argv) != 2:
    print("ERROR. Correct usage: python scipt.py file")
    sys.exit(0)
# Create an output filename from the standard competition input dataset names
def outputFilenameFromInput(infilename):
    # STD filename of input [char]-[small/large]-practice.in.txt
    name = infilename.split('.')[0]
    if len(name.split('-')) >= 2:
        return name.split('-')[1] + ".txt"
    else:
        return name + ".txt"
#Get the first parameter a.k.a. the input file
FILE_NAME = sys.argv[1]
#Read the file
output_file = open(outputFilenameFromInput(FILE_NAME), 'w')
input_file = open(FILE_NAME, 'r')
input_rows = list(input_file)

# ------- SOLVE BELOW THIS ---------
# Parsing input file to problem vars
# READ SINGLE INT: int(input_rows[i])
# READ INT LIST: map(int, input_rows[i].split(' '))
# WRITE LINE: output_file.write(line + "\n")
# ----------------------------------

# Read number of test cases
N = int(input_rows[0])
input_rows = input_rows[1:]
# Loop through all the tests
for i in range(0, N):
    logging.info("Computing case %d", i+1)
    # Compute
    n = int(input_rows[3*i])
    naomis = np.array([float(x) for x in input_rows[3*i+1].split(' ')])
    kens = np.array([float(x) for x in input_rows[3*i+2].split(' ')])
    x = play((naomis, kens), False)[0]
    y = play((naomis, kens), True)[0]
    # Write to output file
    output_file.write("Case #" + str(i+1) + ": " + str(y) + " " + str(x) + "\n")

# ---------- OUTPUT CLOSE ----------
output_file.close()
