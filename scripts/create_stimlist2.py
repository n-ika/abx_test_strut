#this script creates a stimlist for an experiment 
#it is for situations in which the 

import random
import numpy as np
import simanneal
import sklearn.metrics
import pandas as pd
import collections
import os
import pickle
import argparse
import sys

from sklearn.metrics import normalized_mutual_info_score as nmi

class BinaryAnnealer(simanneal.Annealer):
    def __init__(self, meta_info, num_stim,
                    mono_english_speakers, mono_french_speakers,
                    bilingual_speakers, orders):
        assert len(mono_english_speakers) == len(mono_french_speakers)
        self.num_stim = num_stim
        state = np.zeros((self.num_stim, 6))
        simanneal.Annealer.__init__(self, state)

        self.orders = orders
        i = 0
        while i < self.num_stim:
            for order_index in range(len(self.orders)):
                self.set_order(i, order_index)
                i += 1

        self.mono_english_speakers = mono_english_speakers
        self.mono_french_speakers = mono_french_speakers
        self.n_mono_speakers = len(self.mono_english_speakers)
        self.bilingual_speakers = bilingual_speakers
        self.n_bilingual_speakers = len(self.bilingual_speakers)

        self.meta_info = meta_info
        self.items_en = self.meta_info\
                .loc[self.meta_info["language"] == "eng", ("vowel","context")]\
                .drop_duplicates()\
                .reset_index()
        self.items_fr = self.meta_info\
                .loc[self.meta_info["language"] == "fr", ("vowel","context")]\
                .drop_duplicates()\
                .reset_index()
        self.vowels_en = \
            self.items_en.loc[:,"vowel"].drop_duplicates().tolist()
        self.vowels_fr = \
            self.items_fr.loc[:,"vowel"].drop_duplicates().tolist()
        self.contexts = \
            self.meta_info.loc[:,"context"].drop_duplicates().tolist()
        self.n_possible_VVO = len(self.vowels_en)*len(self.vowels_fr)\
                                *len(self.orders)

    def order_to_mono_language(self, order):
        if (order == "EFE" or order == "FEE"):
            return "eng"
        else:
            return "fr"

    def order_index_to_mono_language(self, order_index):
        return(self.order_to_mono_language(self.orders[order_index]))

    def set_order(self, i, order_index):
        self.state[i,0] = order_index

    def get_order(self):
        return self.state[:,0]

    def set_vowel_en(self, i, vowel_en_index):
        self.state[i,1] = vowel_en_index

    def get_vowel_en(self):
        return self.state[:,1]

    def set_vowel_fr(self, i, vowel_fr_index):
        self.state[i,2] = vowel_fr_index

    def get_vowel_fr(self):
        return self.state[:,2]

    def set_context(self, i, context_index):
        self.state[i,3] = context_index

    def get_context(self):
        return self.state[:,3]

    def set_monolingual_speaker(self, i, monolingual_speaker_index):
        self.state[i,4] = monolingual_speaker_index

    def get_monolingual_speaker(self):
        return self.state[:,4]

    def set_bilingual_speakers(self, i, bilingual_speakers_index):
        self.state[i,5] = bilingual_speakers_index

    def get_bilingual_speakers(self):
        return self.state[:,5]

    def sample_item_pair(self):
        while True:
            item_en = random.randrange(self.items_en.shape[0])
            vowel_en = self.items_en.loc[item_en,"vowel"]
            vowel_index_en = self.vowels_en.index(vowel_en)
            context = self.items_en.loc[item_en,"context"]
            context_index = self.contexts.index(context)
            matching_fr = self.items_fr\
                    .loc[self.items_fr["context"]==context,:]\
                    .reset_index()
            if matching_fr.shape[0] > 0:
                break
        item_fr = random.randrange(matching_fr.shape[0])
        vowel_fr = matching_fr.loc[item_fr,"vowel"]
        vowel_index_fr = self.vowels_fr.index(vowel_fr)
        return vowel_en, vowel_index_en, vowel_fr, vowel_index_fr,\
                context, context_index

    def check_existing(self, vowel, context, speaker):
        rows_matching = (self.meta_info['vowel'] == vowel) \
                        & (self.meta_info['context'] == context) \
                        & (self.meta_info['speaker'] == speaker)
        return rows_matching.any()

    def move(self):
        all_exist = False
        while not all_exist:
            i = random.randrange(self.num_stim)
            order_index = int(self.get_order()[i])
            vowel_en, vowel_index_en, vowel_fr, vowel_index_fr, \
                    context, context_index = self.sample_item_pair()
            mono_index = random.randrange(self.n_mono_speakers)
            biling_index = random.randrange(self.n_bilingual_speakers)
            speaker_en, speaker_fr = \
                    self.bilingual_speakers[biling_index]
            if self.order_index_to_mono_language(order_index) == "eng":
                vowel_mono = vowel_en
                speaker_mono = self.mono_english_speakers[mono_index]
            else:
                vowel_mono = vowel_fr
                speaker_mono = self.mono_french_speakers[mono_index]
            all_exist = self.check_existing(vowel_en, context, speaker_en) \
                      and self.check_existing(vowel_fr, context, speaker_fr) \
                      and self.check_existing(vowel_mono, context, speaker_mono)
        self.set_vowel_en(i, vowel_index_en)
        self.set_vowel_fr(i, vowel_index_fr)
        self.set_context(i, context_index)
        self.set_monolingual_speaker(i, mono_index)
        self.set_bilingual_speakers(i, biling_index)


    def n_VVO(self):
        unique = {tuple(row) for row in self.state[:,(0,1,2)]}
        return len(unique)

    def cost_values(self):
        return {"Predict context from monolingual speaker":
                    nmi(self.get_context(), self.get_monolingual_speaker()),
                "Predict context from bilingual speaker":
                    nmi(self.get_context(), self.get_bilingual_speakers()),
                "Predict English vowel from French vowel":
                    nmi(self.get_vowel_en(), self.get_vowel_fr()),
                "Number of missing vowel-vowel-order combinations":
                    self.n_possible_VVO - self.n_VVO(),
                "Predict English vowel from context":
                    nmi(self.get_context(), self.get_vowel_en()),
                "Predict French vowel from context":
                    nmi(self.get_context(), self.get_vowel_fr()),
                "Predict English vowel from monolingual speaker":
                    nmi(self.get_vowel_en(), self.get_monolingual_speaker()),
                "Predict French vowel from monolingual speaker":
                    nmi(self.get_vowel_fr(), self.get_monolingual_speaker()),
                "Predict English vowel from bilingual speakers":
                    nmi(self.get_vowel_en(), self.get_bilingual_speakers()),
                "Predict French from bilingual speakers":
                    nmi(self.get_vowel_fr(), self.get_bilingual_speakers()),
                "Predict order from context":
                    nmi(self.get_context(), self.get_order()),
                "Predict order from monolingual speaker":
                    nmi(self.get_context(), self.get_monolingual_speaker()),
                "Predict order from bilingual speaker":
                    nmi(self.get_order(), self.get_bilingual_speakers()),
                "Predict monolingual speaker from bilingual speaker":
                    nmi(self.get_bilingual_speakers(),
                        self.get_monolingual_speaker())
                }

    def energy(self):
        costs = self.cost_values()
        return sum(costs.values())\
                + 9*costs["Number of missing vowel-vowel-order combinations"]

    def to_data_frame(self):
        result = pd.DataFrame({
            "Order": [self.orders[int(i)] for i in self.state[:,0]],
            "Vowel_EN": [self.vowels_en[int(i)] for i in self.state[:,1]],
            "Vowel_FR": [self.vowels_fr[int(i)] for i in self.state[:,2]],
            "Context": [self.contexts[int(i)] for i in self.state[:,3]],
            "Mono_spk": np.nan,
            "Bilingual_spk_EN": [self.bilingual_speakers[int(i)][0]\
                                    for i in self.state[:,5]],
            "Bilingual_spk_FR": [self.bilingual_speakers[int(i)][1]\
                                    for i in self.state[:,5]]
            })
        for i in range(result.shape[0]):
            if self.order_to_mono_language(result.loc[i,"Order"]) == "eng":
                result.loc[i,"Mono_spk"] = \
                        self.mono_english_speakers[int(self.state[i,4])]
            else:
                result.loc[i,"Mono_spk"] = \
                        self.mono_french_speakers[int(self.state[i,4])]
        return result

