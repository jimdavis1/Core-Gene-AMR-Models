# Core-Gene-AMR-Models

This GitHub repo is designed to aid in the reproducability of the following paper:
*Predicting Antimicrobial Resistance Using Conserved Genes*, by: Marcus Nguyen, Robert Olson, Maulik Shukla, Margo VanOeffelen, and James J. Davis.

This repo  contains the data that were used to build the alignments of 100 concatenated conserved genes, and the matrix files that were derived from them. K-mer-based data are not provided due to size limitations. 

This directory contains four subdirectories, one for each species that was studied, and a directory with python scripts for generating the matrix file.

Within each species directory there are the following files and sub directories:

- `Species.raw.alis` : This directory contains the raw nucleotide alignments in fasta format for the 100 local protein families (PLFs) for each given species.   
- `Species.ali.100.0.one-hot.gz` :  This file is a compressed one-hot encoded alignment, which is a concatenation of all 100 alginments from Species.raw.alis/.  Columns with 100% conservation have been removed.
- `Species.ali.100.0.map`:  This file contains the mapping of informative alignment positions from each protein family that was used in the one-hot encoded alginment. 
- `Species.sir.filt.plf.tab`:  This is a 3-column file containing the genome ID, antibiotic:methodology, and a label (1=S,2=I,4=R).
- `Species.100.0.mat.tar.gz`:  A compressed version of the original matrix file.


**Scripts**
- `makeAlignments.py` : This script is used to one hot encode raw alignments and remove redundant columns (columns with 0 variance).  It reads through the raw alignment directory.
- `makeMatrix.py` :  This script builds the matrix

#### makeAlignments.py

This script is used to concatenate the alignments for each gene over each individual genome and one-hot encode them.  The script will also remove all redundant columns (columns with no variance or are all the same value) in the alignment.  The script takes 3-4 arguments:
1. Alignment fasta directory: the alignment directory of raw fasta files used to build one-hot alignments for (per genome).
2. Alignment out: the output file containing the one-hot alignment per genome.
3. Alignment index out: Order list containing the order of the features in the feature array.  It contains PLF and alignment index value for the given PLF.  
4. File suffix: (*optional*) suffix of the files in the *Alignment fasta directory*.

#### makeMatrix.py

This script takes 4-5 inputs:
1. AMR Metadata tabular file: AMR metadata tabular file.  
2. One-hot alignment file: Files created by *../Alignments/makeAlignments.py* script.
3. Output matrix file: File name to output the matrix to.
4. Output feature order file: File name to output the feature order to.  The last features are the antibiotics.  
5. Folds: (optional, default=10) specify the number of folds to create.  The script makes sure that antibiotic-label combinations are almost equal in every fold created.  

The output matrix is composed of rows of numbers.  The first number is the label (0=S,1=I,2=R) while every subsequent number is a binary encoding of the one-hot matrix.  

A quick way to read them in would be:

```python
f = open(FILE_NAME)
y = [] #labels
X = [] #matrix
for i in f:
	i = list(i.strip('\n'))
	i = [int(x) for x in i]
	y.append(i[0])
	X.append(np.asarray(i[1:]))
f.close()
y = np.asarray(y)
X = np.asarray(X)
```

The script shuffles the input metadata order and creates balanced folds, it's not recommended to reorder or reshuffle the matrix.  You can simply cut off the first 1/N samples for the test, second for the validation, and use the rest to train (or do a similar N-fold cross validation).  N is the number of specified folds (default = 10).

```python
NFOLDS = 10
testY = y[0:len(y)/NFOLDS]
valY = y[len(y)/NFOLDS:len(y)/NFOLDS*2]
trainY = y[len(y)/NFOLDS*2:]
testX = X[0:len(X)/NFOLDS]
valX = X[len(X)/NFOLDS:len(X)/NFOLDS*2]
trainX = X[len(X)/NFOLDS*2:]
```
