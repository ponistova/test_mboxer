#!/bin/bash
# vim: et ts=4 sw=4 sta ai

echo '>>> Converting source code'
rm -r source 2>/dev/null
mkdir -p source
./riesenia.sh $@ |
while IFS=: read RIESENIE NAME ; do
    if [ "$NAME" == "" ]
    then
        NAME="noname"
    fi
    OUT="source/${NAME}.html"
    echo "$RIESENIE" '->' "$OUT"
    pygmentize -l python -f html -O full -O linenos -o "$OUT" $RIESENIE
done


