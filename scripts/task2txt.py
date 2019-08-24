# -*- coding: utf-8 -*-
"""
Created on Tue Jan  23 14:25:01 2018
@author: Thomas Schatz
Script to extract triplets from an ABXpy '.task' file
Output text file format:
    file_A onset_A offset_A file_B onset_B offset_B file_X onset_X, offset_X
Requirements: python 2.7+ or 3.5+, h5py, numpy, pandas
Usage: python task2txt.py task_file out_txt_file
"""

#### WARNING !!!! This script has not been tested !!!! ####

import h5py
import numpy as np
import pandas
from ABXpy.h5tools import h52np


def task2txt(task_file, out_txt_file):
    cols = ['file', 'onset', 'offset']
    dfs = []
    with h5py.File(task_file) as t:
        bys = t['bys'][...]
    for n_by, by in enumerate(bys):
        by_db = pandas.read_hdf(task_file, 'feat_dbs/' + by)
        with h5py.File(task_file) as t:
            trip_attrs = t['triplets']['by_index'][n_by]
        with h52np.H52NP(task_file) as t:
            inp = t.add_subdataset('triplets', 'data', indexes=trip_attrs)
            for triplets in inp:
                df_A = by_db.loc[triplets[:, 0]]
                df_B = by_db.loc[triplets[:, 1]]
                df_X = by_db.loc[triplets[:, 2]]
                df_A = df_A.reset_index(drop=True)
                df_B = df_B.reset_index(drop=True)
                df_X = df_X.reset_index(drop=True)
                df = pandas.DataFrame()
                df[['file_TGT', 'onset_TGT', 'offset_TGT']] = df_A[cols]
                df[['file_OTH', 'onset_OTH', 'offset_OTH']] = df_B[cols]
                df[['file_X', 'onset_X', 'offset_X']] = df_X[cols]
                dfs.append(df)
    df = pandas.concat(dfs)
    df.to_csv(out_txt_file, index=False, float_format='%.6f')


if __name__ == '__main__':
    import argparse
    import os.path as path
    parser = argparse.ArgumentParser()
    parser.add_argument('task_file', help = "ABXpy '.task' file")
    parser.add_argument('out_txt_file', help = "Output text file")
    args = parser.parse_args()
    assert path.isfile(args.task_file), ("No such file "
                                         "{}".format(args.task_file))
    task2txt(args.task_file, args.out_txt_file)

