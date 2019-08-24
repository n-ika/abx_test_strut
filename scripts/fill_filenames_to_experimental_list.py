# This script adds columns to the stimuli list by
# adding the name of the real .wav filename of
# each stimulus interval. It finds it in a folder
# where intervals are. It also adds the stimulus
# number. 
#
# Additionally, it generates the stimulus
# list Stimulus_list.txt needed for concatenation
# done with a Praat script.

import pandas as pd
import numpy as np
import sys



INPUT_TABLE = sys.argv[1]
INTERVAL_FOLDER = sys.argv[2]
INPUT_META_TABLE = sys.argv[3]


table = pd.read_csv(INPUT_TABLE)
meta_table = pd.read_csv(INPUT_META_TABLE)
stimlist = pd.DataFrame()
distance_list = pd.DataFrame()


table = table.rename(index=str, columns={'Bilingual_spk_EN':"Bilingual_spk_eng",
                                        'Bilingual_spk_FR':"Bilingual_spk_fr",
                                        'Vowel_EN':"Vowel_eng",
                                        'Vowel_FR':"Vowel_fr"})


table['tripletid'] = pd.Series(["triplet" + str(i) for i in \
                    range(1, table.shape[0]+1)], index=table.index)


def get_info_triplet_order(order):

    if str(order) == "EFE":
        A = "eng"
        B = "fr"
        X = "eng"
        OTH = "B"
        TGT = "A"
    elif str(order) == "EFF":
        A = "eng"
        B = "fr"
        X = "fr"
        OTH = "A"
        TGT = "B"
    elif str(order) == "FEE":
        A = "fr"
        B = "eng"
        X = "eng"
        OTH = "A"
        TGT = "B"
    elif str(order) == "FEF":
        A = "fr"
        B = "eng"
        X = "fr"
        OTH = "B"
        TGT = "A"
    return (A,B,X,OTH,TGT)


def get_data_by_order(table_row, meta_table):

    order_in_row = getattr(table_row, 'Order')
    order_info = get_info_triplet_order(order_in_row)
    
    A = order_info[0]
    B = order_info[1]
    X = order_info[2]
    OTH = order_info[3]
    TGT = order_info[4]

    context = getattr(table_row, 'Context')

    speaker_A = getattr(table_row, 'Bilingual_spk_' + A)
    speaker_B = getattr(table_row, 'Bilingual_spk_' + B)
    speaker_X = getattr(table_row, 'Mono_spk')
    stimulus_A = context.replace("_", \
                            getattr(table_row, 'Vowel_' + A))
    stimulus_B = context.replace("_", \
                            getattr(table_row, 'Vowel_' + B))
    stimulus_X = context.replace("_", \
                            getattr(table_row, 'Vowel_' + X))

    meta_table_A = meta_table[(meta_table["speaker"] == speaker_A) \
            & (meta_table["int_name"] == stimulus_A) \
            & (meta_table["language"] == A)].reset_index()

    meta_table_B = meta_table[(meta_table["speaker"] == speaker_B) \
            & (meta_table["int_name"] == stimulus_B) \
            & (meta_table["language"] == B)].reset_index()

    meta_table_X = meta_table[(meta_table["speaker"] == speaker_X) \
            & (meta_table["int_name"] == stimulus_X) \
            & (meta_table["language"] == X)].reset_index()

    file_A_full = meta_table_A["int_filename"].iloc[0]
    file_B_full = meta_table_B["int_filename"].iloc[0]
    file_X_full = meta_table_X["int_filename"].iloc[0]


    if TGT == "A":
        stimulus_TGT = stimulus_A
        stimulus_OTH = stimulus_B
        file_TGT_full = file_A_full
        file_OTH_full = file_B_full
        speakerTGT = speaker_A
        speakerOTH = speaker_B
        vowelTGT = getattr(table_row, 'Vowel_' + A)
        vowelOTH = getattr(table_row, 'Vowel_' + B)

    else:
        stimulus_TGT = stimulus_B
        stimulus_OTH = stimulus_A
        file_TGT_full = file_B_full
        file_OTH_full = file_A_full
        speakerTGT = speaker_B
        speakerOTH = speaker_A
        vowelTGT = getattr(table_row, 'Vowel_' + B)
        vowelOTH = getattr(table_row, 'Vowel_' + A)

    
    eng_vowel = getattr(table_row, 'Vowel_eng')
    fr_vowel = getattr(table_row, 'Vowel_fr')

    triplet_num = "triplet" + str(int(row[0])+1)

    order_filename_info = dict(
        tripletid = [triplet_num],
        Stimulus_A = [stimulus_A],
        Stimulus_B = [stimulus_B],
        Stimulus_X = [stimulus_X],
        Corr_ans = [TGT],
        File_A = [file_A_full],
        File_B = [file_B_full],
        File_X = [file_X_full]
        )

    stimlist_info = dict(
        filename = [triplet_num],
        File1 = [file_A_full],
        File2 = [file_B_full],
        File3 = [file_X_full],
        CORR_ANS = [TGT]
        )

    distance_info = dict(
        CORR_ANS = [TGT],
        tripletid = [triplet_num],
        context = [context],
        file_X = [file_X_full],
        speaker_X = [speaker_X],
        vowel_X = [vowelTGT],
        word_X = [stimulus_X],
        file_OTH = [file_OTH_full],
        speaker_OTH = [speakerOTH],
        vowel_OTH = [vowelOTH],
        word_OTH = [stimulus_OTH],
        vowel_eng = [eng_vowel],
        word_fr = [fr_vowel],
        file_TGT = [file_TGT_full],
        speaker_TGT = [speakerTGT],
        vowel_TGT = [vowelTGT],
        word_TGT = [stimulus_TGT],
        )

    return (order_filename_info,stimlist_info,distance_info)




additional_table_info = pd.DataFrame()

for row in table.itertuples():

    order_dictionary = get_data_by_order(row, meta_table)[0]
    stim_dictionary = get_data_by_order(row, meta_table)[1]
    dist_dictionary = get_data_by_order(row, meta_table)[2]

    add_to_table = pd.DataFrame(order_dictionary)
    add_to_stimlist = pd.DataFrame(stim_dictionary)
    add_to_dist = pd.DataFrame(dist_dictionary)

    additional_table_info = additional_table_info.append(add_to_table)
    stimlist = stimlist.append(add_to_stimlist, ignore_index=True)
    distance_list = distance_list.append(add_to_dist, ignore_index=True)



new_table = pd.merge(table, additional_table_info, on="tripletid", how="outer")

new_table.to_csv("outputs/experimental_list_w_filenames.csv", index=False)
stimlist.to_csv("outputs/Stimuli_list.txt", index=False)
distance_list.to_csv("outputs/distance_list.csv", index=False)


