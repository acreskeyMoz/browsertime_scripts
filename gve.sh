#!/bin/bash

: PACKAGE ${PACKAGE:=org.mozilla.geckoview_example}

sh ./clear_apps.sh

if [[ -n $ANDROID_SERIAL ]] ; then
    DEVICE_SERIAL_ARGS="--firefox.android.deviceSerial=$ANDROID_SERIAL --chrome.android.deviceSerial=$ANDROID_SERIAL"
else
    DEVICE_SERIAL_ARGS=
fi

# N.B.: yargs doesn't parse `--firefox.android.intentArgument --ez`
# properly, so always use `=--ez`!
$BROWSERTIME_BIN \
    --android \
    --skipHar \
    --firefox.geckodriverPath="$GECKODRIVER_PATH" \
    --firefox.android.package "$PACKAGE" \
    --firefox.android.activity "$PACKAGE.GeckoViewActivity" \
    --firefox.android.intentArgument=-a \
    --firefox.android.intentArgument=android.intent.action.VIEW \
    --firefox.android.intentArgument=-d \
    --firefox.android.intentArgument="data:," \
    --browser firefox \
    $DEVICE_SERIAL_ARGS \
    "$@"

adb -s $ANDROID_SERIAL shell am force-stop org.mozilla.geckoview_example
