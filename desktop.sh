#!/bin/bash

$BROWSERTIME_BIN \
    --browser firefox \
    --skipHar \
    --firefox.binaryPath="$FIREFOX_BINARY_PATH" \
    "$@"
