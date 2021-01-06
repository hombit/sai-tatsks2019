#!/bin/sh

python /app/weath.py < /app/params.txt &
PID=$!
sleep 200
kill $PID
