import kaldi_io
import numpy as np
import pandas as pd
import pqkmeans
import pickle
import sys
import os
import scipy.spatial
from sklearn.metrics.pairwise import pairwise_distances


ARK_FOLDER = sys.argv[1]
FOLDER = sys.argv[2] # where to read from - pickled items in folders

pickles_folder = os.walk(FOLDER)
ark_folder = os.walk(ARK_FOLDER)



def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def write_cos_to_column(ark_dict, \
                    encoder_corpus, \
                    pq_means, \
                    to_folder_):
    if not os.path.exists(to_folder_ + '/softmax_dist'):
        os.mkdir(to_folder_ + '/softmax_dist') 
    to_folder = to_folder_ + '/softmax_dist/'
    # one stimulus/utterance at the time
    # transform it with the encoder (compress)
    for utterance in ark_dict.keys():
        utterance_n = '_'.join(utterance.split('_')[1:])
        vectors = ark_dict[utterance]
        idx = (3,6,9)
        vectors = np.insert(vectors, idx, 0, axis=1)  
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


ark_dict = {}
for root, dirs, files in ark_folder:
    for ark_file_ in files:
        if ark_file_.endswith(".ark"):
            ark_file = { k:v for k,v in \
                         kaldi_io.read_mat_ark(root + ark_file_) }
            ark_dict = merge_two_dicts(ark_file, ark_dict)


for root_p, dirs_p, files_ in pickles_folder:
    for dir_p in dirs_p:
        if dir_p == 'softmax_dist':
            pass
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

        distance_list = write_cos_to_column(ark_dict, \
                                        encoder_corpus, \
                                        clustering_centers_np, \
                                        PATH)