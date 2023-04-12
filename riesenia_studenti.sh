#!/bin/bash
# vim: et ts=4 sw=4 sta ai
# Toto je pre vyucujuceho, hlada to vsetky studentske riesenia
# studentom to nebude fungovat a tak to ma byt.
cat ../riesenia/repos |
    while read USER_REPO;
    do
        (cd ../riesenia/
        SRC=$(find $USER_REPO -name '*.py')
        NUM=$(echo $SRC | wc -l)
        if [ ! "$NUM" == "1" ]
        then 
            echo 'Zly pocet zdrojakov v' $USER_REPO > /dev/stderr
            continue
        fi
        RIESENIE='../riesenia/'"$SRC"
        NAME=`echo $RIESENIE | cut -f4 -d/`
        echo "$RIESENIE:$NAME"
        )
    done
