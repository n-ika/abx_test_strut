from shennong.audio import Audio
from shennong.features.processor.bottleneck import BottleneckProcessor
import pandas as pd
import numpy as np
import scipy.spatial
import os
import sys


WAV_FOLDER = sys.argv[1] # stimuli in .wav
OUT_FOLDER = sys.argv[2] 
DISTANCE_LIST = sys.argv[3] # result will be appended to this

# list with triplet names
distance_list = pd.read_csv(DISTANCE_LIST)

distance_list['bottle_oth_x'] = "NA"
distance_list['bottle_tgt_x'] = "NA"

def current_position_distance(vector_frame1, vector_frame2):

    cosine_distance = \
            scipy.spatial.distance.cosine(vector_frame1, \
                                             vector_frame2)

    return cosine_distance


def calculate_distances_dtw(vector_1, vector_2):

    distance_matrix = np.zeros((vector_1.shape[0], vector_2.shape[0]))
    
    for i in range(vector_1.shape[0]):
        for j in range(vector_2.shape[0]):
        
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
                                    + current_position_distance(vector_1[i],\
                                                                vector_2[j])

    # tracing the shortest path
    # starting from the position of the last row in last column
    # which equals the shortest path distance
    k,l = vector_1.shape[0]-1,vector_2.shape[0]-1
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
    average_distance = (distance_matrix[vector_1.shape[0]-1][vector_2.shape[0]-1]) \
                        / path_length
    return average_distance




all_features = {}

# get bottleneck features of all .wav files (stimuli)
for root, dirs, files in os.walk(WAV_FOLDER):
    for wav_file in files:
        if wav_file.endswith(".wav"):
            audio = Audio.load(root + wav_file)
            processor = BottleneckProcessor(weights='BabelMulti')
            features = processor.process(audio)
            vectors = features.data
            utterance = wav_file.split('.')[0]
            all_features[utterance] = vectors


for row in distance_list.itertuples():
    row_index = getattr(row, 'Index')
    trip_id = getattr(row, 'tripletid')
    bottle_oth = all_features[trip_id + "_OTH"]
    bottle_tgt = all_features[trip_id + "_TGT"]
    bottle_x = all_features[trip_id + "_X"]
               
    eucl_oth_x = \
        calculate_distances_dtw(bottle_oth,\
                                bottle_x)
    eucl_tgt_x = \
        calculate_distances_dtw(bottle_tgt, \
                                bottle_x)

    distance_list.loc[row_index,'bottle_oth_x'] = eucl_oth_x
    distance_list.loc[row_index,'bottle_tgt_x'] = eucl_tgt_x

# write all distances to csv
distance_list.to_csv(OUT_FOLDER + "distances_bottleneck.csv", \
                                 index=False)
