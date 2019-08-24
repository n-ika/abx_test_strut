############################
#
#  Scales the intensity of all the files
#  in a specified directory to be equal.
#
############################


sound_directory$ = "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/intervals/"
sound_file_extension$ = ".wav"
end_directory$ = "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/norm_intervals/"
intensity = 70.0


# Here, you make a listing of all the sound files in a directory.

Create Strings as file list... list 'sound_directory$'*'sound_file_extension$'

numberOfFiles = Get number of strings

for ifile to numberOfFiles
    # A sound file is opened from the listing:

    filename$ = Get string... ifile
    Read from file... 'sound_directory$''filename$'

    # Scale intensity

    Scale intensity... intensity

    # Save resulting file

    Write to WAV file... 'end_directory$''filename$'

    select Strings list
endfor

select all
Remove
    
endeditor
exitScript ( )
Close