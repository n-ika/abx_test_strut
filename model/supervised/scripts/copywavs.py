import shutil
import sys

FOLDER = sys.argv[1]

old_name = FOLDER + "wav_001.wav"

for i in range (2, 751):
    new_name = FOLDER + "wav_" + str('{0:03}'.format(i)) + ".wav"
    shutil.copy(old_name, new_name)