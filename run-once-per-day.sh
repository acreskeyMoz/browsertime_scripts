#!/usr/bin/env tcsh

set DEVICEID=$1

#source ~bkoz/.tcshrc-moz

cd /opt/mozilla/browsertime.git;


set startt=`date`

# 1
./run-through-sites.sh $DEVICEID fenix-nightly.sh sites.txt

# 2
#./run-through-sites.sh $DEVICEID chrome.sh sites.txt


set endt=`date`

echo $startt
echo $endt
