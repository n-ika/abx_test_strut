# Author: Nika Jurov

import h5features as h5f
import ABXpy.distances.metrics.dtw as dtw
import ABXpy.distances.metrics.kullback_leibler as kullback_leibler
import numpy as np
import pandas as pd
import sys
import os


POST_FOLDER = sys.argv[1]
DISTANCE_LIST = sys.argv[2]


posteriors_folder = os.walk(POST_FOLDER)
distance_list = pd.read_csv(DISTANCE_LIST)


def dtw_kl_divergence(x, y):
    """ Kullback-Leibler divergence """
    if x.shape[0] > 0 and y.shape[0] > 0:
        d = dtw.dtw(x, y, kullback_leibler.kl_divergence, True)
    elif x.shape[0] == y.shape[0]:
        d = 0
    else:
        d = np.inf
    return d

def write_kl_to_column(distance_list, PG_file, root):
    """ Write distances into original table """

    hf5_file = root + PG_file
    times_r, features_r = h5f.read(hf5_file, 'features')
    items = h5f.Reader(hf5_file, 'features').items.data[0:]

    oth_x_array = np.array([])
    tgt_x_array = np.array([])

    for TRIP_NUM in range(1, 113):

        # select only item names which correspond to same triplet
        trip_id = 'triplet' + str('{0:03}'.format(TRIP_NUM))
        trip_items = [itm for itm in items if trip_id in itm]

        # trace the 01 = OTH, 02 = TGT, 03 = X
        item_oth = [oth for oth in trip_items if '_01' in oth][0]
        item_tgt = [tgt for tgt in trip_items if '_02' in tgt][0]
        item_x = [x for x in trip_items if '_03' in x][0]

        # find vectors
        feat_vector_oth = features_r[item_oth]
        feat_vector_tgt = features_r[item_tgt]
        feat_vector_x = features_r[item_x]
        # time_vector = times_r[item]

        # get KL divergence for TGT-X and OTH-X
        kl_oth_x = dtw_kl_divergence(feat_vector_oth, feat_vector_x)
        kl_tgt_x = dtw_kl_divergence(feat_vector_tgt, feat_vector_x)

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
                                                PG_file, root)


# write all distances to csv
distance_list.to_csv(POST_FOLDER + "distances_supmodel_ints.csv", \
                                 index=False)
