#!/bin/bash
#
# Will take all the JSON items in data and build HTML reports for each file.
#

for file in $(find ../input/ -type f -name "*.json")
do
    BASENAME=$(echo "${file##*/}" | cut -d'.' -f1)
    DATE=$(date +%Y-%m-%d)

    echo "$BASENAME"
    ./edx_course_html.py "$file" --id-only > ../output/"$BASENAME"_"$DATE".html
done
