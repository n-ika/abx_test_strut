# This script saves each interval in the selected IntervalTier of a TextGrid to a separate WAV sound file.
# The source sound must be a LongSound object, and both the TextGrid and 
# the LongSound must have identical names and they have to be selected 
# before running the script.
# Files are named with the corresponding interval labels (plus a running index number when necessary).
#
# NOTE: You have to take care yourself that the interval labels do not contain forbidden characters!!!!
# 
# This script is distributed under the GNU General Public License.
# Copyright 8.3.2002 Mietta Lennes

#adapted 20 Aug 2018 by Amelia 
#-removed form and instead saved presets. 
#-removed the warning of how many files will be saved
#-all instances of the same interval name end with a trailing index number, starting from 1. If you run the 
#script multiple times it will continue counting up. 

# adapted by Nika for ABX test - STRUT vowel

#define settings 

	#comment Which IntervalTier in this TextGrid would you like to process?
	tier = 2

	#comment Starting and ending at which interval? 
	start_from = 1
	#0 = end at last contour 
	end_at = 0
	
	#choose whether to exclude empty tiers or XXX (specify as 1/0 boolean)
	exclude_empty_labels = 1
	exclude_intervals_labeled_as_xxx = 1

	#comment Give a small margin in seconds if you like:
	margin = 0.001

	#give the folder where to save the sound files:
	folder$ = "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/intervals/"

	#comment Give an optional suffix for all filenames (.wav will be added anyway):
	suffix$ = ""

	#give the name of the output file:
	output$ = "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/outputs/meta_info_filelist.txt"
	#add header line to output file 
	appendFileLine: "'output$'","orig_file",tab$,"indexnumber", tab$ ,"int_name", tab$, "int_filename"


#open .wavs as Long Sounds and TextGrids as textgrids
Open long sound file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Veronique_ABX_ENG_clean.wav"
Open long sound file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Veronique_ABX_FR_clean.wav"
Open long sound file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Cecilia_ABX_ENG_clean.wav"
Open long sound file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Cecilia_ABX_FR_clean.wav"
Open long sound file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Ewan_ABX_ENG_clean.wav"
Open long sound file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Marc_ABX_FR_clean.wav"
Open long sound file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Jeremy_ABX_ENG_clean.wav"
Open long sound file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Remi_ABX_FR_clean.wav"

Read from file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Veronique_ABX_ENG_clean.TextGrid"
Read from file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Veronique_ABX_FR_clean.TextGrid"
Read from file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Cecilia_ABX_ENG_clean.TextGrid"
Read from file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Cecilia_ABX_FR_clean.TextGrid"
Read from file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Ewan_ABX_ENG_clean.TextGrid"
Read from file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Marc_ABX_FR_clean.TextGrid"
Read from file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Jeremy_ABX_ENG_clean.TextGrid"
Read from file: "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli/Remi_ABX_FR_clean.TextGrid"


##########
####This script is currently done three separate times instead of looping. 
####If you change to aloop, make sure to also change the output file names to retain speaker info. 

#Iteration 1: select the first LongSound and TextGrid Pair
selectObject: "LongSound Veronique_ABX_ENG_clean"
plusObject: "TextGrid Veronique_ABX_ENG_clean"

	gridname$ = selected$ ("TextGrid", 1)
	soundname$ = selected$ ("LongSound", 1)
	select TextGrid 'gridname$'
	numberOfIntervals = Get number of intervals... tier
	if start_from > numberOfIntervals
		exit There are not that many intervals in the IntervalTier!
	endif
	if end_at > numberOfIntervals
		end_at = numberOfIntervals
	endif
	if end_at = 0
		end_at = numberOfIntervals
	endif

	# Default values for variables
	files = 0
	intervalstart = 0
	intervalend = 0
	interval = 1
	intname$ = ""
	intervalfile$ = ""
	endoffile = Get finishing time
	#comment Give an optional prefix for all filenames, here used to define speaker:
	prefix$ = "veronique_eng_" 

	# Loop through all intervals in the selected tier of the TextGrid
	indexnumber = 1

	for interval from start_from to end_at
		select TextGrid 'gridname$'
		intname$ = ""
		intname$ = Get label of interval... tier interval
		check = 0
		if intname$ = "sp" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "I" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "LIKE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "HERE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "" and exclude_empty_labels = 1
			check = 1
		endif
		if check = 0
			intervalstart = Get starting point... tier interval
				if intervalstart > margin
					intervalstart = intervalstart - margin
				else
					intervalstart = 0
				endif
	
			intervalend = Get end point... tier interval
				if intervalend < endoffile - margin
					intervalend = intervalend + margin
				else
					intervalend = endoffile
				endif
	
			select LongSound 'soundname$'
			Extract part... intervalstart intervalend no
			filename$ = intname$
			
			intervalfile$ = "'folder$'" + "'prefix$'" + "'filename$'" + "'suffix$''indexnumber'" + ".wav"
			
			Write to WAV file... 'intervalfile$'
			Remove

			#append info to output text file, with info on longsound file, interval number, interval name, and soundfile name
			appendFileLine: "'output$'", "'prefix$'" ,tab$, "'indexnumber'" , tab$ ,"'intname$'", tab$ ,"'prefix$''indexnumber'"


			indexnumber = indexnumber + 1
		endif
	endfor


