# Author: Nika Jurov

# This script needs as arguments the folder (with MFCCs in .csv format)
# and a new folder where normalized values will be written for each file
# in the same format.
# Normalized values are normalized for each speaker (per every speaker,
# the mean is subtracted and then divided by the standard deviation).
# The mean and the st. dev. are obtained for all speech vectors produced
# by some speaker.



import pandas as pd
import numpy as np
import glob
import os
import sys


MFCC_FOLDER = sys.argv[1]
MFCC_FOLDER_NORM = sys.argv[2]

filenames = os.listdir(MFCC_FOLDER)


def get_speaker_names(filenames):
    speakers = np.array([])
    for filename in filenames:
        spk_name = filename.split("_")[0]
        speakers = np.append(speakers,spk_name)
    speakers = np.unique(speakers)
    return speakers


def normalize_values(spk_filename, mean_values, std_devs):
    vectors = pd.read_csv(spk_filename, header=None)
    minus_mean = vectors.subtract(pd.Series(mean_values), axis=0)
    norm_vectors = minus_mean.divide(pd.Series(std_devs), axis=0)
    write_norm_values(spk_filename, norm_vectors)


def find_mean_std(feature_values):
    mn = np.mean(feature_values)
    sd = np.std(feature_values)

    return (mn, sd)


def regroup_vectors_by_speaker(speakers, folder):
    for speaker in speakers:
        spk_files = glob.glob(MFCC_FOLDER + speaker + '*.csv')
        mean_values = np.array([])
        std_devs = np.array([])
        for i in range(13):
            features = np.array([])
            for spk_filename in spk_files:
                spk_file = pd.read_csv(spk_filename, header=None)
                features = np.append(features, spk_file.loc[i])
            mean_values = np.append(mean_values, find_mean_std(features)[0])
            std_devs = np.append(std_devs, find_mean_std(features)[1])
        for spk_filename in spk_files:
            normalize_values(spk_filename, mean_values, std_devs)



def write_norm_values(filename, norm_vectors):
    name = filename.split("/")[-1] 
    new_name = name.split(".")[0] + "_norm.csv"
    norm_vectors.to_csv(MFCC_FOLDER_NORM + name, header=False, index=False)


speakers = get_speaker_names(filenames)
regroup_vectors_by_speaker(speakers, MFCC_FOLDER)

