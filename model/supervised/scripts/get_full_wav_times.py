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
    times_table = pd.DataFrame(columns=["filename", "utt", \
                                   "start", "end", \
                                   "stimulus", "stim_start", \
                                   "stim_end", "stim_count"])

    file_name = filename.split('.')[1].split('/')[-1]
    language = file_name.split('_')[-1]
    stim_count = 1
    if language == "en":
        for interval in tier:
            
            label = interval.mark.strip()
            if label == "I":

                start_time = "{}".format(float(interval.minTime))

            if label != "" and label != "sp" and label != "I" and \
                label != "LIKE" and label != "HERE":

                utt = "I LIKE " + label + " HERE"
                stim = label
                int_start = "{}".format(float(interval.minTime))
                int_end = "{}".format(float(interval.maxTime))

            if label == "HERE":
                end_time = "{}".format(float(interval.maxTime))            
                
                times_info_interval = pd.DataFrame([[file_name, utt, \
                                            start_time, end_time, \
                                            stim, int_start, int_end, \
                                            str(stim_count)]], \
                                            columns=["filename", "utt", \
                                            "start", "end", "stimulus", \
                                            "stim_start", "stim_end",
                                            "stim_count"])

                times_table = times_table.append(times_info_interval, \
                                                 ignore_index=True)
                stim_count += 1


    if language == "fr":
        for interval in tier:
            
            label = interval.mark.strip()
            if label == "JE":

                start_time = "{}".format(float(interval.minTime))

            if label != "" and label != "sp" and label != "JE" and \
                label != "STOCKE" and label != "ICI":

                utt = "JE STOCKE " + label + " ICI"
                stim = label
                int_start = "{}".format(float(interval.minTime))
                int_end = "{}".format(float(interval.maxTime))
            
            if label == "":
                utt = "NA"  

            if label == "ICI":
                end_time = "{}".format(float(interval.maxTime))

            
                
                times_info_interval = pd.DataFrame([[file_name, utt, \
                                            start_time, end_time, \
                                            stim, int_start, int_end, \
                                            str(stim_count)]], \
                                            columns=["filename", "utt", \
                                            "start", "end", "stimulus", \
                                            "stim_start", "stim_end",
                                            "stim_count"])

                times_table = times_table.append(times_info_interval, \
                                                 ignore_index=True)
                stim_count += 1


    return times_table

    

times_info = pd.DataFrame(columns=["filename", "utt", \
                                   "start", "end", \
                                   "stimulus", "stim_start", \
                                   "stim_end", "stim_count"])
for file_tg in glob.glob(TXTGRIDS_FOLDER + "/*.TextGrid"):
    tier = get_interval_names(file_tg, "word")
    local_times = get_times(tier, file_tg)

    times_info = times_info.append(local_times, \
                    ignore_index=True)

times_info.to_csv(TABLE_NAME, index=False)



