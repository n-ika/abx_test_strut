triplet-list:
	python ./scripts/textgrid_to_abx_item_file_word.py word \
stimuli/Maureen_ABX_FR_corrected.TextGrid,Maureen_ABX_FR_clean.wav \
stimuli/Maureen_ABX_ENG_corrected.TextGrid,Maureen_ABX_ENG_clean.wav \
stimuli/Marc_ABX_FR_corrected.TextGrid,Marc_ABX_FR_clean.wav \
stimuli/Remi_ABX_FR_corrected.TextGrid,Remi_ABX_FR_clean.wav \
stimuli/Veronique_ABX_FR_corrected.TextGrid,Veronique_ABX_FR_clean.wav \
stimuli/Veronique_ABX_ENG_corrected.TextGrid,Veronique_ABX_ENG_clean.wav \
stimuli/Ewan_ABX_ENG_clean.TextGrid,Ewan_ABX_ENG_clean.wav \
stimuli/Jeremy_ABX_ENG_corrected.TextGrid,Jeremy_ABX_ENG_clean.wav \
--excluded-words=JE,STOCKE,ICI,I,LIKE,HERE,sp > ABX_ITEM_FILE.item \
&& Rscript --vanilla ./scripts/add_meta_information_to_item_file.Rscript \
ABX_ITEM_FILE.item ABX_ITEM_FILE_COMPLETE.item \
&& abx-task ABX_ITEM_FILE_COMPLETE.item ABX_TASK_FILE.task -o vowel \
-b context -a blml \
&& python ./scripts/task2txt.py ABX_TASK_FILE.task ABX_TASK_FILE.csv \
&& Rscript --vanilla ./scripts/add_meta_information_to_triplet_file.Rscript \
ABX_TASK_FILE.csv ABX_ITEM_FILE_COMPLETE.item ./outputs/triplets.csv \
&& python ./scripts/filter_blml.py ./outputs/triplets.csv