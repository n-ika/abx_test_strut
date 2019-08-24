# Author: Nika Jurov

import sys
import pandas as pd
import numpy as np

IN_FILE = sys.argv[1] # lexicon used for Abkhazia
OUT_FILE = sys.argv[2] # lexicon in csv format

f = open(IN_FILE, 'r')
lexicon = pd.DataFrame(columns=["word", "phonemes"])

for row in f.readlines():
    each_element = row.split(" ")
    word = each_element[0:1][0].strip('[]')
    phonemes = " ".join(each_element[1:]).strip('\n')
    #phonemes = " ".join(phonemes).strip('\n')


    one_word = pd.DataFrame([[word, phonemes]],
                                columns=["word", "phonemes"])
    lexicon = lexicon.append(one_word, ignore_index=True)


lexicon.to_csv(OUT_FILE, index=False)