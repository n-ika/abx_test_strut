###########################################
###CONCATENATE INTERVAL .wavs into full wav#
###########################################
#9 November by Amelia 
#takes a directory of intervals that have been normalized 
import pydub
import pandas as pd
import os 
import sys

#requires ffmpeg with libvorbis in order to make oggs
#brew install ffmpeg --with-libvorbis


# ARGUMENTS
folderpath = sys.argv[1] #path to directory of intervals 
stimfile = sys.argv[2] # stimlist, output of 
silencefile = sys.argv [3] #first silence between files A and B
outfolder = sys.argv [4] # folder for output files 

wav_folder = outfolder + "/wavs/"
mp3_folder = outfolder + "/mp3s/"
ogg_folder = outfolder + "/oggs/"

os.makedirs(wav_folder)
os.makedirs(mp3_folder)
os.makedirs(ogg_folder)

stimlist = pd.read_csv(stimfile)


from pydub import AudioSegment

silence1 = AudioSegment.from_wav(silencefile)
silence2 = AudioSegment.from_wav(silencefile)


for i in range (0,len(stimlist)):

    sound1 = AudioSegment.from_wav(folderpath + stimlist.loc[i,"File1"] +".wav")
    sound2 = AudioSegment.from_wav(folderpath + stimlist.loc[i,"File2"] +".wav")
    sound3 = AudioSegment.from_wav(folderpath + stimlist.loc[i,"File3"] +".wav")

    combined_sounds = sound1 + silence1 +sound2 + silence2  + sound3

    combined_sounds.export(wav_folder+stimlist.loc[i,"filename"]+".wav", format = "wav")
    combined_sounds.export(mp3_folder+stimlist.loc[i,"filename"]+".mp3", format = "mp3")
    combined_sounds.export(ogg_folder+stimlist.loc[i,"filename"]+".ogg", format = "ogg")


