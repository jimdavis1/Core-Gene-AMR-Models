# Core-Gene-AMR-Models

This GitHub repo is designed to aid in the reproducability of the following paper:
*Predicting Antimicrobial Resistance Using Conserved Genes*, by: Marcus Nguyen, Robert Olson, Maulik Shukla, Margo VanOeffelen, and James J. Davis.

This readme describes the models that were built from alignments of 100 concatenated conserved genes.  K-mer based models and their underlying data are not provided due to size limitations. 

This directory contains four subdirectories, one for each species that was studied, and a directory with python scripts. 

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
1. Alignment fasta directory: the \[Spc\]\_raw\_ali directory used to build one-hot alignments for (per genome).
2. Alignment out: the output file containing the one-hot alignment per genome.
3. Alignment index out: Order list containing the order of the features in the feature array.  It contains PLF and alignment index value for the given PLF.  
4. File suffix: (*optional*) suffix of the files in the *Alignment fasta directory*.

#### FilterAlignments.py

This script is used to filter the alignments based on the minimum occurrence for each individual SNP in a column.  The script takes a number, call it *n*, to filter with.  If a column contains a SNP that occurs less than *n* times, that column is filtered out of the alignment.  This script takes 5 arguments:
1. Alignment in: input one-hot-encoded alignment file created from *makeAlignment.py* or *FilterAlignments.py*.
2. Alignment map order in: the ordering of the SNPs provided as output from *makeAlignment.py* or *FilterAlignments.py*.
3. Filter count: the minimum number of times a SNP can occur for a column to be included in the output one-hot-encoded alignment.
4. Alignment out: output one-hot-encoded alignment file.
5. Alignment map out: Ordering of columns in the one-hot-encoded alignment output.

Note that if you use a filter count that is > 1/2 of the genomes in your dataset, you'll get 0 columns as output as everything will be filtered out.

#### \[Spc\]

These directories contain the filtered alignments and ordering files in the following format: 
```
[Spc].ali.100.0.X
[Spc].ali.100.0.X.map
```

The first file is the one-hot-encoded alignment file that maps a genome to it's encoded alignment.  It's a 2-column tabular file.  *X* is the *filter count* used in the *FilterAlignment.py* script.  The *\*.map* file contains the ordering of columns in the output one-hot-encoded alignment file.  




### Alignments

This directory contains files and directories related to building and encoding alignments.  It contains the following:
- \[Spc\]\_raw\_ali : This directory contains the raw alignments for the 100 local protein families (PLFs) for each given species.  There are 4 species in all: Kleb, Mtb, Sal, and Stf.  
- makeAlignments.py : This script is used to one hot encode raw alignments and remove redundant columns (columns with 0 variance)
- FilterAlignments.py : This script is used to filter out alignments by removing columns that contain low-occurrence SNPs.  
- readme.md : This file
- \[Spc\] : These directories contain the one-hot encoded alignments.

We'll go into further detail regarding each of the files/directories contained in this directory.  

#### \[Spc\]\_raw\_ali

These directories contain 100 files representing each individual PLF that were aligned among genomes who contained all 100 genes with length around the average for the given species.  These directories are used as inputs for the *makeAlignments.py* script provided in this directory.  

#### makeAlignments.py

This script is used to concatenate the alignments for each gene over each individual genome and one-hot encode them.  The script will also remove all redundant columns (columns with no variance or are all the same value) in the alignment.  The script takes 3-4 arguments:
1. Alignment fasta directory: the \[Spc\]\_raw\_ali directory used to build one-hot alignments for (per genome).
2. Alignment out: the output file containing the one-hot alignment per genome.
3. Alignment index out: Order list containing the order of the features in the feature array.  It contains PLF and alignment index value for the given PLF.  
4. File suffix: (*optional*) suffix of the files in the *Alignment fasta directory*.

#### FilterAlignments.py

This script is used to filter the alignments based on the minimum occurrence for each individual SNP in a column.  The script takes a number, call it *n*, to filter with.  If a column contains a SNP that occurs less than *n* times, that column is filtered out of the alignment.  This script takes 5 arguments:
1. Alignment in: input one-hot-encoded alignment file created from *makeAlignment.py* or *FilterAlignments.py*.
2. Alignment map order in: the ordering of the SNPs provided as output from *makeAlignment.py* or *FilterAlignments.py*.
3. Filter count: the minimum number of times a SNP can occur for a column to be included in the output one-hot-encoded alignment.
4. Alignment out: output one-hot-encoded alignment file.
5. Alignment map out: Ordering of columns in the one-hot-encoded alignment output.

Note that if you use a filter count that is > 1/2 of the genomes in your dataset, you'll get 0 columns as output as everything will be filtered out.

#### \[Spc\]

These directories contain the filtered alignments and ordering files in the following format: 
```
[Spc].ali.100.0.X
[Spc].ali.100.0.X.map
```

The first file is the one-hot-encoded alignment file that maps a genome to it's encoded alignment.  It's a 2-column tabular file.  *X* is the *filter count* used in the *FilterAlignment.py* script.  The *\*.map* file contains the ordering of columns in the output one-hot-encoded alignment file.  










#### Alignment Matrices for Training

This directory contains all the scripts and data required to build matrices for training.  During the actual training process, this step is actually baked into the training script and the matrix deleted after training, so a separate script has been generated to make matrices for you to generate the matrix and build your own models.  

Once again, there are a few things in this directory:
- \[Spc\] directories: matrices and AMR metadata tabular files are stored in these directories.  The AMR metadata is stored in a 3-column file containing genome ID, antibiotic:methodology, and a label (1=S,2=I,4=R).  The metadata files are named *\[Spc\].sir.filt.plf.tab*.  
- makeMatrix.py: converts the AMR metadata file and alignments file created by *../Alignments/FilterAlignments.py* or *../Alignments/makeAlignments.py* into a matrix that is able to be trained on.

#### \[Spc\] Directories
These contain the AMR metadata tabular file (*\[Spc\].sir.filt.tab*) as well as the matrices and feature order fields for each of the alignments that exist in the (*../Alignments/\*/* folder).  

#### makeMatrix.py

This script takes 4-5 inputs:
1. AMR Metadata tabular file: AMR metadata tabular file that is in each \[Spc\] directory.  
2. One-hot alignment file: Files created by either the *../Alignments/FilterAlignments.py* or *../Alignments/makeAlignments.py* scripts.  The output is located in the *../\[Spc\]/* directory (non-map files).
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
