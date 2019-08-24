# Author: Nika Jurov

from textgrid import TextGrid
import sys
import os
import pandas as pd
import glob

TXTGRIDS_FOLDER = sys.argv[1]
TABLE_NAME = sys.argv[2]


def get_interval_names(textgrid_fn, tier_name):
    tg = TextGrid()
    tg.read(textgrid_fn)
    tier_i = tg.getNames().index(tier_name)
    return tg[tier_i]



def get_times(tier, filename):
    times_table = pd.DataFrame(columns=["triplet", "word", \
                                        "start", "end", "order"])
    index = 1
    for interval in tier:
        label = interval.mark.strip()
        if label != "" and label != "sp":

            triplet_name = filename.split('.')[1].split('/')[-1]

            start_time = "{}".format(float(interval.minTime))
            end_time = "{}".format(float(interval.maxTime))

            if index == 1:
                order = "A"
            elif index == 2:
                order = "B"
            elif index ==3:
                order = "X"
            
            times_info_interval = pd.DataFrame([[triplet_name, label,\
                                        start_time, end_time, order]],\
                                        columns=["triplet", "word", \
                                        "start", "end", "order"])

            times_table = times_table.append(times_info_interval, \
                                             ignore_index=True)

            index += 1

    return times_table

    

times_info = pd.DataFrame(columns=["triplet", "word", "start",\
                                   "end", "order"])
for file_tg in glob.glob(TXTGRIDS_FOLDER + "/*.TextGrid"):
    tier = get_interval_names(file_tg, "word")
    local_times = get_times(tier, file_tg)

    times_info = times_info.append(local_times, ignore_index=True)

times_info.to_csv(TABLE_NAME, index=False)
