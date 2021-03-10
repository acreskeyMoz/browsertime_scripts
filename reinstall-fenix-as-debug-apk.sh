#!/usr/bin/env bash

ADB="/home/bkoz/.mozbuild/android-sdk-linux/platform-tools/adb"
PRODUCT=org.mozilla.fenix
IDATE=`date +%Y%m%d`
FDEBUGBIN="/opt/mozilla/bin/fenix-nightly/fenix-nightly.${IDATE}.debug.apk"

phones=( 9C081FFBA002DU FA79G1A05075 RF8MB1E9NHB ce0516059d33130f04 )
for i in "${phones[@]}"
do
    echo $i
    $ADB -s $i uninstall org.mozilla.fenix
    $ADB -s $i install -t $FDEBUGBIN
done

echo "done installing $FDEBUGBIN"
