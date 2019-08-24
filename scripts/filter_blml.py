import pandas as pd
import sys
import os

TRIPLETS = sys.argv[1]

cwd = os.getcwd()

new_triplets = cwd + "/outputs/triplets.csv"

file_open = open(TRIPLETS, 'r')
triplets_csv = pd.read_csv(file_open)

# filter out the cases where THT and OTH are monolingual
filtered_ml = triplets_csv[(triplets_csv['blml_TGT']=="bl") & \
                            (triplets_csv['blml_OTH']=="bl")]

# filter out the cases where THT and OTH are same
filtered_bl = filtered_ml[(filtered_ml['speaker_TGT'] != \
                            filtered_ml['speaker_OTH'])]

filtered_bl.to_csv(new_triplets, mode="w", index=False)

