#!/usr/bin/env bash

pandoc \
    -f markdown+lists_without_preceding_blankline-smart \
    -t docx \
    -o output.docx \
    --resource-path="~/Library/Mobile Documents/iCloud~md~obsidian/Documents/limelead-quartz" \
    --embed-resources \
    "$1" \
