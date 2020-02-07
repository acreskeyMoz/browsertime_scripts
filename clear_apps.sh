#!/bin/bash

apps=("org.mozilla.firefox" \
      "org.mozilla.geckoview_example" \
      "org.mozilla.fenix" \
      "org.mozilla.fenix.beta" \
      "org.mozilla.fenix.performancetest" \
      "org.mozilla.fennec_aurora")

for app in ${apps[@]}; do
  echo adb -s $ANDROID_SERIAL shell am force-stop $app
  adb -s $ANDROID_SERIAL shell am force-stop $app
  echo adb -s $ANDROID_SERIAL shell am clear $app
  adb -s $ANDROID_SERIAL shell pm clear $app
done
