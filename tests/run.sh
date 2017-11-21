#!/usr/bin/env bash

# This file should be run from the root directory, i.e.
# tests/run.sh
# instead of
# ./run.sh

# Run the tests the Python 2.6 way, to make sure they can run in lxplus.cern.ch (2.6) and aiadm.cern.ch (2.7)
echo -e "\n\npython -m tests.test_session_basic_auth"
python -m tests.test_session_basic_auth

echo -e "\n\npython -m tests.test_session_sso_oauth"
python -m tests.test_session_sso_oauth

echo -e "\n\npython -m tests.test_record_basic_auth"
python -m tests.test_record_basic_auth

echo -e "\n\npython -m tests.test_record_sso_oauth"
python -m tests.test_record_sso_oauth

echo -e "\n\npython -m tests.test_record_field"
python -m tests.test_record_field

echo -e "\n\npython -m tests.test_task_basic_auth"
python -m tests.test_task_basic_auth

echo -e "\n\npython -m tests.test_task_sso_oauth"
python -m tests.test_task_sso_oauth

echo -e "\n\npython -m tests.test_incident_basic_auth"
python -m tests.test_incident_basic_auth

echo -e "\n\npython -m tests.test_incident_sso_oauth"
python -m tests.test_incident_sso_oauth
