#!/bin/bash

model1=$1
model2=$2

scriptdir=/raid/bin/moses/scripts/analysis/

rm -f results.indom.sign

lp=en-es
l1=en
l2=es

resdir=trads_final
trad1="${resdir}/pubPsych.abstracts.${model1}.${lp}.tc.test.${l1}.bpe.2${l2}.clean"
trad2="${resdir}/pubPsych.abstracts.${model2}.tc.${l1}2${l2}.clean"
ref="test/pubPsych.abstracts.test.en-es.tc.es.2en.clean"
${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
echo "pp abs test" >> results.indom.sign
echo "------" >> results.indom.sign
echo "en->es" >> results.indom.sign
grep "is: " proba.sign | head -n 1 >> results.indom.sign
echo "" >> results.indom.sign

refdir=pp_abs.proc
for lp in en-de en-fr; do
   l1=`echo $lp | cut -f1 -d'-'`
   l2=`echo $lp | cut -f2 -d'-'`
   
   trad1="${resdir}/pubPsych.abstracts.${model1}.${lp}.tc.test.${l1}.bpe.2${l2}.clean"
   trad2="${resdir}/pubPsych.abstracts.${model2}.${lp}.tc.test.${l1}.bpe.2${l2}.clean"
   ref="${refdir}/${lp}.tc.${l2}"
   ${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
   echo "${l1}->${l2}" >> results.indom.sign
   grep "is: " proba.sign | head -n 1 >> results.indom.sign
   
   trad1="${resdir}/pubPsych.abstracts.${model1}.${lp}.tc.test.${l2}.bpe.2${l1}.clean"
   trad2="${resdir}/pubPsych.abstracts.${model2}.${lp}.tc.test.${l2}.bpe.2${l1}.clean"
   ref="${refdir}/${lp}.tc.${l1}"
   ${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
   echo "${l2}->${l1}" >> results.indom.sign
   grep "is: " proba.sign | head -n 1 >> results.indom.sign
   echo "" >> results.indom.sign  
done

echo "pp title" >> results.indom.sign
refdir=pp_title.proc
for lp in en-de en-es en-fr; do
	l1=`echo $lp | cut -f1 -d'-'`
    l2=`echo $lp | cut -f2 -d'-'`
    
	trad1="${resdir}/pubPsych.titles.${model1}.${lp}.tc.test.${l1}.bpe.2${l2}.clean"
    trad2="${resdir}/pubPsych.titles.${model2}.${lp}.tc.test.${l1}.bpe.2${l2}.clean"
   ref="${refdir}/${lp}.tc.${l2}"
   ${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
   echo "${l1}->${l2}" >> results.indom.sign
   grep "is: " proba.sign | head -n 1 >> results.indom.sign
   
   trad1="${resdir}/pubPsych.titles.${model1}.${lp}.tc.test.${l2}.bpe.2${l1}.clean"
   trad2="${resdir}/pubPsych.titles.${model2}.${lp}.tc.test.${l2}.bpe.2${l1}.clean"
   ref="${refdir}/${lp}.tc.${l1}"
   ${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
   echo "${l2}->${l1}" >> results.indom.sign
   grep "is: " proba.sign | head -n 1 >> results.indom.sign
   echo "" >> results.indom.sign  
	
done

## pp dev
echo "pp abs dev" >> results.indom.sign
refdir=tests.proc
for lp in en-de en-es; do
	l1=`echo $lp | cut -f1 -d'-'`
	l2=`echo $lp | cut -f2 -d'-'`
	
	trad1="${resdir}/pubPsych.abstracts.dev.${model1}.tc.${l1}2${l2}.clean"
    trad2="${resdir}/pubPsych.abstracts.dev.${model2}.tc.${l1}2${l2}.clean"
   ref="${refdir}/pubPsych.abstracts.dev.${lp}.tc.${l2}"
   ${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
   echo "${l1}->${l2}" >> results.indom.sign
   grep "is: " proba.sign | head -n 1 >> results.indom.sign
   
   trad1="${resdir}/pubPsych.abstracts.dev.${model1}.tc.${l2}2${l1}.clean"
    trad2="${resdir}/pubPsych.abstracts.dev.${model2}.tc.${l2}2${l1}.clean"
   ref="${refdir}/pubPsych.abstracts.dev.${lp}.tc.${l1}"
   ${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
   echo "${l2}->${l1}" >> results.indom.sign
   grep "is: " proba.sign | head -n 1 >> results.indom.sign
   echo "" >> results.indom.sign  
	
done
