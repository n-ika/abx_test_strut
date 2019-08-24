###########################################
###CLEAN PARTICIPANT OUTPUT GEOMPHON PILOT#
###########################################
#last edit
# 30 Sept by Amelia
#8 August 2018 by Ewan 
#17 July 2018 by Amelia 
# December 2018 by Nika


##################################################
## FIRST ARGUMENT: folder containing raw data files from LMEDS
## This folder MUST contain one subfolder per language group,
## currently we have
##     raw/English_turkers
##     raw/French_turkers
## each of which contain the data files for those two language
## groups; this script puts this subfolder name in a column
## called "subject_language" in the output
##
## The individual data file names (e.g. .../.../NAME.csv)
## will be stripped of pathnames and ".csv" and used to generate subject
## ids (see below); we assume that the NAME is the Turker ID
## therefore this must be run on ANONYMIZED DATA
##
## SECOND ARGUMENT: main results file
## THIRD ARGUMENT: presurvey file
## FOURTH ARGUMENT: first postsurvey file
## FIFTH ARGUMENT: second postsurvey file
##

##change cleaning methods at end to ensure that they are useful for your data

import sys
import os
import fnmatch
import random
import pandas as pd
import numpy as np

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ARGUMENTS
folderpath =sys.argv[1]
results_filename = sys.argv[2]
presurvey_filename =  sys.argv[3]
postsurvey_filename = sys.argv[4]
postsurvey2_filename = sys.argv[5]



###
#Start with only files from the Aug pilot (other files will not match
#in columns because of different survey questions)

######



#make a list of the filenames in the folder 
file_language_tuples = []
for current_root, dirnames_d, filenames_d in os.walk(folderpath):
    csv_filenames = fnmatch.filter(filenames_d, "*.csv")
    if current_root == folderpath:
        if len(csv_filenames) > 0:
            print >> sys.stderr(""), \
                    "ERROR: need at least one level of nesting " \
                    + "in data folder '" + folderpath + "'"
            sys.exit()
        continue
    full_pathnames = [os.path.join(current_root, f) \
            for f in csv_filenames]
    subfolder = folderpath.join(current_root.split(folderpath)[1:])
    first_subfolder = None
    for folder in subfolder.split('/'):
        if len(folder) > 0:
            first_subfolder = folder
            break
    curr_tuples = [(f, first_subfolder) for f in full_pathnames]
    file_language_tuples += curr_tuples




###START LOOP iterating through these files
results = None
presurvey = None
postsurvey = None
postsurvey2 = None
for f, language in file_language_tuples:
    # LMEDS 'csv' files actually don't have the same number of columns on each
    # line: find out the greatest number of columns
    with open(f) as hf:
        max_n_columns = 0
        for line in hf.readlines():
            split_line = line.strip().split(',')
            if len(split_line) > max_n_columns:
                max_n_columns = len(split_line)

    # Generate arbitrary column names (legacy - can let pandas do this in
    # future)
    my_cols = []
    reps = 1
    for i in range(max_n_columns):
        i_alphabet = i % 26
        letter = ALPHABET[i_alphabet]
        my_cols.append(letter*reps)
        if i_alphabet == 25:
            reps += 1

    #read in  one of the files in the folder of subject output into a dataframe
    thissubj = pd.read_csv(f, names=my_cols, engine='python', encoding='utf-8')
    #cast column B to string because we need and sometimes it's being read wrong
    thissubj.B = thissubj.B.astype(str)
    # filenames are SUBJECT_NAME.csv
    subject_name = os.path.splitext(os.path.basename(f))[0]

    #add columns for subject id and subject language
    thissubj['subject_id'] = subject_name
    thissubj['subject_language'] = language
    #find all the lines in the output dataframe that start with the string
    # "media_choice", and make them an obj called :"resultslines"
    #concatenate those new lines and the results DataFrame, replace the old
    # results df with this new combined one.
    resultslines = pd.DataFrame(thissubj.loc[thissubj["A"] == 'media_choice'])
    if results is None:
        results = resultslines
    else:
        results = pd.concat([results,resultslines])
    #now find the row that starts with the words valsurvey, presurvey 
    #concatenate thoese line to the presurvey dataframe
    presurlines = pd.DataFrame(thissubj.loc[(thissubj["B"] == '[presurvey') | \
                                            (thissubj["B"] == '[presurvey_fr')])
    
    if not presurlines[presurlines["subject_language"] == 'eng'].empty:
        presurlines["RR"] = np.nan
    
    if presurvey is None:
        presurvey = presurlines
    else:
        presurvey = pd.concat([presurvey,presurlines])

    #now find the row that starts with post survey
    #concatenate thoese line to the dataframe
    postsurlines = pd.DataFrame(thissubj.loc[(thissubj["B"] == '[postsurvey') | \
                                              (thissubj["B"] == '[postsurvey_fr')])
    if postsurvey is None:
        postsurvey = postsurlines
    else:
        postsurvey = pd.concat([postsurvey,postsurlines])

    #now find the row that starts with post survey 2
    postsur2lines = pd.DataFrame(thissubj.loc[(thissubj["B"] == '[postsurvey2') | \
                                               (thissubj["B"] == '[postsurvey_fr2')])
    if postsurvey2 is None:
        postsurvey2 = postsur2lines
    else:
        postsurvey2 = pd.concat([postsurvey2,postsur2lines])
    ### END OF LOOP




