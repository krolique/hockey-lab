#!/bin/bash

# Style Guid Enforcement
# Reports the number of issues that do not pass the current style guide 

MIN_ISSUES=0

ISSUES=$(flake8 | wc -l)

if [ "$ISSUES" -gt "$MIN_ISSUES" ]
then
    flake8 --count
    echo >&2 "[FAILED] style guide enforcement found more than $MIN_ISSUES allowed issues"
    exit 1
fi

echo "[PASS] style guide enforcement passed"
exit 0
