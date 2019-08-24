# Author: Nika Jurov

import h5features as h5f
import numpy as np
import pandas as pd
import sys
import os

hf5_file = sys.argv[1] # the posterior gram file in .h5 format
TRIPLET_NAME = sys.argv[2] # which index / utterance do we want
NAMED_PG = sys.argv[3] # name the extracted PG


times_r, features_r = h5f.read(hf5_file, 'features')
#items = h5f.Reader(hf5_file, 'features').items.data[0:]

#utterance = items[int(NUMBER)]

f = pd.DataFrame(features_r[TRIPLET_NAME])


f['times'] = ["time_" + str('{0:03}'.format(i)) for i in range(0,f.shape[0])]
f.to_csv("model/supervised/posterior_grams/extracted_pgs/" \
            + NAMED_PG + ".csv", index=False)

#print "The utterance ID is: " + str(utterance)