#Iteration 2: select the first LongSound and TextGrid Pair
selectObject: "LongSound Ewan_ABX_ENG_clean"
plusObject: "TextGrid Ewan_ABX_ENG_clean"

	gridname$ = selected$ ("TextGrid", 1)
	soundname$ = selected$ ("LongSound", 1)
	select TextGrid 'gridname$'
	numberOfIntervals = Get number of intervals... tier
	if start_from > numberOfIntervals
		exit There are not that many intervals in the IntervalTier!
	endif
	if end_at > numberOfIntervals
		end_at = numberOfIntervals
	endif
	if end_at = 0
		end_at = numberOfIntervals
	endif

	# Default values for variables
	files = 0
	intervalstart = 0
	intervalend = 0
	interval = 1
	intname$ = ""
	intervalfile$ = ""
	endoffile = Get finishing time
	#comment Give an optional prefix for all filenames, here used to define speaker:
	prefix$ = "ewan_eng_" 

	# Loop through all intervals in the selected tier of the TextGrid
	indexnumber = 1

	for interval from start_from to end_at
		select TextGrid 'gridname$'
		intname$ = ""
		intname$ = Get label of interval... tier interval
		check = 0
		if intname$ = "sp" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "I" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "LIKE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "HERE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "" and exclude_empty_labels = 1
			check = 1
		endif
		if check = 0
			intervalstart = Get starting point... tier interval
				if intervalstart > margin
					intervalstart = intervalstart - margin
				else
					intervalstart = 0
				endif
	
			intervalend = Get end point... tier interval
				if intervalend < endoffile - margin
					intervalend = intervalend + margin
				else
					intervalend = endoffile
				endif
	
			select LongSound 'soundname$'
			Extract part... intervalstart intervalend no
			filename$ = intname$
			
			intervalfile$ = "'folder$'" + "'prefix$'" + "'filename$'" + "'suffix$''indexnumber'" + ".wav"
			
			Write to WAV file... 'intervalfile$'
			Remove

			#append info to output text file, with info on longsound file, interval number, interval name, and soundfile name
			appendFileLine: "'output$'", "'prefix$'" ,tab$, "'indexnumber'" , tab$ ,"'intname$'", tab$ ,"'prefix$''indexnumber'"


			indexnumber = indexnumber + 1
		endif
	endfor


