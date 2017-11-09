#!/usr/bin/env bash

# This file should be run from the current directory, i.e.
# ./copy_docs_to_eos_qa.sh

rsync -av --delete _build/html/ /eos/project/s/servicenow/www/snow-client-docs-qa