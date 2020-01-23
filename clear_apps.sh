#!/bin/bash

apps=("org.mozilla.firefox" \
      "org.mozilla.geckoview_example" \
      "org.mozilla.fenix.beta" \
      "org.mozilla.fenix.performancetest" \
      "org.mozilla.fennec_aurora" \
      "org.mozilla.reference.browser" \
      "com.android.chrome")

for app in ${apps[@]}; do
  adb -s $ANDROID_SERIAL shell am force-stop $app
  adb -s $ANDROID_SERIAL shell pm clear $app
done
