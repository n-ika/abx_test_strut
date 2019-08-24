 folder$  = "/Users/njurov/Documents/Diderot/Memoire_M2/abx_test_strut/stimuli_test/intervals/resample/"

Create Strings as file list: "list", folder$+ "/*.wav"
numberOfFiles = Get number of strings

for ifile to numberOfFiles
    printline Working on file 'ifile'
    select Strings list
    fileName$ = Get string: ifile
    base$ = fileName$ - ".wav"

    mysound= Read from file: folder$+"/"+ fileName$
    selectObject: mysound
    mysound =Resample: 44100, 50
    Rename:  base$
            

    newbase$ = base$ + ".wav"
    nowarn Write to WAV file: folder$+"/" + newbase$
    removeObject: mysound

endfor
