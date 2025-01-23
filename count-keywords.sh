#!/bin/bash

# Usage:
#  cat KEYWORDS | check-keywords.sh

echo "#files  #matches keywords"
echo "--------------------------------------"

while read -r line; do
    file_count=`grep -iwl --no-filename "$line" *.rst | wc -l`
    word_count=`grep -iw --no-filename "$line" *.rst | wc -l`
    echo -e "$file_count\t$word_count\t $line"
done | sort -nr

