## $1 -- indomain LM
## $2 -- n-best translations
lmin=$1
nbest=$2
ref=$3
lmgen=$4
source=$5

cat ${nbest}| sed "s/||| /|/g" | cut -f2 -d'|' > ${nbest}.clean
## indomain PPL
../turin-raid/bin/srilm/lm/bin/i686-m64/ngram -lm $lmin -ppl ${nbest}.clean -debug 1 > ${nbest}.in.ppl
grep "ppl= " ${nbest}.in.ppl | cut -f6 -d' ' > ${nbest}.indom-scores

## general PPL
../turin-raid/bin/srilm/lm/bin/i686-m64/ngram -lm $lmgen -ppl ${nbest}.clean -debug 1 > ${nbest}.gen.ppl
grep "ppl= " ${nbest}.gen.ppl | cut -f6 -d' ' > ${nbest}.gen-scores

## H_in - H_gen
python rescore.py ${nbest}.indom-scores ${nbest}.gen-scores ${nbest}.in-gen

## indomain PPL for source
../turin-raid/bin/srilm/lm/bin/i686-m64/ngram -lm $lmin -ppl $source -debug 1 > ${source}.in.ppl
grep "ppl= " ${source}.in.ppl | cut -f6 -d' ' > ${source}.indom-scores

## general PPL for source
../turin-raid/bin/srilm/lm/bin/i686-m64/ngram -lm $lmgen -ppl $source -debug 1 > ${source}.gen.ppl
grep "ppl= " ${source}.gen.ppl | cut -f6 -d' ' > ${source}.gen-scores

## H_in - H_gen for source
python rescore.py ${source}.indom-scores ${source}.gen-scores ${source}.in-gen

## sim scores
python3 .parallel_creator/rerank.py $source ${nbest}.clean 1000 ${nbest}.sim
cut -f1 -d' ' ${nbest}.sim > ${nbest}.simavlf
cut -f2 -d' ' ${nbest}.sim > ${nbest}.simav

## ppl to percentage and AVG with sim+LF
python ppl2perc.py ${nbest}.indom-scores ${nbest}.perc
python avg_scores.py ${nbest}.perc ${nbest}.simavlf ${nbest}.pplsimlf

## PPL rescore
python get_min_ind.py ${nbest}.indom-scores ${nbest}.ppl.ind
python get_final_sents.py ${nbest}.clean ${nbest}.ppl.ind ${nbest}.ppl.best-snts
../turin-raid/bin/moses/scripts/generic/multi-bleu.perl $ref < ${nbest}.ppl.best-snts > ${nbest}.ppl.bleu

## H_in - H_gen rescore
python get_min_ind.py ${nbest}.in-gen ${nbest}.in-gen.ind
python get_final_sents.py ${nbest}.clean ${nbest}.in-gen.ind ${nbest}.in-gen.best-snts
../turin-raid/bin/moses/scripts/generic/multi-bleu.perl $ref < ${nbest}.in-gen.best-snts > ${nbest}.in-gen.bleu

## H_src + H_tgt rescore
rm ${source}.in-gen.rep
while read line; do for i in {1..1000}; do echo "$line" >> ${source}.in-gen.rep; done; done < ${source}.in-gen 
python add_scores.py ${source}.in-gen.rep ${nbest}.in-gen ${nbest}.srcPtgt
python get_min_ind.py ${nbest}.srcPtgt ${nbest}.srcPtgt.ind
python get_final_sents.py ${nbest}.clean ${nbest}.srcPtgt.ind ${nbest}.srcPtgt.best-snts
../turin-raid/bin/moses/scripts/generic/multi-bleu.perl $ref < ${nbest}.srcPtgt.best-snts > ${nbest}.srcPtgt.bleu

## sim rescore
python get_max_ind.py ${nbest}.simav ${nbest}.simav.ind
python get_final_sents.py ${nbest}.clean ${nbest}.simav.ind ${nbest}.simav.best-snts
../turin-raid/bin/moses/scripts/generic/multi-bleu.perl $ref < ${nbest}.simav.best-snts > ${nbest}.simav.bleu

## sim+LF rescore
python get_max_ind.py ${nbest}.simavlf ${nbest}.simavlf.ind
python get_final_sents.py ${nbest}.clean ${nbest}.simavlf.ind ${nbest}.simavlf.best-snts
../turin-raid/bin/moses/scripts/generic/multi-bleu.perl $ref < ${nbest}.simavlf.best-snts > ${nbest}.simavlf.bleu

## PPL+sim+LF rescore
python get_max_ind.py ${nbest}.pplsimlf ${nbest}.pplsimlf.ind
python get_final_sents.py ${nbest}.clean ${nbest}.pplsimlf.ind ${nbest}.pplsimlf.best-snts
../turin-raid/bin/moses/scripts/generic/multi-bleu.perl $ref < ${nbest}.pplsimlf.best-snts > ${nbest}.pplsimlf.bleu

 



