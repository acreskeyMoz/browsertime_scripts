#!/bin/bash

#: PACKAGE ${PACKAGE:=org.mozilla.firefox}
: PACKAGE ${PACKAGE:=org.mozilla.fenix.performancetest}

export adb_bin="/home/jesup/.mozbuild/android-sdk-linux/platform-tools/adb"

if [[ -n $ANDROID_SERIAL ]] ; then
    DEVICE_SERIAL_ARGS="--firefox.android.deviceSerial=$ANDROID_SERIAL --chrome.android.deviceSerial=$ANDROID_SERIAL"
else
    DEVICE_SERIAL_ARGS=
fi

export BROWSERTIME_BIN=tools/browsertime/node_modules/browsertime/bin/browsertime.js

# N.B.: yargs doesn't parse `--firefox.android.intentArgument --ez`
# properly, so always use `=--ez`!
$BROWSERTIME_BIN \
    --android \
    --skipHar \
    --firefox.geckodriverPath="/home/jesup/src/mozilla/browsertime_on_android_scripts/geckodriver" \
    --firefox.android.package "$PACKAGE" \
    --firefox.android.activity "org.mozilla.fenix.IntentReceiverActivity" \
    --firefox.android.intentArgument=-a \
    --firefox.android.intentArgument=android.intent.action.VIEW \
    --firefox.android.intentArgument=-d \
    --firefox.android.intentArgument="data:," \
    --browser firefox \
    --firefox.binaryPath=/tmp/foo \
    --firefox.android.intentArgument=--ez \
    --firefox.android.intentArgument=performancetest \
    --firefox.android.intentArgument=true \
    --firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 5  --firefox.geckoProfilerParams.features "js,stackwalk,leaf" --firefox.geckoProfilerParams.threads "GeckoMain,socket,url,ava,cert,html" \
    --pageCompleteWaitTime 10000 \
    -n 3 \
    --resultDir "browsertime-results/remote_settings_condprof/" \
    --browsertime.url https://www.google.com/ \
    --firefox.profileTemplate=/home/jesup/src/mozilla/browsertime_on_android_scripts/fenix.profile \
    --firefox.preference services.settings.loglevel:debug \
    https://www.google.com/ 

$adb_bin -s $ANDROID_SERIAL shell am force-stop $PACKAGE
