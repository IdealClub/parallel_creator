import sys

with open(sys.argv[1], 'r') as source:
    sents = source.readlines()
with open(sys.argv[2], 'r') as source:
    indices = source.readlines() 
with open(sys.argv[3], 'w'):
    pass

k = 1000
for i, ind in enumerate(indices):
    ind = int(ind.strip())
    sentence = sents[i*k+ind]
    with open(sys.argv[3], 'a+') as target:
        target.write(sentence)
