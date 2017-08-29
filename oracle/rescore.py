import sys
import math

with open(sys.argv[1], 'r') as source:
	lines_a = source.readlines()
with open(sys.argv[2], 'r') as source:
        lines_b = source.readlines()
with open(sys.argv[3], 'w'):
	pass

for line_a, line_b in zip(lines_a, lines_b):
	score = math.log(float(line_b.strip()), 2) - math.log(float(line_a.strip()), 2)	
	with open(sys.argv[3], 'a+') as target:
		target.write(str(score)+'\n')
