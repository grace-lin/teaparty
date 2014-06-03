import sys
import math
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 3:
    print "Usage: python tiling.py <input_file> <output_file>"
    sys.exit(0)

# Opens the files passed in the command line for reading/writing
_in = open(sys.argv[1], "r")
_out = open(sys.argv[2], "w")

# distance constraint
S = int(_in.readline())

# seating arrangement, as a list of guest-seat pairs
seating = map(lambda p: map(lambda i: int(i), p.split(" ")), 
       map(lambda s: s.replace("(", "").replace(")",""), _in.readline().split(") (")))

# list of guests to move
moving = map(lambda i: int(i), _in.readline().split(" "))

# a Z3 solver instance
solver = Solver()

# number of people in the party
n = len(seating)

X = [[ Int("x_%s_%s" % (i, j)) for j in range(2)] for i in range(n)]


# everyone who was there is still there after moving
same_c = [X[i][0] == seating[i][0] for i in range(n)]


# is value x of X[i][0] to move?
def toMove(x):
	for i in range(len(moving)):
		if moving[i] == x:
			return True
	return False


# all new seats must belong in old seats
existing_c = [ Or([
	X[i][1] == seating[j][1]
	for j in range(n)])
	for i in range(n)]


# all seats are distinct from each other
diff_c = [ Distinct([X[i][1] for i in range(n) ])]


# get different seats if moving
move_c = [ Or(
	[If(toMove(seating[i][0]),
	And(math.fabs(int(i) - int(j)) >= 0,
	    math.fabs(int(i) - int(j)) <= S,
	    i >= 0, j >= 0,
	    i != j,
	    X[i][1] == seating[j][1]),
	X[i][1] == seating[i][1])
	for j in range(n)])
	for i in range(n)]


total_c = same_c + move_c + diff_c + existing_c
solver.add(total_c)
isSAT = solver.check()
if isSAT == sat:
    m = solver.model()
    for i in range(n):
	_out.write("("),
	_out.write("%s" % m[X[i][0]]),
	_out.write(" "), 
        _out.write("%s" % m[X[i][1]]),
	_out.write(") ")
    _out.write("\n")
else:
    _out.write("no solution possible\n")
