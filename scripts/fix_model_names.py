# Author: Nika Jurov

import pandas as pd
import numpy as np
import sys

EXPERIMENTAL_LIST = sys.argv[1]

FR_MODEL_DIST = sys.argv[2]
FR_MODEL_RESULTS = sys.argv[3]
EN_MODEL_DIST = sys.argv[4]
EN_MODEL_RESULTS = sys.argv[5]

FINAL_DISTANCE_LIST = sys.argv[6]


exp_list = pd.read_csv(EXPERIMENTAL_LIST)
fr_dist = pd.read_csv(FR_MODEL_DIST)
fr_results = pd.read_csv(FR_MODEL_RESULTS)
en_dist = pd.read_csv(EN_MODEL_DIST)
en_results = pd.read_csv(EN_MODEL_RESULTS)
final_dist_list = pd.read_csv(FINAL_DISTANCE_LIST)


stimlist = pd.DataFrame()
distance_list = pd.DataFrame()


exp_list = exp_list.rename(index=str, columns={'File_A':"A", 'File_B':"B",'File_X':"X"})



result_fr = pd.merge(fr_dist, fr_results, how='outer', on=['A', 'B', 'X', 'corr_result'])
result_fr = result_fr.rename(index=str, columns={"model_result":"model_result_fr",
                                                 "AX": "AX_fr", "BX": "BX_fr"})
result_en = pd.merge(en_dist, en_results, how='outer', on=['A', 'B', 'X', 'corr_result'])
result_en = result_en.rename(index=str, columns={"model_result":"model_result_eng",
                                                 "AX": "AX_eng", "BX": "BX_eng"})
result_all = pd.merge(result_en, result_fr, how='outer', on=['A', 'B', 'X', 'corr_result'])
pre_final = pd.merge(exp_list, result_all, how='inner', on=['A', 'B', 'X'])

final = pd.merge(final_dist_list, pre_final, how='inner', on=['tripletid'])




OTH_array_fr = np.array([])
TGT_array_fr = np.array([])
OTH_array_eng = np.array([])
TGT_array_eng = np.array([])


for row in final.itertuples():

    file_A = getattr(row, "A")
    file_B = getattr(row, "B")
    file_OTH = getattr(row, "file_OTH")
    file_TGT = getattr(row, "file_TGT")

    if file_A == file_TGT:
        distance_TGT_eng = getattr(row, "AX_eng")
        distance_TGT_fr = getattr(row, "AX_fr")
        distance_OTH_fr = getattr(row, "BX_fr")
        distance_OTH_eng  = getattr(row, "BX_eng")
    elif file_B == file_TGT:
        distance_TGT_eng = getattr(row, "BX_eng")
        distance_TGT_fr = getattr(row, "BX_fr")
        distance_OTH_fr = getattr(row, "AX_fr")
        distance_OTH_eng  = getattr(row, "AX_eng")

    OTH_array_fr = np.append(OTH_array_fr, distance_OTH_fr)
    TGT_array_fr = np.append(TGT_array_fr, distance_TGT_fr)

    OTH_array_eng = np.append(OTH_array_eng, distance_OTH_eng)
    TGT_array_eng = np.append(TGT_array_eng, distance_TGT_eng)



# write to table

final['distance_OTH_model_fr'] = pd.Series(OTH_array_fr, \
                                  index=final.index)
final['distance_TGT_model_fr'] = pd.Series(TGT_array_fr, \
                                  index=final.index)

final['distance_OTH_model_eng'] = pd.Series(OTH_array_eng, \
                                  index=final.index)
final['distance_TGT_model_eng'] = pd.Series(TGT_array_eng, \
                                  index=final.index)


final.drop(["CORR_ANS", "AX_eng","BX_eng","AX_fr","BX_fr", "A", "B", "X", \
            "Vowel_fr", "Vowel_eng", "Stimulus_A", "Stimulus_B", \
            "Stimulus_X", "corr_result", "Bilingual_spk_eng", 
            "Bilingual_spk_fr", "Context", "Mono_spk", "Order"], axis=1, inplace=True)


final.to_csv("outputs/experimental_list_models_" + \
                    FR_MODEL_DIST.split("/")[-1].split("_")[3] + \
                    ".csv", index=False)
