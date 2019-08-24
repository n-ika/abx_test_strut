# Author: Nika Jurov

import sys
import os
import pandas as pd

# distance_list.csv with stimuli - used for experiment
DISTANCE_LIST = sys.argv[1] 
# int_times_counts.csv with stimuli numbered and with times
INT_NUMS = sys.argv[2]
# name for new table to output
TABLE_NAME = sys.argv[3] 

orig_table = pd.read_csv(DISTANCE_LIST)
int_nums = pd.read_csv(INT_NUMS)


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

def filter_table(tripletid, int_nums, orig_word, file, abx):
    filtered = int_nums[int_nums.spk_num_name == file]
    i = filtered.index.values.astype(int)[0]
    word = filtered.loc[i, 'stimulus']
    if word != orig_word:
        no_num_spk = '_'.join(file.split('_')[:-1])
        filtered = int_nums[(int_nums.stimulus == orig_word) & \
        (int_nums['spk_num_name'].str.contains(no_num_spk))]
        i = filtered.index.values.astype(int)[0]
        word = filtered.loc[i, 'stimulus']
        print file, filtered.loc[i, 'spk_num_name']
    
    stim_spk = filtered.loc[i, 'spk_num_name']
    stim_start_ = filtered.loc[i, 'stim_start']
    stim_end_ = filtered.loc[i, 'stim_end']
    start = filtered.loc[i, 'utt_start']
    end = filtered.loc[i, 'utt_end']
    utt_start = 0
    utt_end = end - start
    stim_start = stim_start_ - start
    stim_end = stim_end_ - start
    real_count = filtered.loc[i, 'real_count']

    spk_name = "_".join(stim_spk.split('_')[:-1])
    spk_num = get_speaker_num(spk_name)
    lang = stim_spk.split('_')[1]
    if lang == "eng":
        lang = "en"
    # e.g. spk01_utt_fr01005
    utt = spk_num + "_utt_" + lang \
                + str(spk_num[-2:]) + \
                str('{0:03}'.format(real_count))

    one_int = pd.DataFrame([[tripletid, stim_spk, stim_start, stim_end, \
                             utt_start, utt_end, word, utt, abx]],
                             columns=["tripletid", "stimulus", \
                             "stim_start", "stim_end", "utt_start", \
                             "utt_end", "word", "utt", "abx"])
    return one_int
            


def find_orig_info(orig_table, int_nums):
    interval_info = pd.DataFrame(columns=["tripletid", \
                                "stimulus", "stim_start", "stim_end", \
                                "utt_start", "utt_end", \
                                "word", "utt", "abx"])

    for row in orig_table.itertuples():
        word_OTH = getattr(row, 'word_OTH')
        word_TGT = getattr(row, 'word_TGT')
        word_X = getattr(row, 'word_X')

        file_OTH = getattr(row, 'file_OTH')
        file_TGT = getattr(row, 'file_TGT')
        file_X = getattr(row, 'file_X')

        tripletid = getattr(row, 'tripletid')

        #words = (word_OTH, word_TGT, word_X)
        #files = (file_OTH, file_TGT, file_X)

        OTH_filt = filter_table(tripletid, int_nums, \
                                word_OTH, file_OTH, "OTH")
        TGT_filt = filter_table(tripletid, int_nums, \
                                word_TGT, file_TGT, "TGT")
        X_filt = filter_table(tripletid, int_nums, \
                                word_X, file_X, "X")


        interval_info = interval_info.append(OTH_filt, \
                                         ignore_index=True)
        interval_info = interval_info.append(TGT_filt, \
                                         ignore_index=True)
        interval_info = interval_info.append(X_filt, \
                                         ignore_index=True)

    return interval_info



new_table = find_orig_info(orig_table, int_nums)
new_table.to_csv(TABLE_NAME)

