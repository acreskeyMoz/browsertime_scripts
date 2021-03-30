#!/usr/bin/env tcsh

set DEVICEID=$1
set DATESTAMP=`date --iso`

cd /opt/mozilla/browsertime.git;


set startt=`date`

# 1
./run-through-sites.sh $DEVICEID $DATESTAMP fenix-nightly.sh sites.txt

# 2
./run-through-sites.sh $DEVICEID $DATESTAMP chrome.sh sites.txt


set endt=`date`

echo $startt
echo $endt
