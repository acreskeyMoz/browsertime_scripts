#!/bin/bash
# XXX get where this script was loaded from instead
BASE='/home/jesup/src/mozilla/browsertime_on_android_scripts/'

if test $PERF; then
    SCRIPT=${BASE}perf.sh
else
    SCRIPT=$FIREFOX_BINARY_LOCATION
fi
echo ./mach browsertime \
    --firefox.binaryPath=\'"$SCRIPT"\' \
  "$@"

./mach browsertime \
    --firefox.binaryPath=\'"$SCRIPT"\' \
  "$@"
