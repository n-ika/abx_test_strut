cut_intervals: 
	python scripts/cut_all.py\
	--excluded-words JE,STOCKE,ICI,I,LIKE,HERE,sp\
	word ./stimuli/intervals outputs/interval_meta_information.csv\
	stimuli/Jeremy_ABX_ENG_corrected.TextGrid,stimuli/Jeremy_ABX_ENG_clean.wav\
	stimuli/Maureen_ABX_ENG_corrected.TextGrid,stimuli/Maureen_ABX_ENG_clean.wav\
	stimuli/Maureen_ABX_FR_corrected.TextGrid,stimuli/Maureen_ABX_FR_clean.wav\
	stimuli/Ewan_ABX_ENG_corrected.TextGrid,stimuli/Ewan_ABX_ENG_clean.wav\
	stimuli/Marc_ABX_FR_corrected.TextGrid,stimuli/Marc_ABX_FR_clean.wav\
	stimuli/Remi_ABX_FR_corrected.TextGrid,stimuli/Remi_ABX_FR_clean.wav\
	stimuli/Veronique_ABX_ENG_corrected.TextGrid,stimuli/Veronique_ABX_ENG_clean.wav\
	stimuli/Veronique_ABX_FR_corrected.TextGrid,stimuli/Veronique_ABX_FR_clean.wav

create_experimental_list:
	python scripts/create_stimlist2.py --seed 26 --nsteps 1000000 112 \
	intervals/interval_meta_information.csv experimental_list.csv

create_experimental_lists:
	python  ./scripts/fill_filenames_to_experimental_list.py  \
	./outputs/experimental_list.csv ./stimuli/intervals/ \
	./outputs/interval_meta_information.csv

concatenate_intervals:
	python ./scripts/concatenate_intervals.py ./stimuli/intervals/ \
	./outputs/Stimuli_list.txt ./stimuli/500ms_silence.wav \
	./stimuli/triplets

make_lmeds_sequence:
	python ./scripts/print_stim_to_table.py ./triplets/wavs \
	./lmeds_materials/sequence_to_be_fixed.txt

normalize_vectors:
	python ./scripts/normalize_vectors.py \
	./stimuli/mfccs/ \
	./stimuli/mfccs_norm/

calculate_distances:
	python ./scripts/dtw_distances.py \
	./outputs/distance_list.csv \
	./stimuli/mfccs_norm/ 

anonymize_lmeds_data:
	python ./analysis/scripts/anonymize_lmeds_data_filenames.py \
	./analysis/lmeds_results_not_github/eng \
	./analysis/anon_data/eng \
	./analysis/outputs/anon_table_eng.csv \
	&& python ./analysis/scripts/anonymize_lmeds_data_filenames.py \
	./analysis/lmeds_results_not_github/fr \
	./analysis/anon_data/fr \
	./analysis/outputs/anon_table_fr.csv \
	&& python ./analysis/scripts/anonymize_lmeds_data_filenames.py \
	./analysis/lmeds_results_not_github/fr2 \
	./analysis/anon_data/fr2 \
	./analysis/outputs/anon_table_fr2.csv

split_output_to_results_files:
	python ./analysis/scripts/split_output_to_results_files.py \
	./analysis/anon_data/ \
	./analysis/outputs/clean_results.csv \
	./analysis/outputs/presurvey.txt \
	./analysis/outputs/postsurvey.txt \
	./analysis/outputs/postsurvey2.txt

analysis_step1:
	Rscript --vanilla ./analysis/scripts/analysis_step1_preprocess_strut.Rscript \
	./analysis/outputs/presurvey.txt \
	./analysis/outputs/clean_results.csv \
	./analysis/outputs/postsurvey.txt \
	./analysis/outputs/postsurvey2.txt \
	./model/supervised/posterior_grams/ints/distances_supmodel_ints.csv \
	./analysis/outputs/analysed_data_FINALstim.csv

add_silence_to_ints:
	python ./model/supervised/intervals_for_model/downsampled/ \
	./stimuli/500ms_silence.wav \
	./model/supervised/intervals_for_model/wavs_silence/

supervised_model_files_intervals:
	python model/supervised/scripts/make_abkhazia_files_intervals.py \
	./outputs/distance_list.csv \
	./model/supervised/intervals_for_model

supervised_model_files_triplets:
	python ./model/supervised/scripts/get_times.py \
	./model/supervised/triplets_for_model/textgrid/ \
	./model/supervised/triplets_for_model/triplet_times.csv \
	&& python model/supervised/scripts/make_abkhazia_files_triplets.py \
	./outputs/distance_list.csv \
	./model/supervised/triplets_for_model/triplet_times.csv \
	./model/supervised/triplets_for_model/

supervised_model_files_fullwav:
	python ./model/supervised/scripts/get_full_wav_times.py \
	./model/supervised/full_wavs/txt_grids_full/ \
	./model/supervised/full_wavs/fullwav_times.csv \
	&& python model/supervised/scripts/make_abkhazia_files_entirewav.py \
	./model/supervised/full_wavs/fullwav_times.csv \
	./model/supervised/full_wavs/

