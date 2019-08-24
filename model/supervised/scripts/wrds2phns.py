#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Nika Jurov

import sys
import pandas as pd
import numpy as np
import Levenshtein
import os
import io

reload(sys)
sys.setdefaultencoding('utf-8')

LEXICON_FILE = sys.argv[1] # lexicon used for Abkhazia
TEXT_FILE = sys.argv[2] # text file with words to become phones
DECODINGS_FOLDER = sys.argv[3] # model's decoding - a text file
LANG = sys.argv[4] # which language to filter, string "en" or "fr"
#OUT_FILE = sys.argv[4] # lexicon in csv format

lexicon_file = io.open(LEXICON_FILE, 'r', encoding='utf-8') 
text_file = io.open(TEXT_FILE, 'r', encoding='utf-8')
levenshtein_folder = os.walk(DECODINGS_FOLDER)


def local_levenshtein_distance(orig_phone, decoded_phone):

    leven_dist = Levenshtein.distance(orig_phone, decoded_phone)
    return leven_dist


# def calculate_distances_dtw(orig_utt, decoded_utt):

#     if decoded_utt.shape[0] == 0:
#         decoded_utt = np.array(["X"])

#     distance_matrix = np.zeros((orig_utt.shape[0], decoded_utt.shape[0]))

#     for i in range(orig_utt.shape[0]):
#         for j in range(decoded_utt.shape[0]):
        
#             if (i==0) and (j==0):
#                 smallest_distance = 0
#             elif (i==0):
#                 smallest_distance = distance_matrix[i][j-1] 
#             elif (j==0):
#                 smallest_distance = distance_matrix[i-1][j]             
#             else:
#                 smallest_distance = min(distance_matrix[i-1][j],
#                                         distance_matrix[i][j-1],
#                                         distance_matrix[i-1][j-1])

#             distance_matrix[i][j] = smallest_distance \
#                                     + local_levenshtein_distance(orig_utt[i],\
#                                                                  decoded_utt[j])
#     shortest_dist = float(distance_matrix[-1][-1])/len(orig_utt)
#     return shortest_dist

def zero_if_equal(orig_utt_phone, decoded_utt_phone):
    if orig_utt_phone == decoded_utt_phone:
        cost = 0
    else:
        cost = 1
    return cost

def calculate_distances_dtw(orig_utt, decoded_utt):

    #if decoded_utt.shape[0] == 0:
    #    decoded_utt = np.array([" "])
    distance_matrix = np.zeros((orig_utt.shape[0] + 1, decoded_utt.shape[0] + 1))

    for i in range(1, orig_utt.shape[0]+1):
        distance_matrix[i][0] = i

    for j in range(1, decoded_utt.shape[0]+1):
        distance_matrix[0][j] = j

    for i in range(1, orig_utt.shape[0]+1):
        for j in range(1, decoded_utt.shape[0]+1):
            smallest_distance = min(distance_matrix[i-1][j] + 1,
                                    distance_matrix[i][j-1] + 1,
                                    distance_matrix[i-1][j-1] + \
                                    zero_if_equal(orig_utt[i-1],
                                                  decoded_utt[j-1]))
            distance_matrix[i][j] = smallest_distance

    shortest_dist = float(distance_matrix[-1][-1])/len(orig_utt)
    return shortest_dist
    


def lexicon2dict(lxcn_file):
    lexicon = {}
    for row in lxcn_file.readlines():
        each_element = row.split(" ")
        word = each_element[0:1][0].strip('[]')
        # phonemes = " ".join(each_element[1:]).strip('\n')
        each_element[-1] = each_element[-1].strip('\n')
        if '' in each_element:
            each_element.remove('')
        phonemes = np.array(each_element[1:])
        lexicon[word] = phonemes
    
    return lexicon


def text2dict(txt_file, lexicon):
    NOT_HERE = []
    transcription = {}
    for row_ in txt_file.readlines():
        each_element2 = row_.split(" ")
        id_utt = each_element2[0:1][0].strip('[]')
        utterance = each_element2[1:]
        phns_all = np.array([])
        for wrd in utterance:
            wrd = wrd.strip('\n').decode('utf-8')
            if wrd == "" or wrd == " ":
                pass
            elif wrd == "<unk>":
                phns_all = np.append(phns_all, "X")
            if wrd not in lexicon:
                NOT_HERE.append(wrd)
            else:
                phns = lexicon[wrd]
                phns_all = np.append(phns_all, phns)
        #transcription[id_utt] = " ".join(phns_all)
        transcription[id_utt] = phns_all
    print NOT_HERE
    return transcription



def cer(orig_text, decoded_text, lang="spk"):
    cer_dict = {}
    for utt in orig_text.keys():
        if lang in utt:
            orig_utt = orig_text[utt]
            decoded_utt = decoded_text[utt]
            #DTW
            cer_dict[utt] = calculate_distances_dtw(orig_utt,\
                                                    decoded_utt)
    return cer_dict



orig_lexicon = lexicon2dict(lexicon_file)
orig_text = text2dict(text_file, orig_lexicon)
cer_df = pd.DataFrame()

for root, dirs, files in levenshtein_folder:
    for decode_file in files:

        if decode_file.endswith("word.txt"):
            decoded_file = open(root + decode_file, 'r')
            decoded_text = text2dict(decoded_file, orig_lexicon)
            distances = cer(orig_text, decoded_text, LANG)
            dist_df = pd.DataFrame.from_dict(distances, orient='index')
            total_dist = dist_df[0].mean(axis=0)
            cer_df_row = pd.DataFrame({"file":[decode_file],\
                                       "cer":[float(total_dist)]})
            cer_df = cer_df.append(cer_df_row, ignore_index=True)
            print "Mean CER of {} is: {}".format(decode_file, float(total_dist))
            # dist_df.to_csv(root + decode_file.strip(".txt") + \
            #                 "_lvnstn.csv", header=False, sep=",")

        elif decode_file.endswith("phone.txt"):
            decoded_file = open(root + decode_file, 'r')
            decoded_text = lexicon2dict(decoded_file)
            distances = cer(orig_text, decoded_text, LANG)
            dist_df = pd.DataFrame.from_dict(distances, orient='index')
            total_dist = dist_df[0].mean(axis=0)
            cer_df_row = pd.DataFrame({"file":[decode_file], \
                                       "cer":[float(total_dist)]})
            cer_df = cer_df.append(cer_df_row, ignore_index=True)
            print "Mean CER of {} is: {}".format(decode_file, float(total_dist))
            # dist_df.to_csv(root + decode_file.strip(".txt") + \
            #                 "_lvnstn.csv", header=False, sep=",")

cer_df.to_csv(DECODINGS_FOLDER + "distances_cer_filtered.csv", \
                                 index=False)