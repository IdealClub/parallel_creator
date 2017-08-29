#!/bin/sh

# inputs
model=$1  #ULL al exe tb
#src=$2
#tgt=$3
#lang=$4

export CUDA_HOME=/usr/local/cuda-7.5/
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64:/raid/bin/cudnn-v2/cudnn-6.5-linux-x64-v2:$LD_LIBRARY_PATH
export PATH=$PATH:${CUDA_HOME}/bin

# theano device
device=cpu

#EMEA.en-es.tc.test.en.bpe.2es
# path to nematus ( https://www.github.com/rsennrich/nematus )
nematus=/home/avarga/sge-data/adapt/nematus
#code=$nematus/wmt16-scripts/sample
#code=$nematus

adapt=/home/avarga/sge-data/adapt/pp_translate
data=$adapt/pp_abs.proc
#test=$data/pubPsych.abstracts.$lang.tc.test.${src}.bpe.2${tgt}.abs
#trad=pubPsych.abstracts.$model.tc.${src}2${tgt}
test=$data/$2
trad=${model}.${2}.trad
#trad="${trad/\//_}"


#echo $device $nematus $adapt $model $test $trad
export OMP_NUM_THREADS=1
THEANO_FLAGS=mode=FAST_RUN,floatX=float32,device=$device,on_unused_input=warn,nvcc.flags=-D_FORCE_INLINES,optimizer=None python $nematus/nematus/translate.py \
     -m $adapt/$model \
     --n-best \
     -i $test \
     -o $adapt/trads_oracle_part/$trad \
     -k 1000 -n -p 5