##############################
## CLEAN UP RESULTS DATAFRAME#
##############################

RESULTS_COLUMN_ORDER = ["subject_id", "subject_language", "B",
        "G", "O", "P", "S", "T", "U", "V"]
RESULTS_COLUMN_DICT = {
    "subject_id": "subject_id",
    "subject_language": "subject_language",
    "B": "trial_type",
    "G": "tripletid",
    "O": "S-order",
    "P": "A_Order",
    "S": "RT",
    "T": "order",
    "U": "first_sound",
    "V": "second_sound"
}

# drop columns that are not needed 
results = results[RESULTS_COLUMN_ORDER]

#give columns clearer titles
results= results.rename(columns=RESULTS_COLUMN_DICT)

# remove extra characters
results.tripletid = results.tripletid.str.replace('[','')
results.tripletid = results.tripletid.str.replace(']','')
results.trial_type = results.trial_type.str.replace('[','')
results.A_Order = results.A_Order.str.replace(']','')

# write out to .csv  
results.to_csv(results_filename, index=False, encoding='utf-8')

#################################
#CLEAN UP PRESURVEY DATAFRAME#
#################################

PRESURVEY_COLUMN_ORDER_ENG = ["subject_id", "subject_language", "I",
    "J", "K", "L", "M", "N", "O", "P", "OO","PP", "Q", "R", "S", "QQ", 
    "T", "U", "V","W", "X", "Y", "RR","Z", "AA", "BB", "CC", "DD", 
    "EE","FF","GG","HH","II","JJ","KK","LL","MM","NN",
    ]
PRESURVEY_COLUMN_DICT_ENG = {
    "subject_id": "subject_id",
    "subject_language": "subject_language",
    "I": "18-29yrs",
    "J":"30-39yrs",
    "K":"40-49yrs",
    "L":"50-59yrs",
    "M":"60-69yrs",
    "N":"more_than_69yrs",
    "O":"handedness_L",
    "P":"handedness_R",
    "OO":"french_native",
    "PP":"french_non_native",
    "Q":"lang_other_target_no",
    "R":"lang_other_target_yes",
    "S":"other_lang_na",
    "QQ":"other_lang_na2",
    "T":"other_lang_native",
    "U":"other_lang_bcpdexp",
    "V":"other_lang_assezdexp",
    "W":"other_lang_unpeudexp",
    "X":"other_lang_trespeudexp",
    "Y":"other_lang_comp_na",
    "RR":"other_lang_comp_na2",
    "Z":"other_lang_comp_native",
    "AA":"other_lang_presque_native",
    "BB":"other_lang_avancee",
    "CC":"other_lang_intermediare",
    "DD":"other_lang_debutant",
    "EE":"hear_vis_problems_yes",
    "FF":"hear_vis_problems_no",
    "GG":"troubles_de_lang_yes",
    "HH":"troubles_de_lang_no",
    "II":"ling_course_yes",
    "JJ":"ling_course_no",
    "KK":"phonet_course_yes",
    "LL":"phonet_course_no",
    "MM":"phonog_course_yes",
    "NN":"phonog_course_no"
}


PRESURVEY_COLUMN_ORDER_FR = ["subject_id", "subject_language", "I",
    "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
    "W", "X", "RR", "Y", "Z", "AA", "BB", "CC", "DD", "EE","FF","GG","HH",
    "II","JJ","KK","LL","MM","NN","OO", "PP", "QQ"]
