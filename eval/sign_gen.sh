!/bin/bash

model1=$1
model2=$2

scriptdir=/raid/bin/moses/scripts/analysis/
resdir=$3
rm -f results.gen.sign

refdir=tests.proc
echo "newstest" >> results.gen.sign
## newstest
for refl in de en es fr; do
	for sourcel in de en es fr; do
		if [ "$refl" != "$sourcel" ]; then
			trad1="${resdir}/newstest2013.${model1}.tc.${sourcel}.bpe.2${refl}.clean"
			trad2="${resdir}/newstest2013.${model2}.tc.${sourcel}.bpe.2${refl}.clean"
			ref="${refdir}/newstest2013.tc.${refl}"
			${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
			echo "${sourcel}->${refl}" >> results.gen.sign
			grep "is: " proba.sign | head -n 1 >> results.gen.sign
			
		fi
	done
done

refdir=tests.proc
echo "" >> results.gen.sign
echo "EMEA" >> results.gen.sign
## EMEA
for lp in de-en de-es en-es en-fr; do
	for subset in dev test; do
		l1=`echo $lp | cut -f1 -d'-'`
		l2=`echo $lp | cut -f2 -d'-'`
		
		trad1="${resdir}/EMEA.${lp}.${model1}.tc.${subset}.${l2}.bpe.2${l1}.clean"
		trad2="${resdir}/EMEA.${lp}.${model2}.tc.${subset}.${l2}.bpe.2${l1}.clean"
		ref="${refdir}/EMEA.${lp}.tc.${subset}.${l1}"
		${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
		echo "${l1}->${l2}" >> results.gen.sign
		grep "is: " proba.sign | head -n 1 >> results.gen.sign
   
		trad1="${resdir}/EMEA.${lp}.${model1}.tc.${subset}.${l1}.bpe.2${l2}.clean"
		trad2="${resdir}/EMEA.${lp}.${model2}.tc.${subset}.${l1}.bpe.2${l2}.clean"
		ref="${refdir}/EMEA.${lp}.tc.${subset}.${l2}"
		${scriptdir}/bootstrap-hypothesis-difference-significance.pl $trad1 $trad2 $ref > proba.sign
   
		echo "${l2}->${l1}" >> results.gen.sign
		grep "is: " proba.sign | head -n 1 >> results.gen.sign
		echo "" >> results.gen.sign  
		
	done
done
