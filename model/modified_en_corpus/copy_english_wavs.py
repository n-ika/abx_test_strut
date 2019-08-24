import pandas as pd
import sys
from shutil import copy

#read file of selected wavs
SELECTION_FILE = sys.argv[1]
OUT_FOLDER = sys.argv[2]


sel_df = pd.read_csv(SELECTION_FILE, header=None,\
                     names=['filename'])

for row in sel_df.itertuples():
    filename = getattr(row, 'filename')
    file_path = '/scratch2/njurov/abkhazia_projects/en_corpus_jan2019_abkhazia/split/train/data/wavs/' + filename
    copy(file_path, OUT_FOLDER) 