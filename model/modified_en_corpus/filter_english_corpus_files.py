import numpy as np
import pandas as pd
import sys
import os
import io

TEXT = sys.argv[1]
SEGMENTS = sys.argv[2]
UTT2SPK = sys.argv[3]
SELECTION_CSV = sys.argv[4]
OUT_FOLDER = sys.argv[5]

text_file = open(TEXT, 'r+')
segment_file = open(SEGMENTS, 'r+')
utt2spk_file = open(UTT2SPK , 'r+')
selection = pd.read_csv(SELECTION_CSV, header=None,\
                     names=['filename'])

def omit_utterances(some_file, OUT_FOLDER, name):
    new_name = OUT_FOLDER + name + ".txt"
    with open(new_name, 'w+') as f:
        #new_file = pd.DataFrame()
        i = 0
        for line_i in some_file.readlines():
            for row in selection.itertuples():
                wav = getattr(row, 'filename')
                wav_name = wav.split('.')[0]
                if line_i.startswith(wav_name):
                    #new_file.loc[i] = line_i
                    line_i = line_i.rstrip('\n')
                    print >> f, line_i
                    i += 1
        #new_file.to_csv(new_name, index=False, header=False)


omit_utterances(text_file, OUT_FOLDER, "text")
omit_utterances(segment_file, OUT_FOLDER, "segments")
omit_utterances(utt2spk_file, OUT_FOLDER, "utt2spk")


