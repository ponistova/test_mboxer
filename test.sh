#killall python3 2>/dev/null
if [ -e test_prepare.sh ]
then	
	source test_prepare.sh
fi
python3 "$1"  >/dev/null& 
PIDRIESENIE=$!
sleep 0.2
python3 test.py
EXIT_STATUS=$?
kill -sTERM $PIDRIESENIE 2>/dev/null
echo '>>>' Killed PID "$PIDRIESENIE"
echo '>>> Checking with ps:' $(ps --pid $PIDRIESENIE)
echo '>>> Test exit status:' "$EXIT_STATUS"
if [ -e test_cleanup.sh ]
then	
	source test_cleanup.sh
fi
exit $EXIT_STATUS
