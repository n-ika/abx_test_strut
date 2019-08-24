from python_speech_features import mfcc
import scipy.io.wavfile as wav
import os
import sys
import pandas as pd
import math

WAV_FOLDER = sys.argv[1]
OUT_FOLDER = sys.argv[2]

# source povey window: 
# https://github.com/kaldi-asr/kaldi/blob/master/src/feat/feature-window.cc

for sound_file in os.listdir(WAV_FOLDER):
    if sound_file.endswith('.wav'):
        wav_file = WAV_FOLDER + sound_file
        (rate,sig) = wav.read(wav_file)
        mfcc_feat = mfcc(sig,rate,winfunc=lambda n:\
                        pow((0.5 - 0.5*math.cos(0.025/n*2*math.pi)), 0.85))
        df = pd.DataFrame(mfcc_feat)
        df.to_csv(OUT_FOLDER + \
            sound_file.split('.')[0] + \
            "_mfcc.csv", index=False, header=False)