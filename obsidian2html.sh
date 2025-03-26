#!/usr/bin/env bash

pandoc \
    -f markdown+lists_without_preceding_blankline-smart \
    -t html \
    -o output.html "$1"
