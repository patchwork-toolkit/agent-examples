#!/bin/bash


COUNT=`ps -A | wc -l | tr -d ' '`
TS=$(date +%s)
echo "{\"count\":${COUNT},\"timestamp\":${TS}}"

exit 0