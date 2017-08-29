import sys

with open(sys.argv[1], 'r') as source:
	lines = source.readlines()
with open(sys.argv[1]+'.text', 'w'):
	pass
for line in lines:
	with open(sys.argv[1]+'.text', 'a+') as target:
		target.write(line.split('|||')[1].strip()+'\n')