#Iteration 3: select the first LongSound and TextGrid Pair
selectObject: "LongSound Jeremy_ABX_ENG_clean"
plusObject: "TextGrid Jeremy_ABX_ENG_clean"

	gridname$ = selected$ ("TextGrid", 1)
	soundname$ = selected$ ("LongSound", 1)
	select TextGrid 'gridname$'
	numberOfIntervals = Get number of intervals... tier
	if start_from > numberOfIntervals
		exit There are not that many intervals in the IntervalTier!
	endif
	if end_at > numberOfIntervals
		end_at = numberOfIntervals
	endif
	if end_at = 0
		end_at = numberOfIntervals
	endif

	# Default values for variables
	files = 0
	intervalstart = 0
	intervalend = 0
	interval = 1
	intname$ = ""
	intervalfile$ = ""
	endoffile = Get finishing time
	#comment Give an optional prefix for all filenames, here used to define speaker:
	prefix$ = "jeremy_eng_" 

	# Loop through all intervals in the selected tier of the TextGrid
	indexnumber = 1

	for interval from start_from to end_at
		select TextGrid 'gridname$'
		intname$ = ""
		intname$ = Get label of interval... tier interval
		check = 0
		if intname$ = "sp" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "I" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "LIKE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "HERE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "" and exclude_empty_labels = 1
			check = 1
		endif
		if check = 0
			intervalstart = Get starting point... tier interval
				if intervalstart > margin
					intervalstart = intervalstart - margin
				else
					intervalstart = 0
				endif
	
			intervalend = Get end point... tier interval
				if intervalend < endoffile - margin
					intervalend = intervalend + margin
				else
					intervalend = endoffile
				endif
	
			select LongSound 'soundname$'
			Extract part... intervalstart intervalend no
			filename$ = intname$
			
			intervalfile$ = "'folder$'" + "'prefix$'" + "'filename$'" + "'suffix$''indexnumber'" + ".wav"
			
			Write to WAV file... 'intervalfile$'
			Remove

			#append info to output text file, with info on longsound file, interval number, interval name, and soundfile name
			appendFileLine: "'output$'", "'prefix$'" ,tab$, "'indexnumber'" , tab$ ,"'intname$'", tab$ ,"'prefix$''indexnumber'"


			indexnumber = indexnumber + 1
		endif
	endfor


#Iteration 4: select the first LongSound and TextGrid Pair
selectObject: "LongSound Veronique_ABX_FR_clean"
plusObject: "TextGrid Veronique_ABX_FR_clean"

	gridname$ = selected$ ("TextGrid", 1)
	soundname$ = selected$ ("LongSound", 1)
	select TextGrid 'gridname$'
	numberOfIntervals = Get number of intervals... tier
	if start_from > numberOfIntervals
		exit There are not that many intervals in the IntervalTier!
	endif
	if end_at > numberOfIntervals
		end_at = numberOfIntervals
	endif
	if end_at = 0
		end_at = numberOfIntervals
	endif

	# Default values for variables
	files = 0
	intervalstart = 0
	intervalend = 0
	interval = 1
	intname$ = ""
	intervalfile$ = ""
	endoffile = Get finishing time
	#comment Give an optional prefix for all filenames, here used to define speaker:
	prefix$ = "veronique_fr_" 

	# Loop through all intervals in the selected tier of the TextGrid
	indexnumber = 1

	for interval from start_from to end_at
		select TextGrid 'gridname$'
		intname$ = ""
		intname$ = Get label of interval... tier interval
		check = 0
		if intname$ = "sp" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "JE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "STOCKE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "ICI" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "" and exclude_empty_labels = 1
			check = 1
		endif
		if check = 0
			intervalstart = Get starting point... tier interval
				if intervalstart > margin
					intervalstart = intervalstart - margin
				else
					intervalstart = 0
				endif
	
			intervalend = Get end point... tier interval
				if intervalend < endoffile - margin
					intervalend = intervalend + margin
				else
					intervalend = endoffile
				endif
	
			select LongSound 'soundname$'
			Extract part... intervalstart intervalend no
			filename$ = intname$
			
			intervalfile$ = "'folder$'" + "'prefix$'" + "'filename$'" + "'suffix$''indexnumber'" + ".wav"
			
			Write to WAV file... 'intervalfile$'
			Remove

			#append info to output text file, with info on longsound file, interval number, interval name, and soundfile name
			appendFileLine: "'output$'", "'prefix$'" ,tab$, "'indexnumber'" , tab$ ,"'intname$'", tab$ ,"'prefix$''indexnumber'"


			indexnumber = indexnumber + 1
		endif
	endfor


