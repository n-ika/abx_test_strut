# Author: Nika Jurov

# in the table distance_list for every 3 intervals
# find in folder of mfccs the corresponding mfccs (same name + ".csv")
# define the three intervals as variables
# calculate distance between A & X and B & X
# calculates distances of normalilzed values
# append distances to the exp file and write to csv a copy of it



import pandas as pd
import numpy as np
import sys
import math
import scipy.spatial

DISTANCE_LIST = sys.argv[1]
MFCCS_FOLDER = sys.argv[2]


# list with all information (triplets, interval names, filenames)
distance_list = pd.read_csv(DISTANCE_LIST)



def current_position_distance(vector_frame1, vector_frame2):

#squared_difference = 0
    #for k in range(len(vector_frame1)):
    #    squared_difference += pow(vector_frame1[k] - vector_frame2[k], 2)
    #euclidean_distance = math.sqrt(squared_difference)

    euclidean_distance = \
            scipy.spatial.distance.euclidean(vector_frame1, vector_frame2)

    return euclidean_distance


def calculate_distances_dtw(mfcc_1, mfcc_2):

    distance_matrix = np.zeros((mfcc_1.shape[1], mfcc_2.shape[1]))
    
    for i in range(mfcc_1.shape[1]):
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
                                    + current_position_distance(mfcc_1[i], mfcc_2[j])

    # tracing the shortest path
    # starting from the position of the last row in last column
    # which equals the shortest path distance
    k,l = mfcc_1.shape[1]-1,mfcc_2.shape[1]-1
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
    average_distance = (distance_matrix[mfcc_1.shape[1]-1][mfcc_2.shape[1]-1]) \
                        / path_length
    return average_distance


def load_mfcc(file_from_exp_list):

    mfcc_file = np.loadtxt(MFCCS_FOLDER + file_from_exp_list, delimiter=',')
    mfcc_df = pd.DataFrame(mfcc_file)
    return mfcc_df



# to be filled with AX and BX distances corresponding to each row
distances_OTH_array = np.array([])
distances_TGT_array = np.array([])

for row in distance_list.itertuples():
    # find intervals used in triplets
    file_OTH = getattr(row, 'file_OTH') + ".csv"
    file_TGT = getattr(row, 'file_TGT') + ".csv"
    file_X = getattr(row, 'file_X') + ".csv"

    # load mfcc files
    file_OTH_mfcc = load_mfcc(file_OTH)
    file_TGT_mfcc = load_mfcc(file_TGT)
    file_X_mfcc = load_mfcc(file_X)

    # calculate distances
    distance_OTH = calculate_distances_dtw(file_OTH_mfcc, file_X_mfcc)
    distance_TGT = calculate_distances_dtw(file_TGT_mfcc, file_X_mfcc)

    # append the distance to np.array
    distances_OTH_array = np.append(distances_OTH_array, distance_OTH)
    distances_TGT_array = np.append(distances_TGT_array, distance_TGT)


# write to table
distance_list['distance_OTH'] = pd.Series(distances_OTH_array, \
                                    index=distance_list.index)
distance_list['distance_TGT'] = pd.Series(distances_TGT_array, \
                                    index=distance_list.index)


distance_list.to_csv("outputs/distances_table_final.csv", index=False)

