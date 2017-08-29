# Parallel Sentence Extraction from Comparable Corpora

## Create pseudo sentence pairs from comparable Wikipedia articles `candidates/`

1. Extract parallel articles and their sentence counts for the union: `python extract_union.py <mathced IDs file> <path to article directories>`

2. Preprocess extracted articles (normalisation, tokenisation, truecasing)

3. Create union of health and psychology article list discarding those that appear in both domains and that already had been extracted from the union: 
`./filter_union.sh <health> <union> <out>` followed by `./filter_union.sh <psychology> <health> <out>` and  `./filter_union.sh <out> <union> <final out>` for all language pairs

4. repeat steps 1-3 for healt-union filtered intersection (use `intersection_parallel_creator` for step 1)

## Split corpora and context vectors for parallelization `split/`

1. `split_extraction.py <corpus src> <corpus tgt> <cvx src> <cvx tgt> <article snt nos> <no. of splits>`

## Compute similarity features for training sets `feas/`

1. Get context vector similarities `python context_similarities.py <cvx src> <cvx tgt> <output>`

2. Get complementary features `similarities_memeff.py <corpus src> <corpus tgt> <length factors> <lang src> <lang tgt>`

## Train models `training/`

1. Train regression model `python train_regression_all_cont.py <cvx similarities> <label scores> <complementary features>`

## Compute features and extract from comparable articles `extract/`

1. Extract sentence pair IDs using a trained model. 
`python feature_extract_regression.py <corpus src> <corpus tgt> <cvx src> <cvx tgt> <article snt nos> <save_feas (True/False)> <classifier (sv/gb/ens)> <feas ("all"/"set"/"ctx")>`

2. Get sentences corresponding to IDs `python in_domain_extraction.py <corpus src> <corpus tgt> <article snt nos> <matching IDs>` 

## Rerank extracted candidates `rerank/`

1. `python sim_ranker_feas.py <feas>`

## Create adaptation sets `adapt/`

1. `./create_adapt_sets.sh <N> <no. splits> <corpus src> <corpus tgt> <article snt nos> <lang src> <lang tgt>`

## Evaluate after adaptation `eval/`

1. Translate `./run_indomain <model> <device (cpu/gpuX)>` (use `run_general.sh` for non-indomain test sets)

2. Evaluate `./run_test_all.sh <model> <path to Moses eval script> <dir of translations> <output dir of BLEU scores>`

3. Check significance `./significant.sh <model1> <model2>` (use `sign_gen.sh` for non-indomain test sets)

## Finding best translations `oracle/`

1. N-best translations `./nbest.sh <model> <lang src> <lang tgt> <language pair>`

2. Find theoretical best `./oracle.sh <n-best translations> <reference file>`

3. Do reranking & eval `./find_best.sh> <in-domain LM> <n-best translations> <reference file> <general LM> <source>`


