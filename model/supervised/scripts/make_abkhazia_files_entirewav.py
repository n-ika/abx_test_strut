# Author: Nika Jurov

import pandas as pd
import numpy as np
import sys
import csv


INPUT_TABLE = sys.argv[1]
OUTPUT_FOLDER = sys.argv[2]

table = pd.read_csv(INPUT_TABLE)

segments = pd.DataFrame()
utt2spk = pd.DataFrame()
text = pd.DataFrame()


def get_speaker_num(spk_name):

    if spk_name == "vero_full_en":
        spk_num = "01"
    elif spk_name == "vero_full_fr":
        spk_num = "02"
    elif spk_name == "maur_full_en":
        spk_num = "03"
    elif spk_name == "maur_full_fr":
        spk_num = "04"
    elif spk_name == "remi_full_fr":
        spk_num = "05"
    elif spk_name == "marc_full_fr":
        spk_num = "06"
    elif spk_name == "jere_full_en":
        spk_num = "07"
    elif spk_name == "ewan_full_en":
        spk_num = "08"
    return spk_num

def make_files(table, spk_file):

    segments = pd.DataFrame()
    utt2spk = pd.DataFrame()
    text = pd.DataFrame()

    INDEX = 1

    spk_table = table[table['filename'] == spk_file]

    for row in spk_table.itertuples():

        utterance = getattr(row, 'utt')
        file_name = getattr(row, 'filename')
        start_time = getattr(row, 'start')
        end_time = getattr(row, 'end')

        filename = file_name + ".wav"
        language = file_name.split('_')[2].lower()
        if language == "eng":
            language = "en"

        spk = file_name.split('_')[0].lower()
        spk_num = "spk" + get_speaker_num(file_name)    

        utt_num = "utt_" + language + get_speaker_num(file_name) \
                    n
        
        utt_id = spk_num + "_" + utt_num

        INDEX += 1

        # segments = utt_id + filename + start & end time
        segments_add = pd.DataFrame([[utt_id, filename, \
                                    start_time, end_time]])

        # utt2spk = utt_id + spk_num
        utt2spk_add = pd.DataFrame([[utt_id, spk_num]])
    
        # text = utt_id + word
        text_add = pd.DataFrame([[utt_id, utterance]])

        segments = segments.append(segments_add, ignore_index=True)
        utt2spk = utt2spk.append(utt2spk_add, ignore_index=True)
        text = text.append(text_add, ignore_index=True)

    return (segments, utt2spk, text)

for wav_file in table['filename'].unique():
    abk_files = make_files(table, wav_file)
    segments = segments.append(abk_files[0], ignore_index=True)
    utt2spk = utt2spk.append(abk_files[1], ignore_index=True)
    text = text.append(abk_files[2], ignore_index=True)


segments.to_csv(OUTPUT_FOLDER + "/segments.txt", \
                sep=' ', header=False, index=False)
utt2spk.to_csv(OUTPUT_FOLDER + "/utt2spk.txt", \
                sep=' ', header=False, index=False)
text.to_csv(OUTPUT_FOLDER + "/text.txt", sep=' ', \
                header=False, index=False, \
                quoting=csv.QUOTE_NONE, escapechar=' ')

