# Author: Nika Jurov

import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

f = open(in_file, 'r')
with open(out_file, 'w') as f_out:
    for line in f.readlines():
        split_line = line.split('\t')
        for i,num in enumerate(split_line):
            if '.' in num:
                num = 1.0
                split_line[i] = num
            split_line[i] = str(num) 
        print >> f_out, '    '.join(split_line)

