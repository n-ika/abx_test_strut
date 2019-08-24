# Author: Nika Jurov

import h5features as h5f
import ABXpy.distances.metrics.dtw as dtw
import ABXpy.distances.metrics.kullback_leibler as kullback_leibler
import numpy as np
import pandas as pd
import sys
import os


POST_FOLDER = sys.argv[1]
STIM_TABLE = sys.argv[2]
DISTANCE_LIST = sys.argv[3]


posteriors_folder = os.walk(POST_FOLDER)
stim_backtraced = pd.read_csv(STIM_TABLE)
distance_list = pd.read_csv(DISTANCE_LIST)


def minimum_diff(time_pnt, times_arr):
    index = 0  
    smallest_difference = abs(time_pnt - times_arr[index])  

    for i, num in enumerate(times_arr):
        diff = abs(time_pnt - num) 

        if diff < smallest_difference: 
            index = i
            smallest_difference = diff

    return index

def extract_stim_vector(ABX_i, df, times_r, features_r):
    item = df.loc[ABX_i, 'utt']
    start_time = df.loc[ABX_i, 'stim_start']
    end_time = df.loc[ABX_i, 'stim_end']
    times_vector = times_r[item] # entire utt
    # find closest times to start and end of stimulus
    vect_start = minimum_diff(start_time, times_r[item])
    vect_end = minimum_diff(end_time, times_r[item])
    # find vector
    feat_vector = features_r[item][vect_start:vect_end + 1]

    return feat_vector

def dtw_kl_divergence(x, y):
    """ Kullback-Leibler divergence """
    if x.shape[0] > 0 and y.shape[0] > 0:
        d = dtw.dtw(x, y, kullback_leibler.kl_divergence, True)
    elif x.shape[0] == y.shape[0]:
        d = 0
    else:
        d = np.inf
    return d

def write_kl_to_column(distance_list, stim_backtraced, \
                        PG_file, root):
    """ Write distances into original table """

    hf5_file = root + PG_file
    times_r, features_r = h5f.read(hf5_file, 'features')
    items = h5f.Reader(hf5_file, 'features').items.data[0:]

    oth_x_array = np.array([])
    tgt_x_array = np.array([])

    for TRIP_NUM in range(1, 113):

        # select only item names which correspond to same triplet
        trip_id = 'triplet' + str(TRIP_NUM)
        filtered = stim_backtraced[stim_backtraced.tripletid == \
                                    trip_id].reset_index()

        
        oth_vector = extract_stim_vector(0, \
                            filtered, times_r, features_r)
        tgt_vector = extract_stim_vector(1, \
                            filtered, times_r, features_r)
        x_vector = extract_stim_vector(2, \
                            filtered, times_r, features_r)

        # get KL divergence for TGT-X and OTH-X
        kl_oth_x = dtw_kl_divergence(oth_vector, x_vector)
        kl_tgt_x = dtw_kl_divergence(tgt_vector, x_vector)

        # put them into an array
        oth_x_array = np.append(oth_x_array, kl_oth_x)
        tgt_x_array = np.append(tgt_x_array, kl_tgt_x)


    name_othX = PG_file.split('.')[0] + '_oth_x'
    name_tgtX = PG_file.split('.')[0] + '_tgt_x'

    distance_list[name_othX] = pd.Series(oth_x_array, \
                                        index=distance_list.index)
    distance_list[name_tgtX] = pd.Series(tgt_x_array, \
                                        index=distance_list.index)

    return distance_list

for root, dirs, files in posteriors_folder:
    for PG_file in files:
        if PG_file.endswith(".h5"):
            distance_list = write_kl_to_column(distance_list, \
                                                stim_backtraced, \
                                                PG_file, root)


# write all distances to csv
distance_list.to_csv(POST_FOLDER + "distances_supmodel_entw.csv", \
                                 index=False)
