 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import pandas as pd
import sys

#read abkhazia lexicon.txt file
OUT_FOLD = sys.argv[1]

LANG = OUT_FOLD.split('/')[-1]

if LANG == 'eng':
    dict_c1 = {'Z':'Z', 'S':'S', 'F':'F', 'SH':'SH', 'V':'V'}
    dict_c2 = {'G':'G', 'B':'B', 'D':'D', 'P':'P', 'K':'K', \
    'Z':'Z', 'S':'S', 'F':'F', 'SH':'SH', 'V':'V'}
    dict_v = {'AA':'AA',
              'AE':'A', 
              'AH':'U', 
              'AO':'O', 
              'AW':'OU',
              'AY':'AY',
              'EH':'E', 
              'EY':'EY',
              'IH':'I', 
              'IY':'EE',
              'OW':'OW',
              'OY':'OY',
              'UH':'OO',
              'UW':'UW',
              'UW Y':'UY'}

elif LANG == 'fr':
    dict_c1 = {'z':'z', 's':'s', 'f':'f', 'ʃ':'ch', 'v':'v'}
    dict_c2 = {'p':'pe', 'ʃ':'che', 'b':'b', 'd':'d', 'k':'k', \
    'z':'z', 's':'sse', 'f':'ffe', 'ɡ':'gue', 'v':'ve'}
    dict_v = {'i':'i',  
              'ɛ':'è',
              'e':'é',
              'ə':'e',
              'ɛ̃':'in',
              'œ̃':'un',
              'œ':'oe',
              'ø':'eu',
              'y':'u',
              'u':'ou',
              'o':'au',
              'ɔ':'o',
              'ɔ̃':'on',
              'ɑ̃':'en',
              'a':'a'}


def make_combinations(c1_d, v_d, c2_d):
    all_cvcs = {}
    for c1 in c1_d.keys():
        for v in v_d.keys():
            for c2 in c2_d.keys():
                cvc_word = c1_d[c1] + v_d[v] + c2_d[c2]
                #cvc_phon = " ".join((c1, v, c2))
                cvc_phon =  {'p1':c1, 'p2':v, 'p3':c2}
                all_cvcs[cvc_word] = cvc_phon
    return all_cvcs


all_words = make_combinations(dict_c1, dict_v, dict_c2)

#new_lexicon = pd.DataFrame(all_words.items()).drop_duplicates()
new_lexicon = pd.DataFrame.from_dict(all_words, \
                orient='index', columns=['p1', 'p2', 'p3'])

uni_df = pd.DataFrame(new_lexicon.index)
uni_df['order1'] = 0
uni_df['order2'] = 1
uni_df['wrd'] = uni_df[0]
uni_df['wrd2'] = uni_df[0]
uni_df['prob'] = 0.0
uni_df = uni_df.drop(labels=0, axis=1)

uni_df.to_csv(OUT_FOLD + "/lm_all_cvcs.csv", sep=" ", \
                header=False, index=False)

new_lexicon.to_csv(OUT_FOLD + "/lexicon_all_cvcs.csv", \
                sep=" ", header=False)

