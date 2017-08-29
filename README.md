# Parallel Sentence Extraction from Comparable Corpora

## Create pseudo sentence pairs from comparable Wikipedia articles `candidates/`

1. Extract parallel articles and their sentence counts for the union: `python extract_union.py <mathced IDs file> <path to article directories>`

2. Preprocess extracted articles (normalisation, tokenisation, truecasing)

3. Create union of health and psychology article list discarding those that appear in both domains and that already had been extracted from the union: 
`./filter_union.sh <health> <union> <out>` followed by `./filter_union.sh <psychology> <health> <out>` and  `./filter_union.sh <out> <union> <final out>` for all language pairs

4. repeat steps 1-3 for healt-union filtered intersection (use `intersection_parallel_creator` for step 1)

## Split corpora and context vectors for parallelization `split/`

1. `split_extraction.py <corpus src> <corpus tgt> <cvx src> <cvx tgt> <article snt nos> <no. of splits>`

## Compute similarity features `feas/`

1. Get context vector similarities `python context_similarities.py <cvx src> <cvx tgt> <output>`

2. Get complementary features `similarities_memeff.py <corpus src> <corpus tgt> <length factors> <lang src> <lang tgt>`

## Train models `training/`

1. Train regression model `python train_regression_all_cont.py <cvx similarities> <label scores> <complementary features>`

