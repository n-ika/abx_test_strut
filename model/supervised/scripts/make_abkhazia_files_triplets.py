# Author: Nika Jurov

import pandas as pd
import numpy as np
import sys
import re


INPUT_TABLE = sys.argv[1]
TIMES_TABLE = sys.argv[2]
OUTPUT_FOLDER = sys.argv[3]

table = pd.read_csv(INPUT_TABLE)
times_info = pd.read_csv(TIMES_TABLE)

segments = pd.DataFrame()
utt2spk = pd.DataFrame()
text = pd.DataFrame()


def get_speaker_num(spk_name):
    if spk_name == "veronique_eng":
        spk_num = "spk01"
    elif spk_name == "veronique_fr":
        spk_num = "spk02"
    elif spk_name == "maureen_eng":
        spk_num = "spk03"
    elif spk_name == "maureen_fr":
        spk_num = "spk04"
    elif spk_name == "remi_fr":
        spk_num = "spk05"
    elif spk_name == "marc_fr":
        spk_num = "spk06"
    elif spk_name == "jeremy_eng":
        spk_num = "spk07"
    elif spk_name == "ewan_eng":
        spk_num = "spk08"
    return spk_num

def get_times(word, x_word, tripletid, times_info):
    times_info = times_info[times_info["triplet"] == tripletid]


    if word == x_word:
        times_info_ = times_info[times_info["word"] == word]
        times_info1 = times_info_[times_info_["order"] == "X"]
        times_X = (float(times_info1["start"]),\
                    float(times_info1["end"]))
        times_info2 = times_info_[times_info_["order"] != "X"]
        times_TGT = (float(times_info2["start"]),\
                    float(times_info2["end"]))

        times = (times_TGT, times_X)
    else:
        times_info3 = times_info[times_info["word"] == word]
        times_OTH = (float(times_info3["start"]),\
                    float(times_info3["end"]))
        times = times_OTH

    return times



for row in table.itertuples():

    word_OTH = getattr(row, 'word_OTH')
    word_TGT = getattr(row, 'word_TGT')
    word_X = getattr(row, 'word_X')
    
    tripletid_ = getattr(row, 'tripletid')
    tripl_num = re.split('(\d+)', tripletid_)[1]
    tripletid = "tripletid" + '{0:03}'.format(int(tripl_num))

    # triplet044.wav
    filename = tripletid + ".wav"


    spk_OTH = "_".join(getattr(row, 'file_OTH').split('_')[:-1])
    spk_TGT = "_".join(getattr(row, 'file_TGT').split('_')[:-1])
    spk_X = "_".join(getattr(row, 'file_X').split('_')[:-1])

    spk_OTH_num = get_speaker_num(spk_OTH)
    spk_TGT_num = get_speaker_num(spk_TGT)
    spk_X_num = get_speaker_num(spk_X)
    

    utt_OTH_num = tripletid + "_01"
    utt_TGT_num = tripletid + "_02"
    utt_X_num = tripletid + "_03"
    
    utt_id_OTH = spk_OTH_num + "_" + utt_OTH_num
    utt_id_TGT = spk_TGT_num + "_" + utt_TGT_num
    utt_id_X = spk_X_num + "_" + utt_X_num


    tgt_x_times = get_times(word_TGT, word_X, tripletid_, times_info)
    oth_times = get_times(word_OTH, word_X, tripletid_, times_info)


    # segments = utt_id + filename + start & end time
    segments_add = pd.DataFrame([[utt_id_OTH, filename, oth_times[0], oth_times[1]], \
                    [utt_id_TGT, filename, tgt_x_times[0][0], tgt_x_times[0][1]], \
                    [utt_id_X, filename, tgt_x_times[1][0], tgt_x_times[1][1]]])

    # utt2spk = utt_id + spk_num
    utt2spk_add = pd.DataFrame([[utt_id_OTH, spk_OTH_num], \
                    [utt_id_TGT, spk_TGT_num], \
                    [utt_id_X, spk_X_num]])
    
    # text = utt_id + word
    text_add = pd.DataFrame([[utt_id_OTH, word_OTH], \
                    [utt_id_TGT, word_TGT], \
                    [utt_id_X, word_X]])


    segments = segments.append(segments_add, ignore_index=True)
    utt2spk = utt2spk.append(utt2spk_add, ignore_index=True)
    text = text.append(text_add, ignore_index=True)


segments.to_csv(OUTPUT_FOLDER + "/segments.txt", sep=' ', header=False, index=False)
utt2spk.to_csv(OUTPUT_FOLDER + "/utt2spk.txt", sep=' ', header=False, index=False)
text.to_csv(OUTPUT_FOLDER + "/text.txt", sep=' ', header=False, index=False)