# Author: Nika Jurov

import pydub
import pandas as pd
import os 
import sys
import glob
from pydub import AudioSegment

INTERVALS = sys.argv[1]
SILENCE_FILE = sys.argv [2]
OUTPUT_FOLDER = sys.argv [3]

silence = AudioSegment.from_wav(SILENCE_FILE)


for int_file in glob.glob(INTERVALS + "*.wav"):

    interval = AudioSegment.from_wav(int_file)

    combined_sounds = silence + interval + silence

    int_name = int_file.split('/')[-1]

    combined_sounds.export(OUTPUT_FOLDER + int_name, format = "wav")