# Author: Nika Jurov

import pandas as pd
import numpy as np
import sys
import re


INPUT_TABLE = sys.argv[1]
OUTPUT_FOLDER = sys.argv[2]

table = pd.read_csv(INPUT_TABLE)

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



for row in table.itertuples():

    word_OTH = getattr(row, 'word_OTH')
    word_TGT = getattr(row, 'word_TGT')
    word_X = getattr(row, 'word_X')
    
    tripletid_ = getattr(row, 'tripletid')
    tripl_num = re.split('(\d+)', tripletid_)[1]
    tripletid = "triplet" + '{0:03}'.format(int(tripl_num))

    # triplet44_OTH.wav
    file_OTH = tripletid + "_OTH" + ".wav"
    file_TGT = tripletid + "_TGT" + ".wav"
    file_X = tripletid + "_X" + ".wav"


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


    # segments = utt_id + filename
    segments_add = pd.DataFrame([[utt_id_OTH, file_OTH], \
                    [utt_id_TGT, file_TGT], \
                    [utt_id_X, file_X]])

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


segments.to_csv(OUTPUT_FOLDER + "/segments.txt", \
                sep=' ', header=False, index=False)
utt2spk.to_csv(OUTPUT_FOLDER + "/utt2spk.txt", \
                sep=' ', header=False, index=False)
text.to_csv(OUTPUT_FOLDER + "/text.txt", sep=' ', \
                header=False, index=False)