PRESURVEY_COLUMN_DICT_FR = {
    "subject_id": "subject_id",
    "subject_language": "subject_language",
    "I": "18-29yrs",
    "J":"30-39yrs",
    "K":"40-49yrs",
    "L":"50-59yrs",
    "M":"60-69yrs",
    "N":"more_than_69yrs",
    "O":"handedness_L",
    "P":"handedness_R",
    "Q":"french_native",
    "R":"french_non_native",
    "S":"lang_other_target_no",
    "T":"lang_other_target_yes",
    "U":"other_lang_na",
    "V":"other_lang_na2",
    "W":"other_lang_native",
    "X":"other_lang_bcpdexp",
    "RR":"other_lang_assezdexp",
    "Y":"other_lang_unpeudexp",
    "Z":"other_lang_trespeudexp",
    "AA":"other_lang_comp_na",
    "BB":"other_lang_comp_na2",
    "CC":"other_lang_comp_native",
    "DD":"other_lang_presque_native",
    "EE":"other_lang_avancee",
    "FF":"other_lang_intermediare",
    "GG":"other_lang_debutant",
    "HH":"hear_vis_problems_yes",
    "II":"hear_vis_problems_no",
    "JJ":"troubles_de_lang_yes",
    "KK":"troubles_de_lang_no",
    "LL":"ling_course_yes",
    "MM":"ling_course_no",
    "NN":"phonet_course_yes",
    "OO":"phonet_course_no",
    "PP":"phonog_course_yes",
    "QQ":"phonog_course_no"
}



PRESURVEY_COLUMN_ORDER_FR_2 = ["subject_id", "subject_language", "I",
    "J", "K", "L", "M", "N", "O", "P", "OO", "PP", "Q", "R", "S", "QQ", "T", "U","V",
    "W", "X", "Y", "RR", "Z", "AA", "BB", "CC", "DD", "EE","FF","GG","HH",
    "II","JJ","KK","LL","MM","NN"]
PRESURVEY_COLUMN_DICT_FR_2 = {
    "subject_id": "subject_id",
    "subject_language": "subject_language",
    "I": "18-29yrs",
    "J":"30-39yrs",
    "K":"40-49yrs",
    "L":"50-59yrs",
    "M":"60-69yrs",
    "N":"more_than_69yrs",
    "O":"handedness_L",
    "P":"handedness_R",
    "OO":"french_native",
    "PP":"french_non_native",
    "Q":"lang_other_target_no",
    "R":"lang_other_target_yes",
    "S":"other_lang_na",
    "QQ":"other_lang_na2",
    "T":"other_lang_native",
    "U":"other_lang_bcpdexp",
    "V":"other_lang_assezdexp",
    "W":"other_lang_unpeudexp",
    "X":"other_lang_trespeudexp",
    "Y":"other_lang_comp_na",
    "RR":"other_lang_comp_na2",
    "Z":"other_lang_comp_native",
    "AA":"other_lang_presque_native",
    "BB":"other_lang_avancee",
    "CC":"other_lang_intermediare",
    "DD":"other_lang_debutant",
    "EE":"hear_vis_problems_yes",
    "FF":"hear_vis_problems_no",
    "GG":"troubles_de_lang_yes",
    "HH":"troubles_de_lang_no",
    "II":"ling_course_yes",
    "JJ":"ling_course_no",
    "KK":"phonet_course_yes",
    "LL":"phonet_course_no",
    "MM":"phonog_course_yes",
    "NN":"phonog_course_no"
}

presurvey_eng = presurvey[presurvey["subject_language"] == "eng"]
presurvey_fr = presurvey[presurvey["subject_language"] == "fr"]
presurvey_fr_2 = presurvey[presurvey["subject_language"] == "fr2"]

#drop unneeded columns
presurvey_eng = presurvey_eng[PRESURVEY_COLUMN_ORDER_ENG]
#give columns clearer titles
presurvey_eng = presurvey_eng.rename(columns=PRESURVEY_COLUMN_DICT_ENG)

presurvey_fr = presurvey_fr[PRESURVEY_COLUMN_ORDER_FR]
presurvey_fr = presurvey_fr.rename(columns=PRESURVEY_COLUMN_DICT_FR)

presurvey_fr_2 = presurvey_fr_2[PRESURVEY_COLUMN_ORDER_FR_2]
presurvey_fr_2 = presurvey_fr_2.rename(columns=PRESURVEY_COLUMN_DICT_FR_2)



