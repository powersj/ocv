#!/bin/bash
#
# Will take all the JSON items in data and build HTML reports for each file.
#

for file in $(find ../input/ -type f -name "*.json")
do
    echo "$BASENAME"
    ./edx_course_html.py "$file" --id-only
done
