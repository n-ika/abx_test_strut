import kaldi_io
import numpy as np
import pandas as pd
import pqkmeans
import pickle
import sys
import os


TRAINING_CORPUS_FEATS = sys.argv[1]
LANG = sys.argv[2]

if LANG == "en":
    NUM_PHONES_LIST = [2,5,10,42,100,500,611,1000,6000]
elif LANG == "fr":
    NUM_PHONES_LIST = [2,5,10,61,100,500,1000,1565,6000]


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def Kmean_clustering(corpus_feats, num_phones, lang):
    # Train a PQ encoder.
    # Each vector is divided into 4 parts and each part is
    # encoded with log256 = 8 bit, resulting in a 32 bit PQ code.
    encoder = pqkmeans.encoder.PQEncoder(num_subdim=4, Ks=256)

    encoder.fit(corpus_feats[:1000000]) 

    # Convert input vectors to 32-bit PQ codes, where each PQ code consists of four uint8.
    # You can train the encoder and transform the input vectors to PQ codes preliminary.
    X_pqcode = encoder.transform(corpus_feats)

    # Run clustering 
    kmeans = pqkmeans.clustering.PQKMeans(encoder=encoder, \
                                            k=int(num_phones))
    clustered = kmeans.fit_predict(X_pqcode)

    pickle.dump(encoder, open(str(num_phones) + '_' + lang + \
                    '/encoder_' + str(num_phones) + \
                    '_' + lang + '.pkl', 'wb'))
    pickle.dump(kmeans, open(str(num_phones) + '_' + lang + \
                    '/kmeans_' + str(num_phones) + \
                    '_' + lang + '.pkl', 'wb'))


ark_dict = {}
for root, dirs, files in os.walk(TRAINING_CORPUS_FEATS):
    for ark_file_ in files:
        if ark_file_ == "cmvn_features.ark":
            pass
        elif ark_file_.endswith(".ark"):
            # read from ark file
            ark_file = { k:v for k,v in \
                         kaldi_io.read_mat_ark(root + ark_file_) }
            # bind together different ark files into 1 dict
            ark_dict = merge_two_dicts(ark_file, ark_dict)
    # move all vectors from separate arrays into a single array 
    # irrespective of their utterance number / speaker
    flattened_feats = np.concatenate(ark_dict.values(), axis=0)
    idx = (3,6,9)
    flattened_feats = np.insert(flattened_feats, idx, 0, axis=1)
    print flattened_feats.shape
    for NUM_PHONES in list(NUM_PHONES_LIST):
        fold_name = "./" + str(NUM_PHONES) + "_" + LANG
        if not os.path.exists(fold_name):
            os.mkdir(fold_name)
        Kmean_clustering(flattened_feats, int(NUM_PHONES), str(LANG))

