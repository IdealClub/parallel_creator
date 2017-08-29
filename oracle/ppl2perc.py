import sys

with open(sys.argv[1], 'r') as source:
	lines = source.readlines()
with open(sys.argv[2], 'w'):
	pass

ppls = []
for line in lines[:-1]:
	ppls.append(float(line.strip()))

diff = max(ppls) - min(ppls)

for ppl in ppls:
	perc = 1 - (ppl / diff)
	with open(sys.argv[2], 'a+') as target:
		target.write(str(perc) + ' \n')

