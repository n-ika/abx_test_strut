import pandas as pd
import sys
from shutil import copy

#read abkhazia segments.txt file
SEGMENTS_FILE = sys.argv[1]
OUT_FOLDER = sys.argv[2]


segm_df = pd.read_csv(SEGMENTS_FILE, sep=" ", header=0,\
                     names=['utt_id', 'filename'])

for row in segm_df.itertuples():
    filename = getattr(row, 'filename')
    file_path = './model/supervised/intervals_for_model/wavs/' + filename
    copy(file_path, OUT_FOLDER) 
