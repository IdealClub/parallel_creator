#!/bin/bash

## n-best translations file
nbest=$1
## reference translations file
ref=$2

## sentence-level bleu scoring
/raid/bin/moses/mert/sentence-bleu-nbest $ref < $nbest > ${nbest}.sentence-bleu-nbest
## get indices with best BLEU
python get_max_ind.py ${nbest}.sentence-bleu-nbest 1000 ${nbest}.best-ind
## get sentences based on index
python get_final_sents.py ${nbest} ${nbest}.best-ind ${nbest}.best-snts
## filter entences
cat ${nbest}.best-snts | sed "s/||| /|/g" | cut -f2 -d'|' > ${nbest}.best-snts.clean
rm -f ${nbest}.best-snts ${nbest}.best-ind ${nbest}.sentence-bleu-nbest

## eval
/raid/bin/moses/scripts/generic/multi-bleu.perl $ref < ${nbest}.best-snts.clean >> ${nbest}.oracle


