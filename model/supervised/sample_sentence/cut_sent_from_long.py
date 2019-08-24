from pydub import AudioSegment
import sys
import pandas as pd

f_wav = sys.argv[1]
output_folder = sys.argv[2]

audio = AudioSegment.from_wav(f_wav)

# en - 0014.wav:
# segment = audio[737984:752120]
# fr - M02.wav :
segment = audio[4029134:4041171]

segment.export(output_folder + "/french_sentence.wav",
                               format="wav")

