#!/usr/bin/env bash

cd stimuli/norm_intervals
for i in *.wav ; do sox "$i" -r 16000 "converted/$i"; done
for i in *.wav ; do sox "$i" "$(basename -s .wav "$i").mp3"; done
for i in *.wav ; do sox "$i" "$(basename -s .wav "$i").ogg"; done