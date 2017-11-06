#!/usr/bin/env bash

# This file should be run from the root directory, i.e.
# docs/generate_docs.sh
# instead of
# ./generate_docs.sh

rm -r docs/*.html
pydoc -w ./
mv *.html docs/.