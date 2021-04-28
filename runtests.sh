#!/bin/bash
# vim: et ts=4 sw=4 sta ai
./getsource.sh
(
cat << THEEND
<!DOCTYPE html>
<html>
<head>
<meta encoding="utf-8">
<style>
.passed {
    color:green;
}
.failed {
    color:red;
}
</style>
</head>
<body>
<h1>Testy</h1>
<h2>
THEEND
date
cat << THEEND
</h2>
<table border="1">
THEEND


TESTS=`echo test??`

echo '<tr>'
echo '<th>*</th>'
for TEST in $TESTS; do
    echo '<th>' `cat $TEST/test.name | sed 's/+/<br>/g'` '</th>'
    rm -r $TEST/results 2>/dev/null
    mkdir $TEST/results
done
echo '</tr>'
./riesenia.sh $@ |
while IFS=: read RIESENIE NAME ; do
    if [ "$NAME" == "" ]
    then
        NAME="noname"
    fi
    ERR=results/test_${NAME}.err
    OUT=results/test_${NAME}.txt 
    echo '<tr>'
    echo '<th> <a href="source/'${NAME}'.html">'${NAME}'</a></th>'
    for TEST in $TESTS; do
        cd $TEST
        bash test.sh ../$RIESENIE 2>${ERR} >${OUT}
        EXIT_STATUS=$?
        sleep 0.1
        echo '<td>'
        if [ "$EXIT_STATUS" == "0" ]
        then
            CLASS='passed'
            MARK='✓'
        else
            CLASS='failed'
            MARK='X'
        fi
        echo '<span class="'$CLASS'">'$MARK'</span>'
        echo '<a href="'$TEST/${OUT}'">&gt;&gt;</a>'
        if [ ! -s ${ERR} ]; then
	    	rm ${ERR}
        else
            echo '<a href="'$TEST/${ERR}'">err&gt;&gt;</a>'
	    fi
        echo '</td>'
        cd ..
        killall python 2>/dev/null
        killall python3 2>/dev/null
    done
    echo '</tr>'
done
cat <<THEEND
</table>
</body>
</html>
THEEND
) | tee results.html

