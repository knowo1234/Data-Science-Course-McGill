#!/bin/bash
#this script is for analyzing tweet data of more than 10,000 tweets and
#giving us a summary of its stats

if [[ $(wc -l <$1) -le 10000 ]]
then
        echo "ERROR: file is smaller than 10,000 lines."
        exit
fi

wc -l <$1
head -n 1 $1
tail -n 10000 $1 | grep -i potus | wc -l
head -n 200 $1 | tail -n -101 | grep -w "fake" $1 | wc -l