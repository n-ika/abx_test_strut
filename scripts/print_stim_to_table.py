# Author: Nika Jurov

# The output list is generated with stimuli names
# that is later used for LMEDS experiment.
# The input folder is the folder containing the
# experiment stimuli and the output is a text file
# to be used as the experiment sequence file.


import glob
import sys

CONCATENATION_FOLDER = sys.argv[1] # folder with all the concatenated stimuli
LMEDS_SEQUENCE = sys.argv[2] # output file

with open(LMEDS_SEQUENCE, 'w') as lmeds_file:
    for wav in glob.glob(CONCATENATION_FOLDER + '*.wav'):
        wav_filename = wav.split("/")[-1].strip(".wav")
        new_line = "media_choice prot_catch_trial audio 0.5 1 1" + \
             "[[" + wav_filename + \
             "]] [1 2] bindPlayKeyIDList=[space] bindResponseKeyIDList=[f j]"
        print >> lmeds_file, new_line