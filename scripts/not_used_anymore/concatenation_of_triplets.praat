###############
#Concatenation of files 
#last edit 22 Aug 2018 by amelia 
#
#this script concatenates separate files into one longer file
# -takes as input a comma-delimited text file with at least 7 columns and n rows 
# -each row is a trial in the experiment listing (in order) the soundfiles 
#    to be concatenated for that trial.
# -the script must be in the same folder as all the files to be concatenated. 
# -all columns are strings. the first four are the names of sound files/silence.Then the correct answer, and the name of the triplet
#    File1, silence1, File2, silence3, File3,CORR_ANS,tripletid
# -the fourth column is the name of the correct answer for the trial, which will be 
#    encoded as part of the file name of the new file.
#first, import txt file of stimuli list

Read Table from comma-separated file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/Stimuli_list.txt"
selectObject: "Table Stimuli_list"
ncols_Simuli_list = Get number of columns


#setting the label of the columns as variables so they can be referred to
#in principle unnecessary but fixes several bugs

Set column label (index)... 1 File1
Set column label (index)... 2 Silence1
Set column label (index)... 3 File2
Set column label (index)... 4 Silence2
Set column label (index)... 5 File3
Set column label (index)... 6 CORR_ANS
Set column label (index)... 7 filename

n = Get number of rows

#this for loop selects each file, and names it file_X_i, where X is the column number and 
# i is the current index
#then it selects all of the renamed files and concatenates them
#then it saves the concatenation as a .wav, into the specified folder. 

sound_directory$ = "stimuli_test/intervals/"
silence_directory$="stimuli_test/"

for i to n

    selectObject: "Table Stimuli_list"
    nameone$ = Get value... i File1
    Read from file... 'sound_directory$''nameone$'
        Rename... file1_'i'

    selectObject: "Table Stimuli_list"
    silence1$ = Get value... i Silence1
    Read from file... 'silence_directory$''silence1$'
        Rename... silence1_'i'

    selectObject: "Table Stimuli_list"
    nametwo$ = Get value... i File2
    Read from file... 'sound_directory$''nametwo$'
        Rename... file2_'i'
        
    selectObject: "Table Stimuli_list"
    silence2$ = Get value... i Silence2
    Read from file... 'silence_directory$''silence2$'
        Rename... silence2_'i'

    selectObject: "Table Stimuli_list"
    namethree$ = Get value... i File3
    Read from file... 'sound_directory$''namethree$'
        Rename... file3_'i'


        #concatenate
        select Sound file1_'i'
        plus Sound silence1_'i'
        plus Sound file2_'i'
        plus Sound silence2_'i'
        plus Sound file3_'i'
    
        Concatenate recoverably

        # get correct answer from text file
        selectObject: "Table Stimuli_list"
        answer$ = Get value... i CORR_ANS
        stimulus$ = Get value... i filename
    
        # save the file
        select Sound chain
        Write to WAV file... stimuli_test/concatenated/'stimulus$'_'answer$'.wav
endfor