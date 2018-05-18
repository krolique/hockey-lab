#!/bin/bash

# Maintainability Index score
# Scores the source code and generates letter grades per module/function.
# This table describes the grade and risk level:
# +----------+------+------------------+
# | MI score | Rank | Maintainability  |
# +----------+------+------------------+
# | 100 - 20 | A    | Very high        |
# +----------+------+------------------+
# | 19 - 10  | B    | Medium           |
# +----------+------+------------------+
# | 9 - 0    | C    | Extremely low    |
# +----------+------+------------------+

MIN_RANK=B

RANKED_BELOW=$(radon mi . -e "tests/*" --min $MIN_RANK | wc -l)

if [ "$RANKED_BELOW" -gt "0" ]
then
    radon mi . -e "tests/*" --min $MIN_RANK -s
    echo >&2 "[FAILED] maintainability for some modules ranked lower than $MIN_RANK"
    exit 1
fi

echo "[PASS] maintainability check passed"
exit 0
