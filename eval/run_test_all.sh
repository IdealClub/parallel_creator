#!/bin/bash
model=$1
mosespath=$2
resdir=$3
bleudir=$4
mkdir -p $bleudir

## clean up
for f in ${resdir}/*; do
	sed 's/@@ //g' $f > ${f}.clean
done

for f in tests.proc/*.bpe.*; do
	cleanfile=`echo $f | rev | cut -f3- -d'.' | rev`
	sed 's/@@ //g' $f | sed "s/^<abstract> //g" | sed "s/^<title> //g" | sed "s/^<2..> //g"  > $cleanfile
done

## pp abs & title test
refdir=pp_abs.proc
for lp in en-de en-fr; do
	l1=`echo $lp | cut -f1 -d'-'`
    l2=`echo $lp | cut -f2 -d'-'`
    ${mosespath}/multi-bleu.perl ${refdir}/${lp}.tc.${l2} < ${resdir}/pubPsych.abstracts.${model}.${lp}.tc.test.${l1}.bpe.2${l2}.clean > ${bleudir}/pubPsych.abstracts.${model}.${lp}.tc.test.${l1}.bpe.2${l2}.clean.bleu
    ${mosespath}/multi-bleu.perl ${refdir}/${lp}.tc.${l1} < ${resdir}/pubPsych.abstracts.${model}.${lp}.tc.test.${l2}.bpe.2${l1}.clean > ${bleudir}/pubPsych.abstracts.${model}.${lp}.tc.test.${l2}.bpe.2${l1}.clean.bleu
done

refdir=pp_title.proc
for lp in en-de en-es en-fr; do
	l1=`echo $lp | cut -f1 -d'-'`
    l2=`echo $lp | cut -f2 -d'-'`
    ${mosespath}/multi-bleu.perl ${refdir}/${lp}.tc.${l2} < ${resdir}/pubPsych.titles.${model}.${lp}.tc.test.${l1}.bpe.2${l2}.clean > ${bleudir}/pubPsych.titles.${model}.${lp}.tc.test.${l1}.bpe.2${l2}.clean.bleu
    ${mosespath}/multi-bleu.perl ${refdir}/${lp}.tc.${l1} < ${resdir}/pubPsych.titles.${model}.${lp}.tc.test.${l2}.bpe.2${l1}.clean > ${bleudir}/pubPsych.titles.${model}.${lp}.tc.test.${l2}.bpe.2${l1}.clean.bleu
done


## pp dev
refdir=tests.proc	
for lp in en-de en-es; do
	l1=`echo $lp | cut -f1 -d'-'`
	l2=`echo $lp | cut -f2 -d'-'`
	${mosespath}/multi-bleu.perl ${refdir}/pubPsych.abstracts.dev.${lp}.tc.${l2} < ${resdir}/pubPsych.abstracts.dev.${model}.tc.${l1}2${l2}.clean > ${bleudir}/pubPsych.abstracts.dev.${model}.tc.${l1}2${l2}.clean.bleu
    ${mosespath}/multi-bleu.perl ${refdir}/pubPsych.abstracts.dev.${lp}.tc.${l1} < ${resdir}/pubPsych.abstracts.dev.${model}.tc.${l2}2${l1}.clean > ${bleudir}/pubPsych.abstracts.dev.${model}.tc.${l2}2${l1}.clean.bleu

done

## newstest
for refl in de en es fr; do
	for sourcel in de en es fr; do
		if [ "$refl" -ne "$sourcel" ]; then
			${mosespath}/multi-bleu.perl ${refdir}/newstest2013.tc.${refl} < ${resdir}/newstest2013.${model}.tc.${sourcel}.bpe.2${refl}.clean > ${bleudir}/newstest2013.${model}.tc.${sourcel}.bpe.2${refl}.clean.bleu
		fi
	done
done

## EMEA
for lp in de-en de-es en-es en-fr; do
	for subset in dev test; do
		l1=`echo $lp | cut -f1 -d'-'`
		l2=`echo $lp | cut -f2 -d'-'`
		${mosespath}/multi-bleu.perl ${refdir}/EMEA.${lp}.tc.${subset}.${l1} < ${resdir}/pubPsych.abstracts.dev.${model}.tc.${l1}2${l2}.clean > ${bleudir}/pubPsych.abstracts.dev.${model}.tc.${l1}2${l2}.clean.bleu
		${mosespath}/multi-bleu.perl ${refdir}/EMEA.${lp}.tc.${subset}.${l2} < ${resdir}/pubPsych.abstracts.dev.${model}.tc.${l2}2${l1}.clean > ${bleudir}/pubPsych.abstracts.dev.${model}.tc.${l2}2${l1}.clean.bleu

	done
done

