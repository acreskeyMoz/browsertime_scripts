#!/bin/bash
echo perf record -g -F 999 $FIREFOX_BINARY_LOCATION $* >/tmp/command
perf record -g -F 999 $FIREFOX_BINARY_LOCATION $*
