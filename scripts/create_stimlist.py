#this script creates a stimlist for an experiment 
#it is for situations in which the 

import random
import numpy as np
import simanneal
import sklearn.metrics
import pandas as pd
import collections
import os


#first, define the fixed structure. This is the part of the design
#which you want done in its entirety, and it also constrains the number of stimuli


#here, we have 28 comparisons of segments and 4 orders, and we want to counterbalance them. 
#this determines the length of the experiment (28*4= 112 trials)
NUM_ORDERS = 4 # #what order segments in pair are in (PQP,QPP,PQQ,QPQ)
NUM_VOWEL_PAIRS = 28 # (number of segment comparisons) 

NUM_STIM = NUM_VOWEL_PAIRS*NUM_ORDERS

MAX_REPETITIONS_WITHIN_COMPARISON = NUM_ORDERS

#SAMPLED

#for all of the above trials, we want divide evenly


# to be each of the following, and we don't want 
#these two to be predictive of the fixed structure 
NUM_CONTEXTS = 52 
NUM_MONOLINGUAL_SPEAKER = 2 # 2 per language 
NUM_BILINGUAL_SPEAKER = 2 # 2 different options for TGT

#define columns for a matrix which has each of these four factors as a column
COL_ORDER = 0
COL_VOWEL_PAIRS = 1
COL_CONTEXT = 2
COL_MONOLINGUAL_SPEAKER = 3
COL_BILINGUAL_SPEAKER = 4


#define several functions that will be used to create the .csv 

#this counts how many times something is duplicated
def num_duplicates(x):
    vals = collections.OrderedDict()
    for s in x:
        s_tup = tuple(s)
        if s_tup in vals:
            vals[s_tup] += 1
        else:
            vals[s_tup] = 0.
    return sum(vals.values())



#now we are defining the number of repetitions of the fixed part 
def repetitions_within_vowel_pair(stim_list): # FIXME
    result = 0
    for vp in range(NUM_VOWEL_PAIRS):
        items_vp = stim_list[stim_list[:,COL_VOWEL_PAIRS]==vp,:]
        result += num_duplicates(items_comp[:,(COL_CONTEXT,COL_MONOLINGUAL_SPEAKER)]) \
                + num_duplicates(items_comp[:,(COL_CONTEXT,COL_BILINGUAL_SPEAKER)])
    return result


#there are no more global repetitions 
#def repetitions_global(stim_list):
#    result = 0
#    for em in range(NUM_EMOTIONS*2):
#        e1_match = stim_list[(stim_list[:,COL_EM1]==em),:]
#        e2_match = stim_list[(stim_list[:,COL_EM2]==em),:]
#        result += num_duplicates(e1_match[:,(COL_SENTENCE,COL_SPEAKER)]) \
#                + num_duplicates(e2_match[:,(COL_SENTENCE,COL_SPEAKER)])
#    return result


#

def other(e):
    return [x for x in range(NUM_ORDERS) if x != e]


#sentence = context 
#speakers = speakers

def cost_values(solution):
    pred_cont_from_ml_spk = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_CONTEXT],
            solution[:,COL_MONOLINGUAL_SPEAKER])
    pred_cont_from_bl_spk = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_CONTEXT],
            solution[:,COL_BILINGUAL_SPEAKER])

    pred_comp_from_cont = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_VOWEL_PAIRS],
            solution[:,COL_CONTEXT])
    pred_comp_from_ml_spk = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_VOWEL_PAIRS],
            solution[:,COL_MONOLINGUAL_SPEAKER])
    pred_comp_from_bl_spk = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_VOWEL_PAIRS],
            solution[:,COL_BILINGUAL_SPEAKER])   

    pred_ord_from_cont = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_ORDER],
            solution[:,COL_CONTEXT])
    pred_ord_from_ml_spk = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_ORDER],
            solution[:,COL_MONOLINGUAL_SPEAKER])
    pred_ord_from_bl_spk = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_ORDER],
            solution[:,COL_BILINGUAL_SPEAKER])

    pred_ml_spk_from_bl_spk = sklearn.metrics.normalized_mutual_info_score(
            solution[:,COL_MONOLINGUAL_SPEAKER],
            solution[:,COL_BILINGUAL_SPEAKER])

    #FIXME
#    repetitions_within_comparison_ = repetitions_within_comparison(solution)
#    norm_repetitions_within_comparison = repetitions_within_comparison_\
#                                        /MAX_REPETITIONS_WITHIN_COMPARISON # FIXME

    return {"Predict context from monolingual speaker": pred_cont_from_ml_spk,
            "Predict context from bilingual speaker": pred_cont_from_bl_spk,
    #double check if solutions are very different with and without next line
            #"Normalized repetitions within comparison x 10":
            #    norm_repetitions_within_comparison*10,
            "Predict comparison from context": pred_comp_from_cont,
            "Predict comparison from monolingual speaker": pred_comp_from_ml_spk,
            "Predict comparison from bilingual speaker": pred_comp_from_bl_spk,
            "Predict order from context": pred_ord_from_cont,
            "Predict order from monolingual speaker": pred_ord_from_ml_spk,
            "Predict order from bilingual speaker": pred_ord_from_bl_spk,
            "Predict monolingual speaker from bilingual speaker": pred_ml_spk_from_bl_spk,
            }
#        return sklearn.metrics.mutual_info_score(self.state[:,2],
#                self.state[:,3])    

class BinaryAnnealer(simanneal.Annealer):
    def move(self):
        stim = random.randrange(NUM_STIM)
        self.state[stim,COL_CONTEXT] = random.randrange(NUM_CONTEXTS)
        self.state[stim,COL_MONOLINGUAL_SPEAKER] = random.randrange(NUM_MONOLINGUAL_SPEAKER)
        self.state[stim,COL_BILINGUAL_SPEAKER] = random.randrange(NUM_BILINGUAL_SPEAKER)

    def energy(self):
        values = cost_values(self.state)
        return sum(values.values())

# PARAMS
output_file = "stimlist.csv"
read_from_last = True
n_steps = 8000
t_min = 0.00001
seed = 24


# if not read_from_last:
t_max = 10
stim_list = np.zeros((NUM_STIM, 5)) # create an empty matrix with the right number of cols 
i = 0
for vp in range(NUM_VOWEL_PAIRS):
        stim_list[i,COL_ORDER] = 0
        stim_list[i,COL_VOWEL_PAIRS] = vp
        i += 1
        stim_list[i,COL_ORDER] = 1
        stim_list[i,COL_VOWEL_PAIRS] = vp
        i += 1
        stim_list[i,COL_ORDER] = 2
        stim_list[i,COL_VOWEL_PAIRS] = vp
        i += 1
        stim_list[i,COL_ORDER] = 3
        stim_list[i,COL_VOWEL_PAIRS] = vp
        i += 1
# else:
#     t_max = 1
    
#     stim_list = pd.read_csv(output_file).as_matrix()
    
random.seed(seed)
    
opt = BinaryAnnealer(stim_list)
opt.steps = n_steps
opt.Tmax = t_max
opt.Tmin = t_min
solution = opt.anneal()

#print(solution)
print(cost_values(solution[0]))
s_df = pd.DataFrame(solution[0])
s_df.columns = ['ORDER','VOWEL_PAIRS','CONTEXT','MONOLINGUAL_SPEAKER','BILINGUAL_SPEAKER']
s_df.to_csv(output_file, index=False)