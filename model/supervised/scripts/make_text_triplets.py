# Author: Nika Jurov

import pandas as pd
import numpy as np
import sys


INPUT_TABLE = sys.argv[1] #experimental_list_w_filenames

table = pd.read_csv(INPUT_TABLE)

for row in table.itertuples():

    word_A = getattr(row, 'Stimulus_A')
    word_B = getattr(row, 'Stimulus_B')
    word_X = getattr(row, 'Stimulus_X')
    
    tripletid = getattr(row, 'tripletid')

    # triplet44.wav
    new_filename = "model/supervised/triplets_for_model/text/" + tripletid + ".txt"

    text_file = pd.DataFrame([[word_A, word_B, word_X]])
    text_file.to_csv(new_filename, sep=' ', header=False, index=False)