def BUILD_ARGPARSE():
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--nsteps', help="Number of iterations",
            type=int, default=8000)
    parser.add_argument('--start-temp', help="Starting temperature",
            type=float, default=10)
    parser.add_argument('--min-temp', help="Minimum temperature",
            type=float, default=0.00001)
    parser.add_argument('--seed', help="Random seed for annealer",
            type=int, default=None)
    parser.add_argument('--mapping-seed',
            help="Random seed for permutations of factor values",
            type=int, default=None)
    parser.add_argument('num_trials',
            help="Total number of trials to select",
            type=int)
    parser.add_argument('input_table', help="Name of the meta info table",
            type=str)
    parser.add_argument('output_file', help="Name of the output file",
            type=str)
    return parser

if __name__ == "__main__":
    parser = BUILD_ARGPARSE()
    args = parser.parse_args(sys.argv[1:])

    meta_info = pd.read_csv(args.input_table)

    if args.seed is not None:
        random.seed(args.seed)

    MONO_ENGLISH_SPEAKERS = ["ewan", "jeremy"]
    MONO_FRENCH_SPEAKERS = ["remi", "marc"]
    BILINGUAL_SPEAKERS = [("veronique", "cecilia"), ("cecilia", "veronique")]
    ORDERS = ["EFE", "EFF", "FEE", "FEF"]

    random_m = random.Random()
    if args.mapping_seed is not None:
        random_m.seed(args.mapping_seed)
    # FIXME - Shuffle index-value mappings using random_m

    opt = BinaryAnnealer(meta_info, args.num_trials,
                            MONO_ENGLISH_SPEAKERS, MONO_FRENCH_SPEAKERS,
                            BILINGUAL_SPEAKERS, ORDERS)
    opt.steps = args.nsteps
    opt.Tmax = args.start_temp
    opt.Tmin = args.min_temp
    opt.anneal()
    opt.to_data_frame().to_csv(args.output_file, index=False)

    print(opt.cost_values())

