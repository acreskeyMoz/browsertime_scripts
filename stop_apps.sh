#!/bin/bash

myapps=("org.mozilla.firefox" \
      "org.mozilla.geckoview_example" \
      "org.mozilla.fenix.beta" \
      "org.mozilla.fenix.performancetest" \
      "org.mozilla.fennec_aurora" \
      "org.mozilla.reference.browser" \
      "com.android.chrome")

export adb_bin=/home/jesup/.mozbuild/android-sdk-linux/platform-tools/adb

for app in ${myapps[@]}; do
  echo $adb_bin -s $ANDROID_SERIAL shell am force-stop $app
  $adb_bin -s $ANDROID_SERIAL shell am force-stop $app
done
