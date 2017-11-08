#!/usr/bin/env bash

# This file should be run from the current directory, i.e.
# ./copy_docs_to_eos.sh

rsync -av --delete docs/_build/html/ /eos/project/s/servicenow/www/snow-client-docs