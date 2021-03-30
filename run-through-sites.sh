#!/usr/bin/env bash

NPATH=/home/bkoz/.mozbuild/node/bin
PPATH=/opt/mozilla/mozilla-gecko.git/obj-x86_64-pc-linux-gnu/_virtualenvs/init_py3/bin
export PATH=$NPATH:$PPATH:$PATH
echo `which node`
echo `which python`

DEVICEID=$1
DATESTAMP=$2
SCRIPT=$3
SITES=$4

scriptdir=${BASH_SOURCE%/*}
echo $scriptdir
cd ${scriptdir}

BEGINTIME=`date`

for i in `cat ${SITES}`
do
    echo "$i"
    ./${SCRIPT} ${DEVICEID} "$i"
done

ENDTIME=`date`
echo "begin: $BEGINTIME"
echo "end: $ENDTIME"

# Move verbose logs into results folder.
mv *verbose.log browsertime-results/

# Rename results folder.
PRODUCT=`echo $SCRIPT | sed 's/.sh//'`
mv browsertime-results browsertime-results-${DATESTAMP}-${PRODUCT}-${DEVICEID}
