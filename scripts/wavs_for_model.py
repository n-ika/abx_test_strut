# Author: Nika Jurov

import pydub
import pandas as pd
import os 
import sys
from pydub import AudioSegment

folderpath = sys.argv[1] # intervals in .wav format
stimfile = sys.argv[2] # distance_list.csv, the list where filenames are
outfolder = sys.argv [3] # where to output files 

wav_folder = outfolder + "/wavs_for_model/"

os.makedirs(wav_folder)

stimlist = pd.read_csv(stimfile)

def normalize_amplitude(sound, target_dbfs):
    return sound.apply_gain(target_dbfs - sound.dBFS)



for i in range (0,len(stimlist)):

    sound_OTH = AudioSegment.from_wav(folderpath + stimlist.loc[i,"file_OTH"] +".wav")
    sound_TGT = AudioSegment.from_wav(folderpath + stimlist.loc[i,"file_TGT"] +".wav")
    sound_X = AudioSegment.from_wav(folderpath + stimlist.loc[i,"file_X"] +".wav")

    sound_OTH = normalize_amplitude(sound_OTH, -20)
    sound_TGT = normalize_amplitude(sound_TGT, -20)
    sound_X = normalize_amplitude(sound_X, -20)


    sound_OTH.export(wav_folder + stimlist.loc[i,"tripletid"] + \
                    "_OTH" + ".wav", format = "wav")
    sound_TGT.export(wav_folder + stimlist.loc[i,"tripletid"] + \
                    "_TGT" + ".wav", format = "wav")
    sound_X.export(wav_folder + stimlist.loc[i,"tripletid"] + \
                    "_X" + ".wav", format = "wav")


