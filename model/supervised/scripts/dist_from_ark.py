# Author: Nika Jurov

import kaldi_io
import scipy.spatial
import h5features as h5f
import ABXpy.distances.metrics.dtw as dtw
import ABXpy.distances.metrics.kullback_leibler as kullback_leibler
import numpy as np
import pandas as pd
import sys
import os


ARK_FOLDER = sys.argv[1]
DISTANCE_LIST = sys.argv[2]

ark_folder = os.walk(ARK_FOLDER)
distance_list = pd.read_csv(DISTANCE_LIST)

distance_list['mfcc_oth_x'] = "NA"
distance_list['mfcc_tgt_x'] = "NA"

def current_position_distance(vector_frame1, vector_frame2):

    cosine_distance = \
            scipy.spatial.distance.cosine(vector_frame1, \
                                             vector_frame2)

    return cosine_distance


def calculate_distances_dtw(mfcc_1, mfcc_2):

    distance_matrix = np.zeros((mfcc_1.shape[0], mfcc_2.shape[0]))
    
    for i in range(mfcc_1.shape[0]):
        for j in range(mfcc_2.shape[0]):
        
            if (i==0) and (j==0):
                smallest_distance = 0
            elif (i==0):
                smallest_distance = distance_matrix[i][j-1] 
            elif (j==0):
                smallest_distance = distance_matrix[i-1][j]             
            else:
                smallest_distance = min(distance_matrix[i-1][j],
                                        distance_matrix[i][j-1],
                                        distance_matrix[i-1][j-1])

            distance_matrix[i][j] = smallest_distance \
                                    + current_position_distance(mfcc_1[i],\
                                                                mfcc_2[j])

    # tracing the shortest path
    # starting from the position of the last row in last column
    # which equals the shortest path distance
    k,l = mfcc_1.shape[0]-1,mfcc_2.shape[0]-1
    path_length = 1

    # looping through the path until the position (0,0) is reached
    while (k != 0) & (l != 0):
        find_shortest_distance = min(distance_matrix[k-1][l],
                                 distance_matrix[k][l-1],
                                 distance_matrix[k-1][l-1])
        shortest_path_position = np.where(distance_matrix == find_shortest_distance)
        path_length += 1
        k = shortest_path_position[0][0]
        l = shortest_path_position[1][0]

    # divide the shortest distance by the length of the path
    average_distance = (distance_matrix[mfcc_1.shape[0]-1][mfcc_2.shape[0]-1]) \
                        / path_length
    return average_distance


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def write_kl_to_column(distance_list, ark_dict):
    """ Write distances into original table """

    for row in distance_list.itertuples():
        row_index = getattr(row, 'Index')
        trip_id = getattr(row, 'tripletid')
    # oth_x_array = np.array([])
    # tgt_x_array = np.array([])

    # for TRIP_NUM in range(1, 113):

    #     # select only item names which correspond to same triplet
    #     trip_id = 'triplet' + str('{0:03}'.format(TRIP_NUM))
        trip_items = [itm for itm in ark_dict.keys() if trip_id in itm]

        # trace the 01 = OTH, 02 = TGT, 03 = X
        item_oth = [oth for oth in trip_items if '_01' in oth][0]
        item_tgt = [tgt for tgt in trip_items if '_02' in tgt][0]
        item_x = [x for x in trip_items if '_03' in x][0]

        # find vectors
        feat_vector_oth = ark_dict[item_oth]
        feat_vector_tgt = ark_dict[item_tgt]
        feat_vector_x = ark_dict[item_x]

        eucl_oth_x = calculate_distances_dtw(feat_vector_oth, feat_vector_x)
        eucl_tgt_x = calculate_distances_dtw(feat_vector_tgt, feat_vector_x)

        distance_list.loc[row_index,'mfcc_oth_x'] = eucl_oth_x
        distance_list.loc[row_index,'mfcc_tgt_x'] = eucl_tgt_x
        # put them into an array
        # oth_x_array = np.append(oth_x_array, eucl_oth_x)
        # tgt_x_array = np.append(tgt_x_array, eucl_tgt_x)



    # distance_list['mfcc_oth_x'] = pd.Series(oth_x_array, \
    #                                     index=distance_list.index)
    # distance_list['mfcc_tgt_x'] = pd.Series(tgt_x_array, \
    #                                     index=distance_list.index)

    return distance_list


ark_dict = {}
for root, dirs, files in ark_folder:
    for ark_file_ in files:
        if ark_file_.endswith(".ark"):
            ark_file = { k:v for k,v in \
                         kaldi_io.read_mat_ark(root + ark_file_) }
            ark_dict = merge_two_dicts(ark_file, ark_dict)
            
    distance_list = write_kl_to_column(distance_list, \
                                                ark_dict)


# write all distances to csv
distance_list.to_csv(ARK_FOLDER + "distances_mfccs.csv", \
                                 index=False)
