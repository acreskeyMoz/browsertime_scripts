#!/bin/bash
# N.B.: yargs doesn't parse `--firefox.android.intentArgument --ez`
# properly, so always use `=--ez`!

BASE='/home/jesup/src/mozilla/browsertime_on_android_scripts/'

#$BROWSERTIME_BIN \
#    --browser firefox                                               \
#N    --skipHar \
#    --firefox.binaryPath=/home/jesup/src/mozilla/pageload/obj-opt/dist/bin/firefox \
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
#!/bin/bash
# N.B.: yargs doesn't parse `--firefox.android.intentArgument --ez`
# properly, so always use `=--ez`!

BASE='/home/jesup/src/mozilla/browsertime_on_android_scripts/'

#$BROWSERTIME_BIN \
#    --browser firefox                                               \
#N    --skipHar \
#    --firefox.binaryPath=/home/jesup/src/mozilla/pageload/obj-opt/dist/bin/firefox \
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
