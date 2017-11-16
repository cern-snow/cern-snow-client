#!/usr/bin/env bash

# This file should be run from the root directory, i.e.
# tests/run.sh
# instead of
# ./run.sh

# Run the tests the Python 2.6 way, to make sure they can run in lxplus.cern.ch (2.6) and aiadm.cern.ch (2.7)
python -m tests.test_session_basic_auth
python -m tests.test_session_sso_oauth
python -m tests.test_record_basic_auth
python -m tests.test_record_sso_oauth
python -m tests.test_record_field
