#!/bin/bash
model=$1
device=$2


lp=en-es
l1=`echo $lp | cut -f1 -d'-'`
l2=`echo $lp | cut -f2 -d'-'`

./translateEMEA_test.sh $model $l2 $l1 $lp $device test pubPsych.abstracts.en-es.tc.test.es.bpe.2en.abs pubPsych.abstracts.${model}.en-es.tc.test.es.bpe.2en.abs
./translateEMEA_test.sh $model $l1 $l2 $lp $device test pubPsych.abstracts.en-es.tc.test.en.bpe.2es.abs pubPsych.abstracts.${model}.en-es.tc.test.en.bpe.2es.abs

## pp abs & title test
for lp in en-de en-fr; do
	l1=`echo $lp | cut -f1 -d'-'`
    l2=`echo $lp | cut -f2 -d'-'`
    ./translateEMEA_test.sh $model $l1 $l2 $lp $device pp_abs.proc pubPsych.abstracts.${lp}.tc.test.${l1}.bpe.2${l2}.abs pubPsych.abstracts.${model}.${lp}.tc.test.${l1}.bpe.2${l2} 
    ./translateEMEA_test.sh $model $l2 $l1 $lp $device pp_abs.proc pubPsych.abstracts.${lp}.tc.test.${l2}.bpe.2${l1}.abs pubPsych.abstracts.${model}.${lp}.tc.test.${l2}.bpe.2${l1}
done

for lp in en-de en-es en-fr; do
	l1=`echo $lp | cut -f1 -d'-'`
    l2=`echo $lp | cut -f2 -d'-'`
    ./translateEMEA_test.sh $model $l1 $l2 $lp $device pp_title.proc pubPsych.titles.${lp}.tc.test.${l1}.2${l2}.bpe.tit pubPsych.titles.${model}.${lp}.tc.test.${l1}.bpe.2${l2} 
    ./translateEMEA_test.sh $model $l2 $l1 $lp $device pp_title.proc pubPsych.titles.${lp}.tc.test.${l2}.2${l1}.bpe.tit pubPsych.titles.${model}.${lp}.tc.test.${l2}.bpe.2${l1}
done

## pp dev
for lp in en-de en-es; do
	l1=`echo $lp | cut -f1 -d'-'`
	l2=`echo $lp | cut -f2 -d'-'`
	./translateEMEA_test.sh $model $l1 $l2 $lp $device tests.proc pubPsych.abstracts.dev.${lp}.tc.${l1}.bpe.2${l2} pubPsych.abstracts.dev.${model}.tc.${l1}2${l2}
	./translateEMEA_test.sh $model $l2 $l1 $lp $device tests.proc pubPsych.abstracts.dev.${lp}.tc.${l2}.bpe.2${l1} pubPsych.abstracts.dev.${model}.tc.${l2}2${l1}
done

## newstest
./translateEMEA_test.sh $model de en de-en $device tests.proc newstest2013.tc.de.bpe.2en newstest2013.${model}.tc.de.bpe.2en 
./translateEMEA_test.sh $model de es de-es $device tests.proc newstest2013.tc.de.bpe.2es newstest2013.${model}.tc.de.bpe.2es
./translateEMEA_test.sh $model de fr de-fr $device tests.proc newstest2013.tc.de.bpe.2fr newstest2013.${model}.tc.de.bpe.2fr 
./translateEMEA_test.sh $model en fr en-fr $device tests.proc newstest2013.tc.en.bpe.2fr newstest2013.${model}.tc.en.bpe.2fr 
./translateEMEA_test.sh $model en de en-de $device tests.proc newstest2013.tc.en.bpe.2de newstest2013.${model}.tc.en.bpe.2de
./translateEMEA_test.sh $model en es en-es $device tests.proc newstest2013.tc.en.bpe.2es newstest2013.${model}.tc.en.bpe.2es
./translateEMEA_test.sh $model es de es-de $device tests.proc newstest2013.tc.es.bpe.2de newstest2013.${model}.tc.es.bpe.2de 
./translateEMEA_test.sh $model es en es-en $device tests.proc newstest2013.tc.es.bpe.2en newstest2013.${model}.tc.es.bpe.2en
./translateEMEA_test.sh $model es fr es-fr $device tests.proc newstest2013.tc.es.bpe.2fr newstest2013.${model}.tc.es.bpe.2fr
./translateEMEA_test.sh $model fr de fr-de $device tests.proc newstest2013.tc.fr.bpe.2de newstest2013.${model}.tc.fr.bpe.2de
./translateEMEA_test.sh $model fr de fr-es $device tests.proc newstest2013.tc.fr.bpe.2es newstest2013.${model}.tc.fr.bpe.2es
./translateEMEA_test.sh $model fr en fr-en $device tests.proc newstest2013.tc.fr.bpe.2en newstest2013.${model}.tc.fr.bpe.2en

## EMEA
for lp in de-en de-es en-es en-fr; do
	for subset in dev test; do
		l1=`echo $lp | cut -f1 -d'-'`
		l2=`echo $lp | cut -f2 -d'-'`
		./translateEMEA_test.sh $model $l1 $l2 $lp $device tests.proc EMEA.${lp}.tc.${subset}.${l1}.bpe.2${l2} EMEA.${lp}.${model}.tc.${subset}.${l1}.bpe.2${l2}
		./translateEMEA_test.sh $model $l2 $l1 $lp $device tests.proc EMEA.${lp}.tc.${subset}.${l2}.bpe.2${l1} EMEA.${lp}.${model}.tc.${subset}.${l2}.bpe.2${l1}
	done
done

