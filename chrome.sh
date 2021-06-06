#!/usr/bin/env bash

# LAST : 2021-03-24, 25
# USE
# ./chrome.sh 6 https://m.imdb.com/title/tt0083943/


DEVICEID=$1
CHROMEDRIVER_PREFIX="/opt/mozilla/bin/chromedriver"
if [ "$DEVICEID" -eq "1" ]; then
    ANDROID_SERIAL=9C081FFBA002DU #pixel4xl
    CHROMEDRIVER_PATH="$CHROMEDRIVER_PREFIX/chromedriver.89.0.4389.23"
fi
if [ "$DEVICEID" -eq "2" ]; then
    ANDROID_SERIAL=FA79G1A05075 #pixel2
    CHROMEDRIVER_PATH="$CHROMEDRIVER_PREFIX/chromedriver.89.0.4389.23"
fi
if [ "$DEVICEID" -eq "3" ]; then
    ANDROID_SERIAL=RF8MB1E9NHB #s10
    CHROMEDRIVER_PATH="$CHROMEDRIVER_PREFIX/chromedriver.89.0.4389.23"
fi
if [ "$DEVICEID" -eq "4" ]; then
    ANDROID_SERIAL=956AX0EZEZ #pixel3xl
    CHROMEDRIVER_PATH="$CHROMEDRIVER_PREFIX/chromedriver.89.0.4389.23"
fi
if [ "$DEVICEID" -eq "6" ]; then
    ANDROID_SERIAL=ce12160cf80eb22504
    CHROMEDRIVER_PATH="$CHROMEDRIVER_PREFIX/chromedriver.89.0.4389.23"
fi

# ANDROID_SERIAL=ce12160cf80eb22504 #s7 devpac
# ANDROID_SERIAL=2668b1b71a057ece #note9 devpac

echo "device $DEVICEID with address $ANDROID_SERIAL"


URL=$2
TLD=$(./strip-url-to-tld.sh "${URL}")
echo "shortened top level domain: $TLD"

OUTPUTBASE="browsertime-chrome"
OUTPUTNAME="${OUTPUTBASE}-${TLD}"
LOGVERBF="${OUTPUTNAME}.log"


ITERATIONS=10


PACKAGE=com.android.chrome

GOOG_OPTIONS1="--chrome.collectPerfLog true"
GOOG_OPTIONS2="--chrome.collectNetLog true"
GOOG_OPTIONS3="--collectLongTasks true"
GOOG_OPTIONS4="--chrome.cdp.performance"
GOOG_OPTIONS=""


#HAR_OPTIONS="--gzipHar --har ${OUTPUTNAME}"
HAR_OPTIONS="--skipHar"

#VIZM0="--video false --visualMetrics false"
VIZMF0="--video true --visualMetrics true"
VIZMF1="--videoParams.keepOriginalVideo true"
VIZMF2=" --videoParams.addTimer false --videoParams.createFilmstrip false"
VIZMF="$VIZMF0 $VIZMF1 $VIZMF2"


BT_OPTIONS="--browsertime.page_cycles 1 --browsertime.page_cycle_delay 1000 --browsertime.post_startup_delay 30000 --pageLoadStrategy none --pageCompleteCheckStartWait 5000 --pageCompleteCheckPollTimeout 1000 --timeouts.pageLoad 72000 --timeouts.script 72000"

# -vv for debug

/home/bkoz/.mozbuild/node/bin/node /home/bkoz/src/mozilla-gecko.git/tools/browsertime/node_modules/browsertime/bin/browsertime.js --browser chrome --chrome.android.deviceSerial "$ANDROID_SERIAL" --android --chrome.chromedriverPath="$CHROMEDRIVER_PATH" --webdriverPageload true --browsertime.url "$URL"  $BT_OPTIONS $HAR_OPTIONS $VIZMF -o "$OUTPUTNAME" -n $ITERATIONS "$URL" | grep INFO >> $LOGVERBF

echo "done with browsertime run(s)"

adb -s $ANDROID_SERIAL shell am force-stop $PACKAGE

echo "done stopping browser $PACKAGE"
