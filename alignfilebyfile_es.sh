#!/bin/bash

interventions='/home/alina/Desktop/interventions_es/*.en'

for enfile in $interventions
do
    esfile=${enfile/.en/.es}
    esfiletok=${esfile/.es/.es.tok}
    enfiletok=${enfile/.en/.en.tok}
    ladder=${enfile/.en/.ladder}
    python3 /home/alina/pCloudDrive/UniSaarland/01_Projects/B7/03_scripts/habeas-corpus/tok-tok/toktok.py -t Moses -l en < "$enfile" > "$enfiletok"
    echo "English file tokenized"
    python3 /home/alina/pCloudDrive/UniSaarland/01_Projects/B7/03_scripts/habeas-corpus/tok-tok/toktok.py -t Moses -l es < "$esfile" > "$esfiletok"
    echo "Spanish file tokenized"
    alfile=${enfile/.en/.aligned}
    
    /home/alina/hunalign-1.1/src/hunalign/hunalign /home/alina/pCloudDrive/UniSaarland/01_Projects/B7/02_data/europarl-uds/es-en "$enfiletok" "$esfiletok"  -realign -autodict=dic.es-en > "$ladder"
    echo "Ladder file for '$ladder' is created!!!!!!!!!"
    /home/alina/hunalign-1.1/scripts/ladder2text.py "$ladder" "$enfile" "$esfile" > "$alfile"
    echo "File '$alfile' is aligned"
done
