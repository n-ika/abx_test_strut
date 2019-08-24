from shennong.audio import Audio
from shennong.features.processor.bottleneck import BottleneckProcessor
import pandas as pd
import numpy as np
import scipy.spatial
import os
import sys


WAV_FOLDER = sys.argv[1] # stimuli in .wav
OUT_NPZ_FILE = sys.argv[2] 


all_features = {}

# get bottleneck features of all .wav files (stimuli)
for root, dirs, files in os.walk(WAV_FOLDER):
    for wav_file in files:
        if wav_file.endswith(".wav"):
            audio = Audio.load(root + wav_file)
            all_features[wav_file] = audio


processor = BottleneckProcessor(weights='BabelMulti')
features = processor.process(all_features)

np.savez_compressed(OUT_NPZ_FILE, features)


# features.items()
# features['triplet001_OTH.wav']
