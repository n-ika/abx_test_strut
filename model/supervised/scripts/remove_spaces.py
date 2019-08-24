# Author: Nika Jurov

import sys

IN_FILE = sys.argv[1]
OUT_FILE = sys.argv[2]

f = open(IN_FILE, 'r')

with open(OUT_FILE, 'w') as f2:

    for row in f.readlines():

        #print >> f2, row.replace("  ", " ")
        f2.write(row.replace("  ", " ")) 