#Iteration 5: select the first LongSound and TextGrid Pair
selectObject: "LongSound Cecilia_ABX_FR_clean"
plusObject: "TextGrid Cecilia_ABX_FR_clean"

	gridname$ = selected$ ("TextGrid", 1)
	soundname$ = selected$ ("LongSound", 1)
	select TextGrid 'gridname$'
	numberOfIntervals = Get number of intervals... tier
	if start_from > numberOfIntervals
		exit There are not that many intervals in the IntervalTier!
	endif
	if end_at > numberOfIntervals
		end_at = numberOfIntervals
	endif
	if end_at = 0
		end_at = numberOfIntervals
	endif

	# Default values for variables
	files = 0
	intervalstart = 0
	intervalend = 0
	interval = 1
	intname$ = ""
	intervalfile$ = ""
	endoffile = Get finishing time
	#comment Give an optional prefix for all filenames, here used to define speaker:
	prefix$ = "cecilia_fr_" 

	# Loop through all intervals in the selected tier of the TextGrid
	indexnumber = 1

	for interval from start_from to end_at
		select TextGrid 'gridname$'
		intname$ = ""
		intname$ = Get label of interval... tier interval
		check = 0
		if intname$ = "sp" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "JE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "STOCKE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "ICI" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "" and exclude_empty_labels = 1
			check = 1
		endif
		if check = 0
			intervalstart = Get starting point... tier interval
				if intervalstart > margin
					intervalstart = intervalstart - margin
				else
					intervalstart = 0
				endif
	
			intervalend = Get end point... tier interval
				if intervalend < endoffile - margin
					intervalend = intervalend + margin
				else
					intervalend = endoffile
				endif
	
			select LongSound 'soundname$'
			Extract part... intervalstart intervalend no
			filename$ = intname$
			
			intervalfile$ = "'folder$'" + "'prefix$'" + "'filename$'" + "'suffix$''indexnumber'" + ".wav"
			
			Write to WAV file... 'intervalfile$'
			Remove

			#append info to output text file, with info on longsound file, interval number, interval name, and soundfile name
			appendFileLine: "'output$'", "'prefix$'" ,tab$, "'indexnumber'" , tab$ ,"'intname$'", tab$ ,"'prefix$''indexnumber'"


			indexnumber = indexnumber + 1
		endif
	endfor


#Iteration 6: select the first LongSound and TextGrid Pair
selectObject: "LongSound Remi_ABX_FR_clean"
plusObject: "TextGrid Remi_ABX_FR_clean"

	gridname$ = selected$ ("TextGrid", 1)
	soundname$ = selected$ ("LongSound", 1)
	select TextGrid 'gridname$'
	numberOfIntervals = Get number of intervals... tier
	if start_from > numberOfIntervals
		exit There are not that many intervals in the IntervalTier!
	endif
	if end_at > numberOfIntervals
		end_at = numberOfIntervals
	endif
	if end_at = 0
		end_at = numberOfIntervals
	endif

	# Default values for variables
	files = 0
	intervalstart = 0
	intervalend = 0
	interval = 1
	intname$ = ""
	intervalfile$ = ""
	endoffile = Get finishing time
	#comment Give an optional prefix for all filenames, here used to define speaker:
	prefix$ = "remi_fr_" 

	# Loop through all intervals in the selected tier of the TextGrid
	indexnumber = 1

	for interval from start_from to end_at
		select TextGrid 'gridname$'
		intname$ = ""
		intname$ = Get label of interval... tier interval
		check = 0
		if intname$ = "sp" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "JE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "STOCKE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "ICI" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "" and exclude_empty_labels = 1
			check = 1
		endif
		if check = 0
			intervalstart = Get starting point... tier interval
				if intervalstart > margin
					intervalstart = intervalstart - margin
				else
					intervalstart = 0
				endif
	
			intervalend = Get end point... tier interval
				if intervalend < endoffile - margin
					intervalend = intervalend + margin
				else
					intervalend = endoffile
				endif
	
			select LongSound 'soundname$'
			Extract part... intervalstart intervalend no
			filename$ = intname$
			
			intervalfile$ = "'folder$'" + "'prefix$'" + "'filename$'" + "'suffix$''indexnumber'" + ".wav"
			
			Write to WAV file... 'intervalfile$'
			Remove

			#append info to output text file, with info on longsound file, interval number, interval name, and soundfile name
			appendFileLine: "'output$'", "'prefix$'" ,tab$, "'indexnumber'" , tab$ ,"'intname$'", tab$ ,"'prefix$''indexnumber'"


			indexnumber = indexnumber + 1
		endif
	endfor


