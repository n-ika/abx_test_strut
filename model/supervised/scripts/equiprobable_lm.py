import pandas as pd
import sys

#read abkhazia text.txt file
FILE = sys.argv[1]
COMP = sys.argv[2]
LEXICON = sys.argv[3]
OUT_FOLD = sys.argv[4]


text_df = pd.read_csv(FILE, sep=" ", header=0,\
                     names=['utt_id', 'text'])
comp_df = pd.read_csv(COMP, sep=",")
lexi_df = pd.read_csv(LEXICON, sep=" ", header=0,\
                     names=['utt_id', 'text']) 
text_df['good'] = 0

def match_arpa_to_lexicon(word, comp):
    comp_filt = comp[comp['arpa'] == word].reset_index()
    ortho_word = comp_filt['ortho'][0]
    return ortho_word


for row in text_df.itertuples():
    INDEX = getattr(row, 'Index')
    word = getattr(row, 'text')
    ortho_word = match_arpa_to_lexicon(word, comp_df)
    text_df.loc[INDEX,'good'] = ortho_word


unique = text_df['good'].unique()
uni_df = pd.DataFrame(unique)
uni_df['order1'] = 0
uni_df['order2'] = 1
uni_df['wrd'] = uni_df[0]
uni_df['wrd2'] = uni_df[0]
uni_df['prob'] = 0.0
uni_df = uni_df.drop(labels=0, axis=1)

text_df = text_df.drop(labels="text", axis=1)

text_df.to_csv(OUT_FOLD + "text.txt", sep=" ", header=False, index=False)
uni_df.to_csv(OUT_FOLD + "lm.csv", sep=" ", header=False, index=False)
