#!/usr/bin/env bash

# This file should be run from the root directory, i.e.
# tests/run_python27.sh
# instead of
# ./run_python27.sh

# Run the tests the Python 2.7 way

echo -e "python -m unittest discover tests"
python -m unittest discover tests
