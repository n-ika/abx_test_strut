import numpy as np
import pandas as pd
from shennong.audio import Audio
from shennong.features.processor.bottleneck import BottleneckProcessor
import scipy.spatial
import pqkmeans
import pickle
import sys
import os


WAV_FOLDER = sys.argv[1] # stimuli in .wav
#FEATS_FILE = sys.argv[2]
LANG = sys.argv[2]

if LANG == "en":
    NUM_PHONES_LIST = [2,5,10,42,100,500,611,1000,6000]
elif LANG == "fr":
    NUM_PHONES_LIST = [2,5,10,61,100,500,1000,1565,6000]



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

all_features = {}
# get bottleneck features of all .wav files (stimuli)
for root, dirs, files in os.walk(WAV_FOLDER):
    for wav_file in files:
        if wav_file.endswith(".wav"):
            audio = Audio.load(root + wav_file)
            all_features[wav_file] = audio

processor = BottleneckProcessor(weights='BabelMulti')
corpus_features = processor.process_all(all_features)


open_feats = []
for key in corpus_features:
    # access every features object
    feats = corpus_features[key].data
    # put them all together
    open_feats.append(feats)

unlisted_feats = np.asarray(open_feats)
#flattened_feats = np.concatenate(all_corpus_features, axis=0)
flattened_feats = np.concatenate(unlisted_feats)
# idx = (3,6,9)
# flattened_feats = np.insert(flattened_feats, idx, 0, axis=1)
print flattened_feats.shape
for NUM_PHONES in list(NUM_PHONES_LIST):
    fold_name = "./" + str(NUM_PHONES) + "_" + LANG
    if not os.path.exists(fold_name):
        os.mkdir(fold_name)
    Kmean_clustering(flattened_feats, int(NUM_PHONES), str(LANG))

