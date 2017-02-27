Create pseudo sentence pairs from comparable Wikipedia articles.

1. Extract parallel articles and their sentence counts for the union: `python extract_union.py <mathced IDs file> <path to article directories>`

2. Preprocess extracted articles (normalisation, tokenisation, truecasing)

3. Create pseudo-parallel corpora from paired union: `python multiply_sentences.py <source> <target> <sentence counts>`

4. Create union of health and psychology article list discarding those that appear in both domains and that already had been extracted from the union: 
`./filter_union.sh <health> <union> <out>` followed by `./filter_union.sh <psychology> <health> <out>` and  `./filter_union.sh <out> <union> <final out>` for all language pairs

5. repeat steps 1-3 for healt-union filtered intersection (use `intersection_parallel_creator` for step 1)
