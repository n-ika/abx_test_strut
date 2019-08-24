# Author: Nika Jurov

from pydub import AudioSegment
import sys
import glob

folder = sys.argv[1]
#sound_file = sys.argv[2]


def normalize_amplitude(sound, target_dbfs):
    return sound.apply_gain(target_dbfs - sound.dBFS)

for sound_file in glob.glob(folder + "*.wav"):
    audio = AudioSegment.from_wav(sound_file)
    segment = normalize_amplitude(audio, -20)

    sound_name = sound_file.split("/")[-1].split(".")[0]
    segment.export(folder+sound_name+"normalized.mp3", format = "mp3")
    segment.export(folder+sound_name+"normalized.ogg", format = "ogg")
    segment.export(folder+sound_name+"normalized.wav", format = "wav")