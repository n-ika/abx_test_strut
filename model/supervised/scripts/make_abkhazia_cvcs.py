#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import sys

# must contain folders ./fr and ./eng 
# w/ small_lexicon.txt and text.txt
MAIN_FOLDER = sys.argv[1] 
L1 = sys.argv[2] # for language we want to do this

if L1 == "fr":
    L2 = "eng"
else:
    L2 = "fr"

# read abkhazia text.txt file from the *other* language - L2
TEXT_L2 = MAIN_FOLDER + L2 + "/text.txt"
TEXT_L1 = MAIN_FOLDER + L1 + "/text.txt"
LEXICON_L2 = MAIN_FOLDER + L2 + "/small_lexicon.txt" 
LEXICON_L1 = MAIN_FOLDER + L1 + "/small_lexicon.txt"
OUT_FOLDER = MAIN_FOLDER + L1


text_L2 = pd.read_csv(TEXT_L2, sep=" ", \
                     names=['utt_id', 'text'])
text_L1 = pd.read_csv(TEXT_L1, sep=" ", \
                     names=['utt_id', 'text'])
lexi_L1 = pd.read_csv(LEXICON_L1, sep=" ", \
                     names=['word', 'p1', 'p2', 'p3'])
lexi_L2 = pd.read_csv(LEXICON_L2, sep=" ", \
                     names=['word', 'p1', 'p2', 'p3'])

# translates L2 phone to L1 phone
# target en phones: AE, UH, IH, AH
# target fr phones: a, ɛ, i, œ, ɔ, u, y
# output: word in L1 with 3 phonemes
def translate(filtered_df):

    v2v = {'AE':'e', 
           'AH':'eu',
           'IH':'in', 
           'UH':'on',
           'ɛ':'E',
           'œ':'OW',
           'u':'UW',
           'y':'UY',
           'a':'AA',
           'i':'EE',
           'ɔ':'O'}

    v2arpa = {'E':'EH',
             'OW':'OW',
             'UW':'UW',
             'UY':'UW Y',
             'AA':'AA',
             'EE':'IY',
             'O':'AO',
             'e':'ə', 
             'eu':'ø',
             'in':'ɛ̃', 
             'on':'ɔ̃'}

    c2arpa = {'z':'z', 's':'s', 'f':'f', 'ch':'ʃ', 'v':'v', \
              'Z':'Z', 'S':'S', 'F':'F', 'SH':'SH', 'V':'V', \
              'G':'G', 'B':'B', 'D':'D', 'P':'P', 'K':'K', \
              'pe':'p', 'che':'ʃ', 'b':'b', 'd':'d', 'k':'k', \
              'sse':'s', 'ffe':'f', 'gue':'ɡ', 've':'v'}

    dict_c1 = {'Z':'z', 'S':'s', 'F':'f', 'SH':'ch', 'V':'v',\
               'z':'Z', 's':'S', 'f':'F', 'ʃ':'SH', 'v':'V'}

    dict_c2 = {'ɡ':'G', 'b':'B', 'd':'D', 'p':'P', 'k':'K', \
               'z':'Z', 's':'S', 'f':'F', 'ʃ':'SH', 'v':'V', \
               'P':'pe', 'SH':'che', 'B':'b', 'D':'d', 'K':'k', \
               'Z':'z', 'S':'sse', 'F':'ffe', 'G':'gue', 'V':'ve'}

    p1 = filtered_df.loc[0,'p1']
    p2 = filtered_df.loc[0,'p2']
    p3 = filtered_df.loc[0,'p3']

    c1 = dict_c1[p1]
    v = v2v[p2]
    c2 = dict_c2[p3]

    translated_word = c1 + v + c2

    return {'word': translated_word, 'p1': c2arpa[c1], \
            'p2': v2arpa[v], 'p3':c2arpa[c2]}


# makes equip. lm: 0 1 wrd wrd 0.0
def equiprobable_lm(text_df):
    unique = text_df['text'].unique()
    uni_df = pd.DataFrame(unique)
    uni_df['order1'] = 0
    uni_df['order2'] = 1
    uni_df['wrd'] = uni_df[0]
    uni_df['wrd2'] = uni_df[0]
    uni_df['prob'] = 0.0
    uni_df = uni_df.drop(labels=0, axis=1)

    return uni_df


# make a lexicon & text containing 
# words from L1 and words from L2
i = 0
new_lexi = pd.DataFrame(columns=['word', 'p1', 'p2', 'p3'])
new_text = pd.DataFrame(columns=['utt_id', 'text'])
for row in text_L2.itertuples():
    word = getattr(row, 'text')
    utt_id = getattr(row, 'utt_id')
    filtered = lexi_L2[lexi_L2['word'] == word].reset_index()
    new = translate(filtered)
    new_lexi.loc[i] = new
    new_text.loc[i] = {'utt_id': utt_id,\
                       'text': new['word']}
    i += 1


fren_lexi = lexi_L1.append(new_lexi.drop_duplicates(), \
                ignore_index=True)
fren_text = text_L1.append(new_text, \
                ignore_index=True)

equi_lm = equiprobable_lm(fren_text)

fren_lexi.to_csv(OUT_FOLDER + "/lexicon_fren.csv", \
                sep=" ", header=False, index=False)
fren_text.to_csv(OUT_FOLDER + "/text_fren.csv", \
                sep=" ", header=False, index=False)
equi_lm.to_csv(OUT_FOLDER + "/lm_fren.csv", \
                sep=" ", header=False, index=False)