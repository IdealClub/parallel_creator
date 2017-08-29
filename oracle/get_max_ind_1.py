import sys

with open('best_ind.txt', 'w'):
  pass

with open(sys.argv[1], 'r') as source:
  lines = source.readlines()

for i in range(int(len(lines))):
  max_ind = 0
  max_bleu = float(lines[i*k].strip())
  for j in range(1, k-2
    bleu = float(lines[i*k+j].strip())
    if bleu > max_bleu:
      #print(max_bleu, bleu)
      max_bleu = bleu
      max_ind = j
      #print(max_ind)
  with open('best_ind.txt', 'a+') as target:
    target.write(str(max_ind)+'\n')

