# Core-Gene-AMR-Models

This repo contains all the necessary scripts to build alignment-based models for *Klebsiella*, *Mycobacterium*, *Salmonella*, and *Staphylococcus*.  The repo itself contains external github repos as a submodules which need to be initiated and updated after this github repo is cloned.  So the initialization of this repo can be done as follows.

```bash
git clone https://github.com/jimdavis1/Core-Gene-AMR-Models
git submodule init
git submodule update
```

Doing this will initialize the [GenomicModelCreator](https://github.com/Tinyman392/GenomicModelCreator/tree/ccd38f2a27feede0d7747ca8c2f69921ef1ef0a7) and [Subtree-Analysis](https://github.com/jimdavis1/Subtree-Analysis) submodules:
- The GenomicModelCreator is used to train models and run model statistics/metrics using genomic data and metadata.  For the purposes of this repo, it's used to train models using alignments of 100 conserved genes for various species in a susceptible vs resistant format.  However, the GenomicModelCreator can do more than just that.  The GenomicModelCreator is still being updated and not all features are currently functional, although the functions specific to this repo are usable.   
- The Subtree-Analysis is used to create and view trees that are based off of 100 core gene alignments.  It utilizes various libaries from the [PATRIC command line interface](https://github.com/PATRIC3/PATRIC-distribution/releases).  

## Repository Layout

There are a few directories within this github repo:
- Automate: Contains the script to automate the model training on alignments for *Klebsiella*, *Mycobacterium*, *Salmonella*, and *Staphylococcus*.  
- GenomicModelCreator: Submodule that is used to train the models.  Please read its README for more information.
- Subtree-Analysis: Submodule that is used to build trees based on conserved gene alignments.  Please read its README for more information.  
- Scripts: Contains scripts specific for creating one-hot alignments *makeAlignments.py*.  The *makeMatrix.py* script can be used to make a matrix, however, the GenomicModelCreator does this on its own as a first step, so this script is deprecated.  
- *Species* Directories: These directories contain the raw alignments and susceptible/resistant calls.  

## Automate

Contains one script that can be used to automate the training of models, *automate.sh*.  There is a README.md in this directory as well to outline its use.  In summary:

```bash
bash /pathtoautomate/automate.sh [output_dir] <threads>
```

There are some memory requirements to run these models as well.

|Model           |Memory|
|----------------|------|
|*Klebsiella*    |64 GB |
|*Mycobacterium* |128 GB|
|*Salmonella*    |128 GB|
|*Staphylococcus*|64 GB |

In the event you run into an *out of memory* error of any sort, it's likely that the machine being used lacks the RAM to run the model.  

Also note that the training script uses the */dev/shm/* directory to store KMC runs.  This directory should be initialize and writable or the script may fail to run!  

## Scripts

This directory contains the scripts required to process the raw alignments.  The main script to be used here is the *makeAlignments.py* script.  Note that the *makeMatrix.py* script is deprecated now since the *GenomicModelCreator* has this process built in.  

### makeAlignments.py

This script is used to concatenate the alignments for each gene over each individual genome and one-hot encode them.  The script will also remove all redundant columns (columns with no variance or are all the same value) in the alignment.  The script takes 3-4 arguments:
1. Alignment fasta directory: the alignment directory of raw fasta files used to build one-hot alignments for (ex *Staphylococcus/Stf.raw.alis/*).
2. Alignment out: the output file containing one one-hot-encoded alignment per genome.
3. Alignment index out: Order list containing the order of the features in the feature array.  It contains PLF and alignment index value for the given PLF.  
4. File suffix: (*optional*) suffix of the files in the *Alignment fasta directory*.

