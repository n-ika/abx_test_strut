import scipy.spatial
from sklearn.metrics.pairwise import pairwise_distances
from shennong.audio import Audio
from shennong.features.processor.bottleneck import BottleneckProcessor
import numpy as np
import pandas as pd
import pqkmeans
import pickle
import sys
import os

WAV_FOLDER = sys.argv[1]
FOLDER = sys.argv[2] # where to read from - pickled items in folders

pickles_folder = os.walk(FOLDER)



def write_cos_to_column(stim_features, \
                    encoder_corpus, \
                    pq_means, \
                    to_folder_):
    if not os.path.exists(to_folder_ + '/softmax_dist'):
        os.mkdir(to_folder_ + '/softmax_dist') 
    to_folder = to_folder_ + '/softmax_dist/'
    # one stimulus/utterance at the time
    # transform it with the encoder (compress)
    for utterance in stim_features.keys():
        utterance_n = utterance.split('.')[0]
        vectors = stim_features[utterance].data

        # get the encoding of the stimulus
        stim_pqcodes = encoder_corpus.transform(vectors)
        dist_stim_mean = pairwise_distances(stim_pqcodes, \
                            pq_means, metric='euclidean')
        # transform the distance to each mean w/ softmax
        softmax_stim = scipy.special.softmax(dist_stim_mean, \
                        axis = 1)
        # clustered = kmeans_corpus.fit_predict(stim_pqcode)
        np.save(to_folder + utterance_n, softmax_stim)
        #dist_df = pd.DataFrame(softmax_stim)
        #dist_df.to_csv(to_folder + utterance_n + '.csv')


all_features = {}
# get bottleneck features of all .wav files (stimuli)
for root, dirs, files in os.walk(WAV_FOLDER):
    for wav_file in files:
        if wav_file.endswith(".wav"):
            audio = Audio.load(root + wav_file)
            all_features[wav_file] = audio

processor = BottleneckProcessor(weights='BabelMulti')
stim_features = processor.process_all(all_features)


# dict_feats = {}
# for key in stim_features:
#     # access every features object
#     feats = stim_features[key].data
#     # put them all together
#     dict_feats[key] = feats


for root_p, dirs_p, files_ in pickles_folder:
    for dir_p in dirs_p:
        if dir_p == 'softmax_dist':
            pass
        else:
            PATH = root_p + dir_p
            NUM = dir_p.split('_')[0]
            LANG = dir_p.split('_')[1]
            ENCODER = PATH + "/encoder_" + NUM + '_' + LANG + ".pkl"
            KMEANS = PATH + "/kmeans_" + NUM + '_' + LANG + ".pkl"
            #distance_list = pd.read_csv(DISTANCE_LIST)
            encoder_corpus = pickle.load(open(ENCODER, 'rb'))
            kmeans_corpus = pickle.load(open(KMEANS, 'rb'))
            # Convert to np.array with the proper dtype
            clustering_centers_np = \
                    np.array(kmeans_corpus.cluster_centers_, \
                    dtype=encoder_corpus.code_dtype)

            distance_list = write_cos_to_column(stim_features, \
                                            encoder_corpus, \
                                            clustering_centers_np, \
                                            PATH)