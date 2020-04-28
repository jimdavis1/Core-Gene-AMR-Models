'''
python makeAlignments.py [alignment fasta dir] [alignment out] [index out] <file suffix>

Given a directory of raw nucl alignments by PLFam in fasta format, 
outputs a one-hot encoded alingment with indices for the order of 
the final feature set

The suffix is the suffix of the alignment file type, defaults to
fasta.
'''

from sys import argv,stderr
import glob
import os
import numpy as np

# initialize the suffix and set it
SUFFIX = '.fa'
if len(argv) > 4:
	SUFFIX = argv[4]
# initialize the one-hot size
# 6 binary digits per nucl
ONEHOT_SZ = 6

# short cut to stderr.write()
def err(s):
	stderr.write(s)

# parse a fasta file and reads sequences into a hash
# mapping genome ID (entry/seq name) to sequence
def parseFasta(fName, aliHsh):
	f = open(fName)

	hsh = {}

	aliLen = 0

	currGene = ''
	currSeq = ''
	for i in f:
		i = i.strip()
		if i[0] == '>':
			if currGene != '' and currSeq != '':
				if currGene not in aliHsh:
					aliHsh[currGene] = ''
				aliHsh[currGene] += currSeq
				aliLen = len(currSeq)
			
			i = i.split('>')[1].split(' ')[0]
			currGene = i
			currSeq = ''
			continue
		currSeq += i

	f.close()

	if currGene != '' and currSeq != '':
		if currGene not in aliHsh:
			aliHsh[currGene] = ''
		aliHsh[currGene] += currSeq

	return aliLen

# gets alignments for all alignments in directory
# returns a hash mapping genome ID to one-hot alignment
# and an index array of feature order
def getAlignments():
	fList = glob.glob(argv[1] + '*' + SUFFIX)

	aliHsh = {}
	indArr = []
	count = 0
	inc = len(fList) / 50
	err('reading fasta...\n\t')
	for i in fList:
		if count >= inc:
			err('=')
			count = 0
		count += 1

		base = os.path.basename(i)
		plf = base.split('.')[0]

		l = parseFasta(i, aliHsh)

		for j in range(0,l):
			indArr.append([plf, j])

	err('\n')

	return aliHsh, indArr

# removes all redudant columns in alignment
# redudant column = column with all same base
def removeRedudancies(hsh):
	alis = []
	err("Making matrix and transposing...\n\t")
	count = 0
	inc = len(hsh) / 50
	for i in hsh:
		if count >= inc:
			err('=')
			count = 0
		count += 1

		hsh[i] = list(hsh[i])
		alis.append(hsh[i])
	alis = np.transpose(alis)
	err('\n')

	badInd = []
	count = 0
	inc = len(alis) / 50
	err("Getting redudant alignments...\n\t")
	for i in range(0,len(alis)):
		if count >= inc:
			err('=')
			count = 0
		count += 1

		aliCount = {}
		for j in alis[i]:
			if j not in aliCount:
				aliCount[j] = 0
			aliCount[j] += 1

		if len(aliCount) == 1:
			badInd.append(i)
	err('\n')

	badInd = badInd[::-1]

	count = 0
	inc = len(hsh) / 50
	err("Removing redudant alignments...\n\t")
	for i in hsh:
		if count >= inc:
			err('=')
			count = 0
		count += 1

		for j in badInd:
			del hsh[i][j]
	err("\n")

	return badInd

# removes filtered indices from index array
def removeBadIndInArr(indArr, badInd):
	for i in badInd:
		del indArr[i]

# prints the alignment hash to file
def printHsh(aliHsh):
	nHsh = {
		'a':'100000',
		'c':'010000',
		'g':'001000',
		't':'000100',
		'n':'000010',
		'-':'000001'
	}

	fout = open(argv[2], 'w')

	err("Printing alignments...\n\t")
	count = 0
	inc = len(aliHsh) / 50
	for i in aliHsh:
		if count >= inc:
			err('=')
			count = 0
		count += 1

		aliStr = ''.join(aliHsh[i]).lower()
		ali = ''
		for j in aliStr:
			ali += nHsh[j]

		fout.write('\t'.join([i, ali]) + '\n')
	err('\n')

	fout.close()

# prints feature map array to file.
def printIndArr(indArr):
	fout = open(argv[3], 'w')

	err("Printing index order...\n\t")
	count = 0
	inc = len(indArr) / 50
	for i in indArr:
		if count >= inc:
			count = 0
			err('=')
		count += 1

		for j in range(0, len(i)):
			i[j] = str(i[j])
		fout.write('\t'.join(i) + '\n')
	err('\n')

	fout.close()

if argv[1][-1] != '/':
	argv[1] += '/'

# read and convert the alignment
aliHsh, indArr = getAlignments()
# remove the redudant columns from alignment
badInd = removeRedudancies(aliHsh)
# remove redudant columns for feature order
removeBadIndInArr(indArr, badInd)
# print files
printHsh(aliHsh)
printIndArr(indArr)
