import sys

with open(sys.argv[1], 'r') as source:
	lines_a = source.readlines()
with open(sys.argv[1], 'r') as source:
        lines_b = source.readlines()
with open(sys.argv[3], 'w'):
	pass

for line_a, line_b in zip(lines_a, lines_b):
	try:
		a = (float(line_a.strip()) + float(line_b.strip()))/2
	except:
		a = 0.
	with open(sys.argv[3], 'a+') as target:	
		target.write(str(a)+ ' \n')



