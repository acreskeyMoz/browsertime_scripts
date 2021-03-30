#!/usr/bin/env bash

# LAST : 2021-03-05, 26
# USE
# ./create-debuggable-apk.sh /path/to/binary.apk

# Path like: /opt/mozilla/FNPRMS/bin/2021/03/01/fenix-nightly.apk
# NB: assume the directory containing this apk is writable
#IFILE=$1
IDATE=`date +%Y/%m/%d`
IFILE="/opt/mozilla/FNPRMS/bin/${IDATE}/fenix-nightly.apk"
if [ ! -n "$IFILE" ]; then
    echo "no input file.apk given, exiting..."
    exit 1;
fi


# Get output/rewritten file name.
filebase="${IFILE##*/}"
idirbase="${IFILE%/*}"
odirbase="/opt/mozilla/bin/fenix-nightly"
EXT="${filebase##*.}"
FILE="${filebase%.*}"
ODATE=`date +%Y%m%d`
OFILE="$odirbase/$FILE.$ODATE.debug.apk"
OAFILE="$odirbase/$FILE.$ODATE.debug-aligned.apk"

# Condition check: find state of debug
DEBUGP=`aapt dump badging $IFILE | grep -c application-debuggable`
echo "debug flag set to: $DEBUGP"
if [ "$DEBUGP" -eq "1" ]; then
    echo "apk file is debuggable already, exiting";
    exit 2;
fi


# Use apktool to dump/uncompress the file into output directory.
# NB: assumes apktool in PATH and correctly configured
ODIR=odir
WDIR=`pwd`
if [ -d "$ODIR" ]; then
    echo "removing previous output directory"
    rm -rf "$ODIR"
fi
apktool d -o "$ODIR" "$IFILE"


# Edit manifest to be debuggable
# (change '<application' to '<application android:debuggable="true"')
MFILE="AndroidManifest.xml"
if [ -f "${ODIR}/${MFILE}" ]; then
    echo "found $MFILE, editing..."
    cd "$ODIR";
    sed 's/application /application android\:debuggable\=\"true\" /g' < $MFILE > temp
    mv temp $MFILE
    cd "$WDIR";
    echo "done editing, returning to working directory $WDIR"
else
    echo "did not find $ODIR/$MFILE, exiting..."
    exit 3;
fi


# Recompress the files into an apk.
apktool --use-aapt2 b -o "$OFILE" "$ODIR"
if [ ! -f "$OFILE" ]; then
    echo "could not re-assemble the debug file, exiting";
    exit 4;
fi

# For Android 10, needs resources.arsc to be uncompressed and 4 byte aligned.
zipalign -f -p 4 "$OFILE" "$OAFILE"
if [ ! -f "$OAFILE" ]; then
    echo "could not align the debug file, exiting";
    exit 5;
else
    mv "$OAFILE" "$OFILE" 
    echo "zipalign debug file complete"
fi


# Self-sign so that adb can install it.
# NB use -keypass/-storepass $KPASS to sign with password.
ALIAS=perfdebug
KSTORE="${WDIR}/resign.keystore"
KPASS=foxkeh
if [ ! -f "$KSTORE" ]; then
    echo "Generating resign keystore..."
    keytool -genkey -v -keystore "$KSTORE" -alias "$ALIAS" -keyalg RSA -keysize 2048 -validity 10000
fi
#jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "$KSTORE" -storepass "$KPASS" "$OFILE" "$ALIAS"

apksigner sign --ks "$KSTORE" --ks-key-alias "$ALIAS" --ks-pass pass:"$KPASS" "$OFILE"


# Done.
echo "finished creating self-signed and debuggable apk file: $OFILE"
