# Anonymize the names of data files from LMEDS: by default, the filenames
# are the subject ID entered by the subject. This is generally identifiable,
# including on Mechanical Turk. Here we simply create our own, private
# database of randomized subject ID's corresponding to the ID's entered by
# the subjects. (see http://wtf.tw/ref/lease.pdf)
#
# This is stored in a CSV that we never release to anyone that contains two
# columns, one for real subject ID, called "RealID", and one for our
# anonymized ID, called "AnonID".
#
# FIRST ARGUMENT: the folder containing the raw LMEDS data, ending in ".csv"
#
# SECOND ARGUMENT: the folder to output to; the internal structure of the
# input folder will be preserved; this folder will be created if it doesn't
# already exist, but it will *not* be cleaned out if it already exists,
# so be careful
#
# THIRD ARGUMENT: The anonymization CSV
#
# Author: Ewan Dunbar

import sys
import os
import fnmatch
import shutil
import pandas as pd
import random

ALPHABET = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def anonymize_subject_id(real_subject_id, table):
    if sum(table['RealID'] == real_subject_id) > 0:
        matches = table[table['RealID'] == real_subject_id]
        anon_id = matches['AnonID'].tolist()[0]
        updated_table = table
    else:
        anon_id = "X_" + ''.join(random.sample(ALPHABET, 10))
        new_row = pd.DataFrame()
        updated_table = table.append({'RealID': real_subject_id,
                                     'AnonID': anon_id}, ignore_index=True)
    return anon_id, updated_table

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    anon_file = sys.argv[3]

    # read anonymization file
    if os.path.isfile(anon_file):
        anon_table = pd.read_csv(anon_file)
    else:
        anon_table = pd.DataFrame(columns=['RealID','AnonID'])

    # Re-create folder structure of input directory and rename
    # files
    for current_root, dir_names, filenames_d in os.walk(input_folder):
        trailing_path = input_folder.join(current_root.split(input_folder)[1:])
        new_path = os.sep.join([output_folder, trailing_path])
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        csv_filenames = fnmatch.filter(filenames_d, "*.csv")
        for f in csv_filenames:
            subject_id = os.path.splitext(f)[0]
            new_id, anon_table = anonymize_subject_id(subject_id, anon_table)
            new_basename = new_id + ".csv"
            full_path_old = os.sep.join([current_root, f])
            full_path_new = os.sep.join([new_path, new_basename])
            shutil.copy2(full_path_old, full_path_new)

    # Write out updated anonymization file
    anon_table.to_csv(anon_file, index=False)