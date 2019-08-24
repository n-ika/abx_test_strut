# Author: Nika Jurov

import kaldi_io
import scipy.spatial
import ABXpy.distances.metrics.dtw as dtw
import ABXpy.distances.metrics.kullback_leibler as kullback_leibler
import numpy as np
import pandas as pd
import sys
import os


DIST_FOLDER = sys.argv[1]
DISTANCE_LIST = sys.argv[2]


distance_list = pd.read_csv(DISTANCE_LIST)
pqkmean_folder = os.walk(DIST_FOLDER)


def dtw_kl_divergence(x, y):
    """ Kullback-Leibler divergence """
    # times on rows, features on columns
    if x.shape[0] > 0 and y.shape[0] > 0:
        d = dtw.dtw(x, y, kullback_leibler.kl_divergence, True)
    elif x.shape[0] == y.shape[0]:
        d = 0
    else:
        d = np.inf
    return d

def write_kl_to_column(distance_list, folder_path, ID):
    """ Write distances into original table """
    #dist_files = os.listdir(root)
    oth_x_array = np.array([])
    tgt_x_array = np.array([])

    for TRIP_NUM in range(1, 113):

        # select only item names which correspond to same triplet
        trip_id = 'triplet' + str('{0:03}'.format(TRIP_NUM))

        # trace the 01 = OTH, 02 = TGT, 03 = X
        # item_oth = trip_id + '_01'
        # item_tgt = trip_id + '_02'
        # item_x = trip_id + '_03'

        item_oth = trip_id + '_OTH'
        item_tgt = trip_id + '_TGT'
        item_x = trip_id + '_X'

        # find vectors
        # feat_vector_oth = pd.read_csv(folder_path + item_oth + '.csv')
        # feat_vector_tgt = pd.read_csv(folder_path + item_tgt + '.csv')
        # feat_vector_x = pd.read_csv(folder_path + item_x + '.csv')
        feat_vector_oth = np.load(folder_path + item_oth + '.npy')
        feat_vector_tgt = np.load(folder_path + item_tgt + '.npy')
        feat_vector_x = np.load(folder_path + item_x + '.npy')
        kl_oth_x = dtw_kl_divergence(feat_vector_oth, feat_vector_x)
        kl_tgt_x = dtw_kl_divergence(feat_vector_tgt, feat_vector_x)

        # put them into an array
        oth_x_array = np.append(oth_x_array, kl_oth_x)
        tgt_x_array = np.append(tgt_x_array, kl_tgt_x)


    ID_inv = ID.split('_')[-1] + "_" + ID.split('_')[0]
    distance_list[ID_inv + '_kmean_oth_x'] = pd.Series(oth_x_array, \
                                        index=distance_list.index)
    distance_list[ID_inv + '_kmean_tgt_x'] = pd.Series(tgt_x_array, \
                                        index=distance_list.index)

    return distance_list

for root, dirs_pq, files in pqkmean_folder:
    for dir_pq in dirs_pq:
        if dir_pq == "softmax_dist":
            dist_path = '/'.join((root, dir_pq)) + "/"
            ID = root.split('/')[-1]
            distance_list = write_kl_to_column(distance_list, \
                                        dist_path, ID)
# write all distances to csv
distance_list.to_csv(DIST_FOLDER + "/distances_kmeans" + ".csv", \
                                         index=False)
