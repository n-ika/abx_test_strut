import os
import sys
import pandas as pd
import numpy as np
import scipy.spatial


MFCCS_FOLDER = sys.argv[1]
OUT_FOLDER = sys.argv[2]
DISTANCE_LIST = sys.argv[3]

distance_list = pd.read_csv(DISTANCE_LIST)

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
                                    + current_position_distance(mfcc_1.loc[i],\
                                                                mfcc_2.loc[j])

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


oth_x_array = np.array([])
tgt_x_array = np.array([])

for TRIP_NUM in range(1, 113):
    # select only item names which correspond to same triplet
    trip_id = 'triplet' + str('{0:03}'.format(TRIP_NUM))
    #path = os.listdir(MFCCS_FOLDER)
    mfcc_oth = pd.read_csv(MFCCS_FOLDER + trip_id + "_OTH_mfcc.csv",\
                            header=None)
    mfcc_tgt = pd.read_csv(MFCCS_FOLDER + trip_id + "_TGT_mfcc.csv",\
                            header=None)
    mfcc_x = pd.read_csv(MFCCS_FOLDER + trip_id + "_X_mfcc.csv",\
                            header=None)

    eucl_oth_x = \
        calculate_distances_dtw(mfcc_oth,\
                                mfcc_x)
    eucl_tgt_x = \
        calculate_distances_dtw(mfcc_tgt, \
                                mfcc_x)

    # put them into an array
    oth_x_array = np.append(oth_x_array, eucl_oth_x)
    tgt_x_array = np.append(tgt_x_array, eucl_tgt_x)



distance_list['mfcc_oth_x'] = pd.Series(oth_x_array, \
                                        index=distance_list.index)
distance_list['mfcc_tgt_x'] = pd.Series(tgt_x_array, \
                                        index=distance_list.index)

    
# write all distances to csv
distance_list.to_csv(OUT_FOLDER + "distances_mfccs_python.csv", \
                                 index=False)