trace_int_times:
	python model/supervised/scripts/intNfrom_txtgrids.py \
	model/supervised/full_wavs/clean_txtgrids/ \
	model/supervised/full_wavs/int_times_counts.csv \
	&& python ./model/supervised/scripts/trace_stim_from_wavs.py \
	./outputs/distance_list.csv \
	./model/supervised/full_wavs/int_times_counts.csv \
	./model/supervised/full_wavs/stim_backtraced.csv

supervised_model_write_kl_ints:
	python ./model/supervised/scripts/kaldi2features.py \
	./model/supervised/posterior_grams/ints/phones_en.txt \
	./model/supervised/posterior_grams/ints/phones_en.post \
	./model/supervised/posterior_grams/ints/post_en.h5 \
	./model/supervised/posterior_grams/extracted_pgs/phone_order_en.txt \
	&& python ./model/supervised/scripts/model_dtw_ints.py \
	./model/supervised/posterior_grams/ints/ outputs/distance_list.csv


levenshtein_distance_fr:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/intervals_for_model/fr/lexicon_all_cvcs.csv \
	./model/supervised/intervals_for_model/fr/text_fren.csv \
	./model/supervised/levenshtein_distance/ints/fr/ spk

levenshtein_distance_en:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/intervals_for_model/eng/lexicon_all_cvcs.csv \
	./model/supervised/intervals_for_model/eng/text_fren.csv \
	./model/supervised/levenshtein_distance/ints/en/ spk

levenshtein_distance_corpus_en:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/levenshtein_distance/test_corpora/lexicon_corp_en.txt \
	./model/supervised/levenshtein_distance/test_corpora/text_orig_en.txt \
	./model/supervised/levenshtein_distance/test_corpora/en/ -

levenshtein_distance_corpus_fr:
	python ./model/supervised/scripts/wrds2phns.py \
	./model/supervised/levenshtein_distance/test_corpora/lexicon_corp_fr.txt \
	./model/supervised/levenshtein_distance/test_corpora/text_orig_fr.txt \
	./model/supervised/levenshtein_distance/test_corpora/fr/ _

mfcc_ark:
	python ./model/supervised/scripts/dist_from_ark.py \
	./model/supervised/mfccs/ark/ \
	./outputs/distance_list.csv

make_mfccs_python:
	python ./model/supervised/scripts/make_mfccs.py \
	./model/supervised/intervals_for_model/wavs/ \
	./model/supervised/mfccs/povey_mfcc_py/

mfcc_dist:
	python ./model/supervised/scripts/mfcc_dist_python.py \
	./model/supervised/mfccs/povey_mfcc_py/ \
	./model/supervised/mfccs/ \
	./outputs/distance_list.csv

# change lang as needed
equiprob_lm:
	python ./model/supervised/scripts/equiprobable_lm.py \
	./model/supervised/intervals_for_model/eng/text_old.txt \
	./model/supervised/intervals_for_model/eng/comparison_table.csv \
	./model/supervised/intervals_for_model/eng/lexicon.txt \
	./model/supervised/intervals_for_model/eng/

# change lang as needed
copy_intervals:
	python ./model/supervised/scripts/copy_intervals_by_lang.py \
	./model/supervised/intervals_for_model/eng/segments.txt \
	./model/supervised/intervals_for_model/eng/wavs/

# change lang as needed
orthographic_lxcn:
	python ./model/supervised/scripts/lexicon_all_cvcs.py \
	./model/supervised/intervals_for_model/fr \
	&& python ./model/supervised/scripts/make_abkhazia_cvcs.py \
	./model/supervised/intervals_for_model/ \
	fr
# change utt_id as needed
extract_pg:
	python -m pdb ./model/supervised/scripts/extract_pg.py \
	./model/supervised/posterior_grams/ints/post_fr.h5 \
	spk03_triplet005_02 \
	triplet005_02_FR


dist_to_kmean:
	python model/unsupervised/scripts/dist_pqmean_stim.py \
	model/supervised/mfccs/ark/ \
	model/unsupervised/pqKmeans/1M_PQkmean_clustering/

kl_dtw_kmeans:
	python model/unsupervised/scripts/kl_kmeans.py \
	model/unsupervised/pqKmeans/1M_PQkmean_clustering/ \
	outputs/distance_list.csv \

# extract_bottleneck_feats:
# 	python shennong_distances/pq_kmeans/extract_bottleneck_feats.py \
#  	abkhazia_projects/fr_corpus_jan2019_abkhazia/split/train/data/wavs/ \
#  	french_bottleneck_feats

# CLUSTER
bottleneck_pqkmeans_clustering:
	python bottleneck_pqkmeans_clustering.py \
	../../../abkhazia_june/english_corpus/split/train/data/wavs/ \
	en
	
# CLUSTER
bottleneck_distances_kmeans:
	python bottle_dist_pqmean_stim.py \
	../../abkhazia_projects/intervals_en/data/wavs/ \
	pqk_clustering/


