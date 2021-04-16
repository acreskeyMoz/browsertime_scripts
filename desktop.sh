#!/bin/bash
# N.B.: yargs doesn't parse `--firefox.android.intentArgument --ez`
# properly, so always use `=--ez`!

BASE='/home/jesup/src/mozilla/browsertime_on_android_scripts/'
REPO='/home/jesup/src/mozilla/pageload/'

if test $PERF; then
    SCRIPT=${BASE}perf.sh
else
    SCRIPT=$FIREFOX_BINARY_PATH
fi
echo ./mach browsertime \
    --firefox.binaryPath=\'"$SCRIPT"\' \
  "$@"

./mach browsertime \
    --firefox.binaryPath=\'"$SCRIPT"\' \
  "$@"
