from textgrid import TextGrid
from pydub import AudioSegment
import sys

# sentence .wav
f_wav = sys.argv[1]
# .TextGrid for the sentence
file_tg = sys.argv[2]
# .wav of 500ms silence
silence_f = sys.argv[3]
# folder ./wavs to output
output_folder = sys.argv[4]


def get_annotated_words(textgrid_fn, tier_name):
    tg = TextGrid()
    tg.read(textgrid_fn)
    tier_i = tg.getNames().index(tier_name)
    return tg[tier_i]


audio = AudioSegment.from_wav(f_wav)
silence = AudioSegment.from_wav(silence_f)
tier = get_annotated_words(file_tg, "word")

count = 1
for interval in tier:
    label = interval.mark.strip()
    start_time = float(interval.minTime) * 1000
    end_time = float(interval.maxTime) * 1000
    word = audio[start_time:(end_time + 1)]
    combined_sounds = silence + word + silence
    count += 1

    combined_sounds.export(output_folder + label + "_" + \
                            str(count) + ".wav", format="wav")
