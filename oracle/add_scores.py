import sys

with open(sys.argv[1], 'r') as source:
	linesa = source.readlines()
with open(sys.argv[2], 'r') as source:
        linesb = source.readlines()
with open(sys.argv[3], 'w'):
        pass

for linea, lineb in zip(linesa, linesb):
	with open(sys.argv[3], 'a+') as target:
		target.write(str(float(linea.strip())+float(lineb.strip()))+' \n')