presurvey_joined = pd.concat([presurvey_eng, presurvey_fr, presurvey_fr_2])

# write out to .csv  
presurvey_joined.to_csv(presurvey_filename, index=False, encoding='utf-8')


################################
#CLEAN UP POSTSURVEY1 DATAFRAME#
################################
POSTSURVEY_COLUMN_ORDER = ["subject_id", "subject_language",
    "G", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
    "T", "U", "V", "W", "X", "Y", "Z", "AA", "BB", "CC", "DD",
    "EE", "FF", "GG"]
POSTSURVEY_COLUMN_DICT = {
    "subject_id": "subject_id",
    "subject_language": "subject_language",
    "G":"survey_time",
    "I":"chrome",
    "J":"firefox",
    "K":"IE",
    "L":"safari",
    "M":"opera",
    "N":"other",
    "O":"don't know",
    "P":"headphones",
    "Q":"speakers",
    "R":"earbuds",
    "S":"very bad",
    "T":"bad",
    "U":"normal",
    "V":"good",
    "W":"very good",
    "X":"distractions_yes",
    "Y":"distractions_no",
    "Z":"wireless",
    "AA":"wired",
    "BB":"very_slowly",
    "CC":"slowly",
    "DD":"tolerably_so",
    "EE":"pretty_fast",
    "FF":"no_loading_time",
    "GG":"satisfaction"
}

POSTSURVEY_COLUMN_ORDER_FR = ["subject_id", "subject_language",
    "G", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "BB", "CC",
    "DD", "EE", "FF", "GG", "R", "S",
    "T", "U", "V", "W", "X", "Y", "Z", "AA"]
POSTSURVEY_COLUMN_DICT_FR = {
    "subject_id": "subject_id",
    "subject_language": "subject_language",
    "G":"survey_time",
    "I":"chrome",
    "J":"firefox",
    "K":"IE",
    "L":"safari",
    "M":"opera",
    "N":"other",
    "O":"don't know",
    "P":"headphones",
    "Q":"speakers",
    "BB":"earbuds",
    "CC":"very bad",
    "DD":"bad",
    "EE":"normal",
    "FF":"good",
    "GG":"very good",    
    "R":"distractions_yes",
    "S":"distractions_no",
    "T":"wireless",
    "U":"wired",
    "V":"very_slowly",
    "W":"slowly",
    "X":"tolerably_so",
    "Y":"pretty_fast",
    "Z":"no_loading_time",
    "AA":"satisfaction"
}



postsurvey_eng = postsurvey[postsurvey["subject_language"] == "eng"]

postsurvey_eng = postsurvey_eng[POSTSURVEY_COLUMN_ORDER]
postsurvey_eng = postsurvey_eng.rename(columns=POSTSURVEY_COLUMN_DICT)

postsurvey_fr = postsurvey[postsurvey["subject_language"] == "fr"]

postsurvey_fr = postsurvey_fr[POSTSURVEY_COLUMN_ORDER_FR]
postsurvey_fr = postsurvey_fr.rename(columns=POSTSURVEY_COLUMN_DICT_FR)

postsurvey_fr2 = postsurvey[postsurvey["subject_language"] == "fr2"]

postsurvey_fr2 = postsurvey_fr2[POSTSURVEY_COLUMN_ORDER_FR]
postsurvey_fr2 = postsurvey_fr2.rename(columns=POSTSURVEY_COLUMN_DICT_FR)


postsurvey_joined = pd.concat([postsurvey_eng, postsurvey_fr, postsurvey_fr2])

postsurvey_joined.to_csv(postsurvey_filename, index=False, encoding='utf-8')

###############################
#CLEAN UP POSTSURVEY2 DATAFRAME#
###############################

POSTSURVEY2_COLUMN_ORDER = ['subject_id', 'subject_language',
        "G", "I", "J"]
POSTSURVEY2_COLUMN_DICT = {
    "subject_id": "subject_id",
    "subject_language": "subject_language",
    "G": "survey_time",
    "I": "comments",
    "J": "experiment_topic"
}

postsurvey2 = postsurvey2[POSTSURVEY2_COLUMN_ORDER]
postsurvey2 = postsurvey2.rename(columns=POSTSURVEY2_COLUMN_DICT)
postsurvey2.to_csv(postsurvey2_filename, index=False, encoding='utf-8')

