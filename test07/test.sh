killall python3 2>/dev/null
( python3 "$1"  >/dev/null& )
PID=$!
sleep 0.2
python3 test.py
EXIT_STATUS=$?
echo -------------
killall python3 2>/dev/null
exit $EXIT_STATUS
