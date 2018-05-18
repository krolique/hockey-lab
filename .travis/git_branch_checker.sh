#!/bin/bash

# Git Branch Linter
# Enforces branch naming conventions by validating the
# `TRAVIS_PULL_REQUEST_BRANCH` variable injected into the execution context
# The policy is as follows:
# 1. only lower case letters, digits, '/', '-' and '.' characters can be used
# 2. the name of the branch cannot be longer than 50 characters
VALID_BRANCH_PATTERN="^[a-z,0-9,\.,\/,\-]{1,50}$"

if [[ -n "$TRAVIS_PULL_REQUEST_BRANCH" ]]
then
    if ! [[ "$TRAVIS_PULL_REQUEST_BRANCH" =~ $VALID_BRANCH_PATTERN ]]
    then
        echo >&2 "[FAILED] Branch name '$TRAVIS_PULL_REQUEST_BRANCH' does not conform to $VALID_BRANCH_PATTERN"
        exit 1
    fi
fi

echo "[PASS] git branch name check"
exit 0
