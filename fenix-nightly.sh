#!/usr/bin/env bash

# LAST : 2021-02-16, 23, 2021-03-03
# USE
# ./fenix-nightly.sh 6 https://m.imdb.com/title/tt0083943/


DEVICEID=$1
if [ "$DEVICEID" -eq "1" ]; then
    ANDROID_SERIAL=9C081FFBA002DU #pixel4xl
fi
if [ "$DEVICEID" -eq "2" ]; then
    ANDROID_SERIAL=FA79G1A05075 #pixel2
fi
if [ "$DEVICEID" -eq "3" ]; then
    ANDROID_SERIAL=RF8MB1E9NHB #s10
fi
if [ "$DEVICEID" -eq "4" ]; then
    ANDROID_SERIAL=956AX0EZEZ #pixel3xl
fi
if [ "$DEVICEID" -eq "6" ]; then
    ANDROID_SERIAL=ce0516059d33130f04 #s7 SFO
fi

# ANDROID_SERIAL=ce12160cf80eb22504 #s7 devpac
# ANDROID_SERIAL=2668b1b71a057ece #note9 devpac

echo "device $DEVICEID with address $ANDROID_SERIAL"


URL=$2
TLD=$(./strip-url-to-tld.sh "${URL}")
echo "shortened top level domain: $TLD"

OUTPUTBASE="browsertime-fenix-nightly"
OUTPUTNAME="${OUTPUTBASE}-${TLD}"
LOGVERBF="${OUTPUTNAME}-verbose.log"


ITERATIONS=10


#PACKAGE="org.mozilla.firefox_beta"
PACKAGE="org.mozilla.fenix"


MOZ1="--firefox.preference network.http.speculative-parallel-limit:6"
MOZ2="--firefox.preference gfx.webrender.force-disabled:true"
MOZ_OPTIONS="$MOZ1 $MOZ2"


# For --android-storage args (sdcard, internal, app, auto) see
# https://firefox-source-docs.mozilla.org/testing/geckodriver/Flags.html
# NB: sdcard does not work on Android >= 11.
#     app requires debuggable
#     internal requires root

GECKODRIVER_PREFIX="/opt/mozilla/bin/geckodriver"
#GECKODRIVER_PATH="$GECKODRIVER_PREFIX/geckodriver-v0.29.0"
GECKODRIVER_PATH="$GECKODRIVER_PREFIX/geckodriver-v0.30.20210223"

GECKODF1='--firefox.geckodriverArgs="--log" --firefox.geckodriverArgs="trace"'
GECKODF2='--firefox.geckodriverArgs="--android-storage" --firefox.geckodriverArgs="app"'

GECKODRIVERF="--firefox.geckodriverPath=$GECKODRIVER_PATH $GECKODF1 $GECKODF2"


#VIZM0="--video false --visualMetrics false"
VIZMF0="--video true --visualMetrics true"
VIZMF1="--videoParams.keepOriginalVideo true"
VIZMF2=" --videoParams.addTimer false --videoParams.createFilmstrip false"
VIZMF="$VIZMF0 $VIZMF1 $VIZMF2"


BT_OPTIONS="--browsertime.page_cycles 1 --browsertime.page_cycle_delay 1000 --browsertime.post_startup_delay 30000 --pageLoadStrategy none --pageCompleteCheckStartWait 5000 --pageCompleteCheckPollTimeout 1000 --timeouts.pageLoad 72000 --timeouts.script 72000"


/home/bkoz/.mozbuild/node/bin/node /home/bkoz/src/mozilla-gecko.git/tools/browsertime/node_modules/browsertime/bin/browsertime.js --browser firefox --firefox.android.deviceSerial "$ANDROID_SERIAL" $GECKODRIVERF --android --firefox.android.package "$PACKAGE" --firefox.android.activity "org.mozilla.fenix.IntentReceiverActivity" --firefox.android.intentArgument=-a --firefox.android.intentArgument android.intent.action.VIEW --firefox.android.intentArgument=-d --firefox.android.intentArgument about:blank --firefox.disableBrowsertimeExtension true --webdriverPageload true --browsertime.url "$URL"  $BT_OPTIONS --skipHar $MOZ_OPTIONS $VIZMF -o "$OUTPUTNAME" -n $ITERATIONS "$URL" | grep INFO >> $LOGVERBF

echo "done with browsertime run(s)"

adb -s $ANDROID_SERIAL shell am force-stop $PACKAGE

echo "done stopping browser $PACKAGE"
