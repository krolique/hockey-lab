#!/bin/bash

# Cyclomatic Complexity score
# Scores the source code and generates letter grades per module/function.
# This table describes the grade and risk level:
# +----------+-------+-----------------------------------------+
# | CC score | Rank  |  Risk                                   |
# +----------+-------+-----------------------------------------+
# | 1 - 5    | A     | low - simple block                      |
# +----------+-------+-----------------------------------------+
# | 6 - 10   | B     | low - well structured and stable block  |
# +----------+-------+-----------------------------------------+
# | 11 - 20  | C     | moderate - slightly complex block       |
# +----------+-------+-----------------------------------------+
# | 21 - 30  | D     | more than moderate - more complex block |
# +----------+-------+-----------------------------------------+
# | 31 - 40  | E     | high - complex block, alarming          |
# +----------+-------+-----------------------------------------+
# | 41+      | F     | very high - error-prone, unstable block |
# +----------+-------+-----------------------------------------+

MIN_RANK=B

RANKED_BELOW=$(radon cc . -e "tests/*" --min $MIN_RANK | wc -l)

if [ "$RANKED_BELOW" -gt "0" ]
then
    radon cc . -e "tests/*" --min $MIN_RANK -s
    echo >&2 "[FAILED] cyclomatic complexity for some modules ranked lower than $MIN_RANK"
    exit 1
fi

echo "[PASS] cyclomatic complexity check passed"
exit 0
