#!/bin/bash

apps=("org.mozilla.firefox" \
      "org.mozilla.geckoview_example" \
      "org.mozilla.fenix" \
      "org.mozilla.fenix.beta" \
      "org.mozilla.fenix.performancetest" \
      "org.mozilla.fennec_aurora")

export adb_bin=/home/jesup/.mozbuild/android-sdk-linux/platform-tools/adb
for app in ${apps[@]}; do
  echo $adb_bin -s $ANDROID_SERIAL shell am force-stop $app
  $adb_bin -s $ANDROID_SERIAL shell am force-stop $app
  echo $adb_bin -s $ANDROID_SERIAL shell pm clear $app
  $adb_bin -s $ANDROID_SERIAL shell pm clear $app
done
