import os
import pandas as pd
import sys

WAVS_FOLDER = sys.argv[1]
OUTPUT_FOLDER = sys.argv[2]


segments = pd.DataFrame()
utt2spk = pd.DataFrame()
text = pd.DataFrame()

count = 1
#for dirpath, dirname, filename in os.walk(WAVS_FOLDER):
for filename in os.listdir(WAVS_FOLDER):
    if filename.endswith(".wav"):
        utt_id = "spk01_utt" + str('{0:03}'.format(count))
        spk_id = "spk01"
        word = filename.split('.')[0].split('_')[0]

        # segments = utt_id + filename
        segments_add = pd.DataFrame([[utt_id, filename]])

        # utt2spk = utt_id + spk_num
        utt2spk_add = pd.DataFrame([[utt_id, spk_id]])
        
        # text = utt_id + word
        text_add = pd.DataFrame([[utt_id, word]])

        segments = segments.append(segments_add, ignore_index=True)
        utt2spk = utt2spk.append(utt2spk_add, ignore_index=True)
        text = text.append(text_add, ignore_index=True)

        count += 1

segments.to_csv(OUTPUT_FOLDER + "/segments.txt", \
                sep=' ', header=False, index=False)
utt2spk.to_csv(OUTPUT_FOLDER + "/utt2spk.txt", \
                sep=' ', header=False, index=False)
text.to_csv(OUTPUT_FOLDER + "/text.txt", sep=' ', \
                header=False, index=False)