#!/bin/bash

## Creates the (unique) union article title list for two matched ID files
## Usage: filter_union.sh <file1> <file2>

while read line; do
	title=`echo $line | cut -f2 -d$'\t'`
	match=`cat $2 | grep $title`
	if [[ -z $match ]]; then
		echo $line >> ${1}.${2}.uu
	fi
done < $1	