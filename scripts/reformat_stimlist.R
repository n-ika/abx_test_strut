#this takes as input the output of the script "create_stimlist.py"  and the textfile
#meta info from save_intervals_to_wavs.Praat and puts it
#in the format needed for "concatenation_of_wavs.Praat"

library(plyr)
library(dplyr)
library(tidyr)
set.seed(567)

#arguments 
#working directory 
#stimlist to reformat
#meta_info_ from save_intervals to wavs
#output 

setwd("/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/outputs/")

stimlist<-read.csv("./stimlist.csv")
#Using plyr mapvalues, interpret numerals output by create_stimlist 
#as meaningful strings 

vowel_pairs <- c('AE_A', 'AE_E', 'AE_I', 'AE_O', 'AE_OE', 'AE_U', 'AE_Y', 'AH_A',
                 'AH_E', 'AH_I', 'AH_O', 'AH_OE', 'AH_U', 'AH_Y', 'IH_A', 'IH_E',
                 'IH_I', 'IH_O', 'IH_OE', 'IH_U', 'IH_Y', 'UH_A', 'UH_E', 'UH_I',
                 'UH_O', 'UH_OE', 'UH_U', 'UH_Y')

consonantal_context<-c('F_B', 'F_D', 'F_F', 'F_G', 'F_K', 'F_P', 'F_SH', 'F_T', 'F_V',
                       'F_Z', 'SH_B', 'SH_D', 'SH_F', 'SH_G', 'SH_K', 'SH_P', 'SH_S',
                       'SH_SH', 'SH_T', 'SH_V', 'SH_Z', 'S_B', 'S_D', 'S_F', 'S_G', 'S_S',
                       'S_SH', 'S_T', 'S_V', 'S_Z', 'V_B', 'V_D', 'V_F', 'V_G', 'V_K',
                       'V_P', 'V_S', 'V_SH', 'V_T', 'V_V', 'V_Z', 'Z_B', 'Z_D', 'Z_F',
                       'Z_G', 'Z_K', 'Z_P', 'Z_S', 'Z_SH', 'Z_T', 'Z_V', 'Z_Z')

stimlist$VOWEL_PAIRS<-
  mapvalues(stimlist$VOWEL_PAIRS,
            from = c(0:27),
            to=vowel_pairs,
            warn_missing = TRUE)

stimlist$ORDER<-
  mapvalues(stimlist$ORDER,
            from= c(0,1,2,3),
            to = c("PQP","QPP","PQQ","QPQ"),
            warn_missing = TRUE)

stimlist$BILINGUAL_SPEAKER<-
  mapvalues(stimlist$BILINGUAL_SPEAKER,
            from=c(0,1),
            to=c('cecilia','veronique'),
            warn_missing = TRUE)

stimlist$BILINGUAL_SPEAKER_Q<-
  mapvalues(stimlist$BILINGUAL_SPEAKER,
            from=c('cecilia', 'veronique'),
            to=c('veronique', 'cecilia'),
            warn_missing = TRUE)

stimlist$CONTEXT<-
  mapvalues(stimlist$CONTEXT,
            from=c(0:51),
            to=consonantal_context,
            warn_missing = TRUE)


#if X==P, ml_spl = sample(c('ewan', 'jeremy'), size=1)
#if X==Q, ml_spl = sample(c('remi', 'marc'), size=1)
stimlist_XP <- subset(stimlist,stimlist$ORDER == "PQP" | stimlist$ORDER == "QPP")
stimlist_XQ <- subset(stimlist,stimlist$ORDER == "PQQ" | stimlist$ORDER == "QPQ")

stimlist_XP$MONOLINGUAL_SPEAKER<-
   mapvalues(stimlist_XP$MONOLINGUAL_SPEAKER,
              from=c(0,1),
              to=c("ewan","jeremy"),
              warn_missing = TRUE)

 stimlist_XQ$MONOLINGUAL_SPEAKER<-
   mapvalues(stimlist_XQ$MONOLINGUAL_SPEAKER,
              from=c(0,1),
              to=c("remi","marc"),
              warn_missing = TRUE)

stimlist <- rbind(stimlist_XP, stimlist_XQ)

# split the pair column into two columns, name them P and Q
stimlist<-as.data.frame(stimlist)
stimlist<- stimlist %>% separate(VOWEL_PAIRS, c("P", "Q"),sep="_")

stimlist$WORD_PAIRS <- NULL
# rename the bilingual speaker and define it as P
names(stimlist)[names(stimlist) == 'BILINGUAL_SPEAKER'] <- "BILINGUAL_SPEAKER_P"

# Reconstruct the "word" (interval name) from vowel + context


find_word <- function(x){
  words <- c()
  for (i in 1:length(stimlist[, 2:2])) {
    vowel <- stimlist[i, x]
    context <- as.character(stimlist[i, 4])
    splitted_context <- unlist(strsplit(context, split='_', fixed=TRUE))
    words[i] <- paste(splitted_context[1], vowel, splitted_context[2], sep="")
  }
  return(words)
}


