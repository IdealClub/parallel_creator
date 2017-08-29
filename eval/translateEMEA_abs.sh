#!/bin/sh

# inputs
model=$1  #ULL al exe tb
src=$2
tgt=$3
lang=$4

export CUDA_HOME=/usr/local/cuda-7.5/
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:/raid/bin/cudnn-v2/cudnn-6.5-linux-x64-v2:$LD_LIBRARY_PATH
export PATH=$PATH:${CUDA_HOME}/bin

# theano device
device=gpu3

#EMEA.en-es.tc.test.en.bpe.2es
# path to nematus ( https://www.github.com/rsennrich/nematus )
nematus=/home/avarga/sge-data/adapt/nematus
#code=$nematus/wmt16-scripts/sample
#code=$nematus

adapt=/home/avarga/sge-data/adapt/pp_translate
data=$adapt/test
test=$data/pubPsych.abstracts.$lang.tc.test.${src}.bpe.2${tgt}
trad=pubPsych.abstracts.$model.tc.${src}2${tgt}
#trad="${trad/\//_}"


#echo $device $nematus $adapt $model $test $trad

THEANO_FLAGS=mode=FAST_RUN,floatX=float32,device=$device,on_unused_input=warn,nvcc.flags=-D_FORCE_INLINES python $nematus/nematus/translate.py \
     -m $adapt/$model \
     -i $test \
     -o $adapt/trads_wiki_5/$trad \
     -k 6 -n -p 1
