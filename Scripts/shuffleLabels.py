'''
python shuffleLabels.py [tabular]
'''

from sys import argv
from random import shuffle

f = open(argv[1])

rawTab = []
rawLab = []
for i in f:
	i = i.strip().split('\t')
	rawTab.append(i[:2])
	rawLab.append(i[2])

f.close()

shuffle(rawLab)

for i in range(0,len(rawTab)):
	arr = rawTab[i] + [rawLab[i]]
	print '\t'.join(arr)
