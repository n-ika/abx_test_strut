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
    times_table = pd.DataFrame(columns=["filename", "spk_num_name",\
                                        "stimulus", "utt_start", "utt_end", \
                                        "stim_start", "stim_end", \
                                        "stim_count", "real_count"])

    file_name = filename.split('.')[0].split('/')[-1]
    language = file_name.split('_')[-2]
    stim_count = 1
    real_count = 1
    if language == "ENG":
        words = ["I", "LIKE", "HERE", "sp"]
    elif language == "FR":
        words = ["JE", "STOCKE", "ICI", "sp"]
    for interval in tier:
        label = interval.mark.strip()
        if label == words[0]:

            start = "{}".format(float(interval.minTime))

        elif label not in words:

            stim = label
            spk_num_name = '_'.join([file_name.split('_')[0].lower(), \
                            language.lower(), str(stim_count)])

            int_start = "{}".format(float(interval.minTime))
            int_end = "{}".format(float(interval.maxTime))


        elif label == words[2]:
            end = "{}".format(float(interval.maxTime))

            if stim == "":
                stim_count -= 1
                spk_num_name = "NA"            
            
            times_info_interval = pd.DataFrame([[file_name, spk_num_name, \
                                        stim, start, end, \
                                        int_start, int_end, \
                                        str(stim_count), str(real_count)]], \
                                        columns=["filename", "spk_num_name",\
                                        "stimulus", "utt_start", "utt_end", \
                                        "stim_start", "stim_end",
                                        "stim_count", "real_count"])

            times_table = times_table.append(times_info_interval, \
                                             ignore_index=True)
            stim_count += 1
            real_count += 1


    return times_table
    

times_info = pd.DataFrame(columns=["filename", "spk_num_name",\
                                    "stimulus", "utt_start", "utt_end", \
                                    "stim_start", "stim_end", \
                                    "stim_count", "real_count"])
for file_tg in glob.glob(TXTGRIDS_FOLDER + "/*.TextGrid"):
    tier = get_interval_names(file_tg, "word")
    local_times = get_times(tier, file_tg)

    times_info = times_info.append(local_times, \
                    ignore_index=True)

times_info.to_csv(TABLE_NAME, index=False)