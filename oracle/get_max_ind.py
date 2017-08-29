import sys

with open(sys.argv[2], 'w'):
  pass

k = 1000
with open(sys.argv[1], 'r') as source:
  lines = source.readlines()
print(len(lines))
for i in range(int(len(lines)/k)):
  max_ind = 0
  max_bleu = float(lines[i*k].strip())
  for j in range(1, k-25):
    bleu = float(lines[i*k+j].strip())
    if bleu > max_bleu:
      #print(max_bleu, bleu)
      max_bleu = bleu
      max_ind = j
      #print(max_ind)
  with open(sys.argv[2], 'a+') as target:
    target.write(str(max_ind)+'\n')

