import sys
import os
import itertools
import pickle


cwd = os.getcwd()

STIMULI_ENG = sys.argv[1]
STIMULI_FR = sys.argv[2]

unique_stimuli = cwd + "/pair_context_values.p"


# creates a dictionary with key as consonantal context,
# and the values are a list of the vowels that appear
# on the real stimuli list

def get_context_vowel_dict(stimuli_list):
    stim_list = []
    context_vowels = {}

    file_open = open(stimuli_list, 'r')
    for line in file_open.readlines():
        line = line.strip()
        stim_list.append(line)

    unique_stim = set(stim_list)

    # separate context and the vowel
    for stimulus in unique_stim:
        if stimulus[0:2] == "SH":
            char1 = "SH"
        else:
            char1 = stimulus[0]

        if stimulus[-2:] == "SH":
            char2 = "SH"
        else:
            char2 = stimulus[-1]

        context = char1 + "_" + char2
        no_first_letter = stimulus[len(char1):]
        vowel = no_first_letter[:-len(char2)]

        # find if key exists and append the value (V) to the exist. Vs
        if context_vowels.has_key(context):
            context_vowels.setdefault(context, []).append(vowel)

        # create new key & add value
        else:
            context_vowels[context] = [vowel]

    return context_vowels


# create all of the possible pairs of words with the same context

PAIR_CONTEXT_VALUES = []

eng_dict = get_context_vowel_dict(STIMULI_ENG)
fr_dict = get_context_vowel_dict(STIMULI_FR)

# context_vowels = dict(eng_dict.items() + fr_dict.items())
for key, value in eng_dict.items():
    eng_vowels = value
    fr_vowels = fr_dict[key]
    for pair in itertools.product(eng_vowels, fr_vowels):
            vowel_pair = pair[0] + "_" + pair[1]
            vowel_pair = tuple([vowel_pair, key])
            PAIR_CONTEXT_VALUES.append(vowel_pair)

# output is np.array of all existent pairs
pickle.dump(PAIR_CONTEXT_VALUES, open(unique_stimuli, "wb"))


# check whether the result is unique values only
# compare size of entire array:
# np.array(PAIR_CONTEXT_VALUES).size
# with unique rows only:
# np.unique(np.array(PAIR_CONTEXT_VALUES), axis=0).size
