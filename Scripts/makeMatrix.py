'''
python makeMatrix.py [AMR tab] [one-hot alignment] [output matrix] [output feat order] <folds=10>

This script takes an AMR tabular file containing 3 columns: genome 
ID, antibiotic:source, and an AMR label (1=S,2=I,4=R).  The script also takes a one-hot alignment that is 2 columns containing a genome ID and one-hot alignment for that given genome.  

Using these files, it generates a matrix that can be used to train with.  By default script will shuffle the contents of the tabular file and create a single matrix composed of 10 folds (# of folds can be adjusted by passing a 3rd argument) where each fold has approximately an equal number of antibiotic-label combinations.  For example, all folds should have approximately the same number of Amoxicillin susceptible samples.  

Due to the fact that code was originally used for MIC data which follow 2^x format, the output SIR labels are 0=S,1=I,2=R.  
'''

from sys import argv
from math import log
from random import shuffle
import numpy as np

# parses alignment tabular file and returns hash that
# maps genome ID to alignment.
def parseAlignment():
	f = open(argv[2])

	aliHsh = {}
	for i in f:
		i = i.strip('\n').split('\t')
		aliHsh[i[0]] = list(i[1])

	f.close()

	return aliHsh

# splits the tabular file into X folds
# if genome ID does not exist in alignment hash, skips it
def makeFolds(tab, aliHsh):
	NFOLDS = 10
	if len(argv) > 5:
		NFOLDS = int(argv[5])

	tabSpl = []
	for i in range(0,NFOLDS):
		tabSpl.append([])

	shuffle(tab)
	cntHsh = {}
	for i in tab:
		if i[0] not in aliHsh:
			continue

		if i[1] not in cntHsh:
			cntHsh[i[1]] = {}
		if i[2] not in cntHsh[i[1]]:
			cntHsh[i[1]][i[2]] = 0

		ind = cntHsh[i[1]][i[2]] % NFOLDS
		tabSpl[ind].append(i)

		cntHsh[i[1]][i[2]] += 1

	tab = []
	for i in tabSpl:
		tab += i

	return tab

# parses the AMR tabulra file and returns the raw tabular data and
# an antibiotic hash that enumerates the antiotics.
def parseAMRTab(aliHsh):
	f = open(argv[1])

	amrTab = []
	abHsh = {}
	for i in f:
		i = i.strip('\n').split('\t')
		i[-1] = float(i[-1])
		i[-1] = str(round(log(i[-1],2)))

		amrTab.append(i)
		if i[1] not in abHsh:
			abHsh[i[1]] = 0

	f.close()

	cnt = 0
	for i in sorted(abHsh):
		abHsh[i] = cnt
		cnt += 1

	amrTab = makeFolds(amrTab, aliHsh)

	return amrTab, abHsh

def makeMatrix(amrTab, aliHsh, abHsh):
	f = open(argv[3], 'w')

	mat = []
	aliLen = None
	for i in amrTab:
		ali = aliHsh[i[0]]

		if aliLen is None:
			aliLen = len(ali)

		abInd = abHsh[i[1]]
		abArr = ['0']*len(abHsh)
		abArr[abInd] = '1'

		line = ''.join([i[2]] + ali + abArr)
		f.write(line + '\n')

	f.close()

	f = open(argv[4], 'w')

	for i in range(0,len(aliHsh)):
		f.write('ali_col_' + str(i) + '\t' + str(i))

	cnt = 0
	for j in sorted(abHsh, key = lambda x: abHsh[x]):
		f.write('x' + '\t' + str(cnt + aliLen))
		cnt += 1

	f.close()

def main():
	aliHsh = parseAlignment()
	amrTab, abHsh = parseAMRTab(aliHsh)
	makeMatrix(amrTab, aliHsh, abHsh)

if __name__ == '__main__':
	main()