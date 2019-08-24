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


def find_orig_info(orig_table, int_nums):
    interval_info = pd.DataFrame(columns=["tripletid", \
                                "stimulus", "start", "end", \
                                "word", "utt", "abx"])

    for row in orig_table.itertuples():
        word_OTH = getattr(row, 'word_OTH')
        word_TGT = getattr(row, 'word_TGT')
        word_X = getattr(row, 'word_X')

        file_OTH = getattr(row, 'file_OTH')
        file_TGT = getattr(row, 'file_TGT')
        file_X = getattr(row, 'file_X')

        tripletid = getattr(row, 'tripletid')

        words = (word_OTH, word_TGT, word_X)
        files = (file_OTH, file_TGT, file_X)

        for int_row in int_nums.itertuples():
            if getattr(int_row, 'spk_num_name') in files:
                stim_spk = getattr(int_row, 'spk_num_name')
                start = getattr(int_row, 'stim_start')
                end = getattr(int_row, 'stim_end')
                word = getattr(int_row, 'stimulus')
                real_count = getattr(int_row, 'real_count')
                
                #assert getattr(int_row, 'stimulus') in words

                if stim_spk == file_OTH:
                    abx = "OTH"
                elif stim_spk == file_TGT:
                    abx = "TGT"
                elif stim_spk == file_X:
                    abx = "X"

                spk_name = "_".join(stim_spk.split('_')[:-1])
                spk_num = get_speaker_num(spk_name)
                lang = stim_spk.split('_')[1]
                if lang == "eng":
                    lang = "en"
                # e.g. spk01_utt_fr01005
                utt = spk_num + "_utt_" + lang \
                        + str(spk_num[-2:]) + \
                        str('{0:03}'.format(real_count))

                one_int = pd.DataFrame([[tripletid, stim_spk, start, \
                                         end, word, utt, abx]],
                                         columns=["tripletid", "stimulus", \
                                         "start", "end", \
                                         "word", "utt", "abx"])
                interval_info = interval_info.append(one_int, \
                                             ignore_index=True)

    return interval_info


new_table = find_orig_info(orig_table, int_nums)
new_table.to_csv(TABLE_NAME)