stimlist$word_P <- find_word(2)
stimlist$word_Q <- find_word(3)

  
  

######################################################
#create a list of filenames that randomly selects one interval filename of each type
#from the full list_of_all_intervals
######################################################


#first read in list of all intervals from interval saving script
list_of_all_interval_filenames<-
  read.delim("./meta_info_filelist.txt", row.names=NULL)

#now add a variable for speaker by stripping off all characters before "_" in orig_file
#(because orig_file is the FILENAME, which either Ewan or amelia_consonants)
list_of_all_interval_filenames$speaker<-sub("_.*","", list_of_all_interval_filenames$orig_file)

#now group by speaker, then by interval name, then sample one of those intervals.
final_intervals <- group_by(list_of_all_interval_filenames, speaker, int_name)%>% sample_n(1)
final_intervals$key<-paste(final_intervals$speaker,"_",final_intervals$int_name,sep="")
#final_intervals now lists the specific instance of the interval used in col int_filename.



########
#Create a key of which files to use where based on the stimlist created
#by the optimizatiuon script
#####

# create file and silence columns depending on the order column Ps and Qs
stimlist<-stimlist %>% mutate(
  interval_name_1 = case_when(
    ORDER == "PQP"~word_P,
    ORDER == "PQQ"~ word_P,
    ORDER == "QPQ"~ word_Q,
    ORDER == "QPP"~ word_Q),
  interval_name_2 = case_when(
    ORDER == "PQP"~word_Q,
    ORDER == "PQQ"~word_Q,
    ORDER == "QPQ"~word_P,
    ORDER == "QPP"~word_P),
  interval_name_3 = case_when(
    ORDER == "QPQ"~word_Q,
    ORDER == "PQQ"~word_Q,
    ORDER == "PQP"~word_P,
    ORDER == "QPP"~word_P)
)

#add correct answer-- nb do this before adding speaker because speaker will be different across these.  
stimlist<-stimlist %>% mutate(
  CORR_ANS = case_when(
    ORDER %in% c("PQP", "QPQ") ~ "A",
    ORDER %in% c("PQQ", "QPP") ~ "B"))



#############################
#create file keys that will be used to look up the real file name 
##############

stimlist<-stimlist %>% mutate(
  interval_name_1 = case_when(
    BILINGUAL_SPEAKER_P=="cecilia"~paste("cecilia_",interval_name_1,sep=""),
    BILINGUAL_SPEAKER_P=="veronique"~paste("veronique_",interval_name_1,sep="")))

stimlist<-stimlist %>% mutate(
  interval_name_2 = case_when(
    BILINGUAL_SPEAKER_Q=="cecilia"~paste("cecilia_",interval_name_2,sep=""),
    BILINGUAL_SPEAKER_Q=="veronique"~paste("veronique_",interval_name_2,sep="")))

stimlist<-stimlist %>% mutate(
  interval_name_3 = case_when(
    MONOLINGUAL_SPEAKER=="ewan"~paste("ewan_",interval_name_3,sep=""),
    MONOLINGUAL_SPEAKER=="jeremy"~paste("jeremy_",interval_name_3,sep=""),
    MONOLINGUAL_SPEAKER=="remi"~paste("remi_",interval_name_3,sep=""),
    MONOLINGUAL_SPEAKER=="marc"~paste("marc_",interval_name_3,sep="")))

#####

stimlist<-tibble::rowid_to_column(stimlist, "ID")
stimlist$trial_num<-paste("trial_num",stimlist$ID, sep="")





###################
#MAP SITMLIST TO REAL INTERVAL NAMES
#- changing format from wide to long, left join with list of
# real interval names, and then going back to wide.


#transform data to long version with one interval per line
long<-gather(stimlist, key=file_pos, value=key, interval_name_1:interval_name_3)

#use merge to add interval name for each interval 
with_interval_names<-left_join(x=long, y=final_intervals)

#create a unique ID so we can use spread 
with_interval_names<-tibble::rowid_to_column(with_interval_names, "ID")

#select only the columns we care about to make data manipulation work
simple_long<-with_interval_names %>%
  select(file_pos,int_filename, trial_num, CORR_ANS)

#transform data back to wide version with three intervals per line 
wide<-spread(simple_long, key=file_pos, value=int_filename)


#add in columns with the name of the silences. 
wide$Silence1<-rep("500ms_silence",length(wide$interval_name_1))
wide$Silence2<-rep("500ms_silence",length(wide$interval_name_2))

#create Column that has the filename for the concatenated file
wide$filename<-paste("stimulus",1:length(wide$interval_name_1),sep="")

final_stimlist<-wide%>%
  select(interval_name_1,Silence1,interval_name_2,Silence2,interval_name_3,CORR_ANS,filename)

#print df  to text file (NB NOT A CSV, Praat prefers TXT here.)  
write.table(final_stimlist, file="Stimuli_list.txt", sep="\t",quote = FALSE, row.names = FALSE)


# find all the NAs in the table, remove those
# NAS <- with_interval_names[!complete.cases(with_interval_names),]
