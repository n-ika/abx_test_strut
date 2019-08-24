HOW - NEW ABKHAZIA CORPUS AND DECODING:

    * copy phones.txt from corresponding language trained folder (i.e. from train folder of corpus)

    * copy variants.txt and silences.txt
    
    * generate files for the corpus: meta.txt, segments.txt, utt2spk.txt, lexicon.txt, text.txt

    * for old-version Julien's AM: copy-create ./lang from LM

    L_disambig.fst  L.fst  local  oov.int  oov.txt  phones  phones.txt  recipe  topo  words.txt

    * FEATURES:
        abkhazia features mfcc --cmvn --allow-downsample=true CORPUS
        (my files were sampled at different rates)

    * LM:
        abkhazia language -o OUT_FILE --recipe -n 1 CORPUS

    * DECODE:
        abkhazia decode sa -o OUT_FOLDER --recipe -l LM -a AM -f FEAT_FOLDER CORPUS

    * flat LM:
        unzip G.arpa.gz
        erase everything
        gzip it back

        make all the probabilities uniform in G.fst - to do this:
        fstprint --isymbols=LM/phones.txt --osymbols=LM/phones.txt  --save_isymbols=isymbols.txt --save_osymbols=osymbols.txt LM/G.fst LM/Gtest.txt

        change probabilities to e.g. 1

        fstcompile --isymbols=LM/phones.txt --osymbols=LM/phones.txt LM/Gtest.txt LM/Gtest.fst
        
        ALSO CHANGE IT HERE:
            ./recipe/data/local/language/G.fst

    * REMEMBER:
        - no spaces at the end of corpus files
        - check if phones tables are same for decoding as they were for AM training
        - check if lexicon.txt (dictionary) uses phones from the corresponding tables
        - if problems, delete ./tmp/ in lang folder and decode_fmllr in AM folder
