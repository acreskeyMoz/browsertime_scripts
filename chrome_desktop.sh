#!/bin/bash

$BROWSERTIME_BIN \
    --browser chrome \
    --skipHar \
    "$@"