#Iteration 7: select the first LongSound and TextGrid Pair
selectObject: "LongSound Marc_ABX_FR_clean"
plusObject: "TextGrid Marc_ABX_FR_clean"

	gridname$ = selected$ ("TextGrid", 1)
	soundname$ = selected$ ("LongSound", 1)
	select TextGrid 'gridname$'
	numberOfIntervals = Get number of intervals... tier
	if start_from > numberOfIntervals
		exit There are not that many intervals in the IntervalTier!
	endif
	if end_at > numberOfIntervals
		end_at = numberOfIntervals
	endif
	if end_at = 0
		end_at = numberOfIntervals
	endif

	# Default values for variables
	files = 0
	intervalstart = 0
	intervalend = 0
	interval = 1
	intname$ = ""
	intervalfile$ = ""
	endoffile = Get finishing time
	#comment Give an optional prefix for all filenames, here used to define speaker:
	prefix$ = "marc_fr_" 

	# Loop through all intervals in the selected tier of the TextGrid
	indexnumber = 1

	for interval from start_from to end_at
		select TextGrid 'gridname$'
		intname$ = ""
		intname$ = Get label of interval... tier interval
		check = 0
		if intname$ = "sp" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "JE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "STOCKE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "ICI" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "" and exclude_empty_labels = 1
			check = 1
		endif
		if check = 0
			intervalstart = Get starting point... tier interval
				if intervalstart > margin
					intervalstart = intervalstart - margin
				else
					intervalstart = 0
				endif
	
			intervalend = Get end point... tier interval
				if intervalend < endoffile - margin
					intervalend = intervalend + margin
				else
					intervalend = endoffile
				endif
	
			select LongSound 'soundname$'
			Extract part... intervalstart intervalend no
			filename$ = intname$
			
			intervalfile$ = "'folder$'" + "'prefix$'" + "'filename$'" + "'suffix$''indexnumber'" + ".wav"
			
			Write to WAV file... 'intervalfile$'
			Remove

			#append info to output text file, with info on longsound file, interval number, interval name, and soundfile name
			appendFileLine: "'output$'", "'prefix$'" ,tab$, "'indexnumber'" , tab$ ,"'intname$'", tab$ ,"'prefix$''indexnumber'"


			indexnumber = indexnumber + 1
		endif
	endfor


#Iteration 8: select the first LongSound and TextGrid Pair
selectObject: "LongSound Cecilia_ABX_ENG_clean"
plusObject: "TextGrid Cecilia_ABX_ENG_clean"

	gridname$ = selected$ ("TextGrid", 1)
	soundname$ = selected$ ("LongSound", 1)
	select TextGrid 'gridname$'
	numberOfIntervals = Get number of intervals... tier
	if start_from > numberOfIntervals
		exit There are not that many intervals in the IntervalTier!
	endif
	if end_at > numberOfIntervals
		end_at = numberOfIntervals
	endif
	if end_at = 0
		end_at = numberOfIntervals
	endif

	# Default values for variables
	files = 0
	intervalstart = 0
	intervalend = 0
	interval = 1
	intname$ = ""
	intervalfile$ = ""
	endoffile = Get finishing time
	#comment Give an optional prefix for all filenames, here used to define speaker:
	prefix$ = "cecilia_eng_" 

	# Loop through all intervals in the selected tier of the TextGrid
	indexnumber = 1

	for interval from start_from to end_at
		select TextGrid 'gridname$'
		intname$ = ""
		intname$ = Get label of interval... tier interval
		check = 0
		if intname$ = "sp" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "I" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "LIKE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "HERE" and exclude_intervals_labeled_as_xxx = 1
			check = 1
		endif
		if intname$ = "" and exclude_empty_labels = 1
			check = 1
		endif
		if check = 0
			intervalstart = Get starting point... tier interval
				if intervalstart > margin
					intervalstart = intervalstart - margin
				else
					intervalstart = 0
				endif
	
			intervalend = Get end point... tier interval
				if intervalend < endoffile - margin
					intervalend = intervalend + margin
				else
					intervalend = endoffile
				endif
	
			select LongSound 'soundname$'
			Extract part... intervalstart intervalend no
			filename$ = intname$
			
			intervalfile$ = "'folder$'" + "'prefix$'" + "'filename$'" + "'suffix$''indexnumber'" + ".wav"
			
			Write to WAV file... 'intervalfile$'
			Remove

			#append info to output text file, with info on longsound file, interval number, interval name, and soundfile name
			appendFileLine: "'output$'", "'prefix$'" ,tab$, "'indexnumber'" , tab$ ,"'intname$'", tab$ ,"'prefix$''indexnumber'"

			
			indexnumber = indexnumber + 1
		endif
	endfor




endeditor
exitScript ( )
Close

