#!/usr/bin/env bash
# usage: runjsfl.sh script.jsfl logfile [timeout_s]
# Hands the JSFL to the running Animate instance, then waits for the log file.
JS="$1"; LOG="$2"; TO="${3:-120}"
rm -f "$LOG"
WIN=$(cygpath -w "$JS")
"/c/Program Files/Adobe/Adobe Animate 2024/Animate.exe" "$WIN" >/dev/null 2>&1 &
for ((i=0;i<TO;i++)); do [ -f "$LOG" ] && { sleep 1; cat "$LOG"; exit 0; }; sleep 1; done
echo "TIMEOUT waiting for $LOG"; exit 1
