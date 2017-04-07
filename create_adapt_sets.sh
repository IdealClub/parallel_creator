#!/bin/bash

## To be executed from the directory where files are stored
## split_intesect.sh and id_extract.sh as well as in_domain_extraction.py must be present
## Args:
## $1 -- top-N
## $2 -- max split
## $3 -- corpus A
## $4 -- corpus B
## $5 -- article sentence counts file
## $6 -- lang 1
## $7 -- lang 2


for sim in  a c s; do
	## get top ranking and extract corresponding sentences
	cat *.${sim}sim.ind | sort -k4 -n | tail -n $1 > ${sim}sim.top${1}
	./split_intersect.sh ${sim}sim.top${1} $2
	./id_extract.sh $3 $4 $5 ${sim}sim.top${1}
	mkdir -p ${sim}.${1} 
	mv *.a *.b ${sim}.${1}
	rm ${sim}sim.top${1} ${sim}sim.top${1}*
	
	## create training corpus
	cd ${sim}.${1}
	cat *.a >> ${6}-${7}.${6}
	cat *.b >> ${6}-${7}.${6}
	
	## append tags and filter
	sed "s/|/\& 124 ;/g" ${6}-${7}.${6} | sed "s/^/&<2${7}>/g" > ${6}-${7}.${6}.2${7}
	sed "s/|/\& 124 ;/g" ${6}-${7}.${7} | sed "s/^/&<2${6}>/g" > ${6}-${7}.${7}.2${6}
	
	## join source and target
	cat ${6}-${7}.${6}.2${7} ${6}-${7}.${7}.2${6} >> ${6}-${7}.src
	cat ${6}-${7}.${7} ${6}-${7}.${6} | sed "s/|/\& 124 ;/g" >> ${6}-${7}.tgt
	
	cat ${6}-${7}.src >> ../../${sim}.top${1}.src
	cat ${6}-${7}.tgt >> ../../${sim}.top${1}.tgt
	
	cd ..
done
