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

## Downloading Data

The data for this repository is now available through the [PATRIC FTP](ftp://ftp.patricbrc.org/datasets/Nguyen_et_al_2020.tar.gz).  It comes as a tar-ball that is gzipped which can be opened up using the following bash command `tar -xzf PATH/TO/Nguyen_et_al_2020.tar.gz -C [output directory]`.  NOTE THAT `[output directory]` must exist prior to running the command.  If the `-C` option is not used, then it will extract to the working directory.  Once extracted there should be a *Nguyen_et_al_2020* directory inside of the `[output directory]`.  Inside there will be 4 directories for *Klebsiella*, *Mycobacterium*, *Salmonella*, and *Staphylococcus*.  Their directory structures are very similar with the following:
- clades_use : the clades used to generate phylogeny-based models
- fasta.X.Y : *X* represents the number of genes chosen for the gene set, *Y* represents the replicate of sampling (multiple replicates exist for gene sets of 100).  These are the same sets used in the paper.  There will be one fasta file per genome named using the convention genome_id.fasta.
- fasta.low10 : Models were created using the 10 sets of 100 genes and the 10 genes of the lowest importance were then chosen.  These are those genes and corresponding fasta files per genome.  There will be one fasta file per genome named using the convention genome_id.fasta.
- \*.sir.filt.plf.tab : This is the raw AMR metadata for each species.  

Note that the directories containing fasta files may *not* contain the same set of genomes.  This is because genomes which did not contain all *X* genes that were greater than <sup>1</sup>/<sub>2</sub> the average size and less than 2 times the average size of each gene were removed.  

## Automate

Contains one script that can be used to automate the training of models, *automate.sh*.  There is a README.md in this directory as well to outline its use.  In summary:

```bash
bash /PATH/TO/Automate/automate.sh [output_dir] <threads>
```

This script will download the data from the [PATRIC FTP](ftp://ftp.patricbrc.org/datasets/Nguyen_et_al_2020.tar.gz) and store it in the `output_dir`.  It will then go and train and compute model metrics for the following models for Staphylococcus (you substitute in other species by editing *all* of the *for loops*):
- Alignment-based models
- Gene set models
- Randomized models
- Phylogeny models
- Low 10 genes models

If you have already downloaded the data, you can specify the parent directory of the downloaded data directory as the output directory for the *automate.sh* script and comment out lines 46, 47, and 49 to skip the downloading portion of the script.  

In the event you run into an *out of memory* error of any sort, it's likely that the machine being used lacks the RAM to run a certain model.  

Also note that the training script uses the */dev/shm/* directory to store KMC runs.  This directory should be initialize and writable or the script may fail to run!  

## Subtree-Analysis

This submodule is a repository designed to aid the user in creating Phylogentic trees used for the publication related to this repository.  The README.md in the Subtree-Analysis repo will walk the user, step by step, though building various phylogenetic trees to create clades using various tip-distance cutoffs.  It requires the PATRIC command line interface (CLI) installed.  See the README for more info.

## GenomeModelCreator

This submodule is a repository designed as tool to allow users to train machine learning models on genomic and one-hot encoded data.  The *buildModel.py* script is the main driver.  It is designed as an all-in-one solution whose feature set surpasses the scope of the paper this repository is related to.  As such, there will be many more options available with the model-building tool than was used in this paper.  Additionally, some features for this tool are still being implemented, but aren't used in this paper.  The options that will be used for this paper are:
- -f --fasta_dir : Used to specify the location of fasta files to do k-mer based models with.  Each fasta in this directory should be named *[genome_id].fasta*  **Note do not use the -L --alignment option when using the -f --fasta option!**
- -L --alignment : Used to specify the location of an alignment file.  The file should be a 2-column file containing a genome ID and a one-hot-encoded alignment for that genome.  **Note do not use the -f --fasta_dir option when using the -L --alignment option!**
- -t --tabular : Used to specify a tabular file which contains the predicted metadata (last column) as well as the antibiotic that was tested.  Each line should contain 3 columns: genome_id, antibiotic, label (label can be either 1, 2, 4 for S, I, R respectively or a MIC value).  
- -T --temp_dir : Used to specify the temporary directory to store temporary files.  **Note that this will be cleared out by removing all files in the directory at script start, so make sure it is empty.**  It defaults to *temp"
- -o --out_dir : Used to specify the output directory for the model.  **Note that this too will be cleared out by removing all files in the directory at script start, so make sure it is empty.** It defaults to *model*.  
- -n --threads : Used to specify the number of threads to use.  Don't go higher than what is available on your machine.  If on a Linux-based system, `cat /proc/cpuinfo/` will list out the CPUs available to use.  `tail -100 /proc/cpuinfo/` will list out the end of the file to allow you to see how many there are.  These are 0-indexed, so the number of available CPUs is 1 higher than the highest CPU number. 
- -d --depth : Used to specify the maximum tree depth for the model.  Defaults to 4.  **Note this paper varied the depth, but used 16.**
- -k --kmer_size : Used to specify the k-mer size to use.  Defaults to 10.  **Note this paper uses 15.  It should be noted that a k-mer size of 10 produced approximately the same results as a k-mer size of 15.  If you run into memory issues, changing this value to 10, or even 8, may help out a lot.**
- -P --presence_absence: Set this to *True* if the k-mer size is greater than or equal to 12.  This will help reduce the memory footprint by defining k-mer counts as binary (presence vs absence).  The default for this is *False*.  
- -i --individual : Used to specify whether or not to run each antibiotic as an individual model.  The default for this is *False*.
- -e --enumerate_class : **This option is not used in the paper, do NOT set this option to True for AMR models, it was created for non-AMR models!**.  The default value for this option is *False*. 
- -a --folds_to_run : Total folds to run.  Its default is set to 5 which is what was used for this paper.
- -A --total+folds :Total folds to have.  Its default is set to 10 which is what is used for this paper.
- -c --classification : Set this to *True* for SIR models as those are treated as a classification model.  MIC models should have this set to *False*.  The default for this is *False*.  
- -J --noI : Set this to *False* as it will remove the intermediate class from the model which was done for this paper.
- -S --compute_stats : Set this to either *AMRcls* or *AMRreg* for SIR and MIC models, respectively. 
- -M --model_type : Specify the type of model to run if you're not using XGBoost.  *RandomForest* was also used in this paper.  **Note that SciKit-Learn can very memory intensive and will multiply your memory footprint by the number of threads being used (on models that support multi-threading)!**  SVMs do *not* support multithreading and will run very slowly.    
- -w --weighted : Set this to *True* for SIR models and *False* for MIC models, however for clade weighted models, do not specify this and use the -u option instead (listed below).  This weights the samples based on class distribution.  
- -u --cluster_weight : Specify whether to weight each cluster by a cluster weight.  0 = no cluster weight, 1 = weight by size, 2 = weight by SIR cluster dist, 3 = weight by both.  
- -U --cluster_file : Specify the location of a cluster file to use with the cluster weight (-u --cluster_weight) option.  This is a 2-column file containing a genome ID and the cluster number it belongs to.  

A couple example runs are shown below:

```
# 100 gene set model using kmers
PATH/TO/buildModel.py -f Nguyen_et_al_2020/Klebsiella/fasta.100.0 -t Nguyen_et_al_2020/Klebsiella/Kleb.sir.filt.plf.tab -T temp -o model_gset_100_0 -n 24 -d 16 -k 15 -P True -c True -J True -S AMRcls -w True

# 100 gene set alignment model
PATH/TO/buildModel.py -L Nguyen_et_al_2020/Klebsiella/ali.out.tab -t Nguyen_et_al_2020/Klebsiella/Kleb.sir.filt.plf.tab -T temp -o model_gset_100_0 -n 24 -d 16 -k 15 -P True -c True -J True -S AMRcls -w True

# 100 gene set model weighted by cluster SR distribution
PATH/TO/buildModel.py -f Nguyen_et_al_2020/Klebsiella/fasta.100.0 -t Nguyen_et_al_2020/Klebsiella/Kleb.sir.filt.plf.tab -T temp -o model_gset_100_0 -n 24 -d 16 -k 15 -P True -c True -J True -S AMRcls -u 2 -U Nguyen_et_al_2020/Klebsiella/clades_use/247.clades
```

Note that, as stated above, there are other options to the script, but they are not used at all in this paper and some of them are still untested for accuracy or in some cases not yet implemented.  

Also note that the training script uses the */dev/shm/* directory to store KMC runs.  This directory should be initialize and writable or the script may fail to run!  

## Scripts

This directory contains the scripts required to process the raw alignments.  The main scripts to be used here are the *makeAlignments.py* and *shuffleLabels.py* scripts.  Note that the *makeMatrix.py* script is deprecated now since the *GenomicModelCreator* has this process built in.  

### makeAlignments.py

This script is used to concatenate the alignments for each gene over each individual genome and one-hot encode them.  The script will also remove all redundant columns (columns with no variance or are all the same value) in the alignment.  The script takes 3-4 arguments:
1. Alignment fasta directory: the alignment directory of raw fasta files used to build one-hot alignments for (ex *Staphylococcus/Stf.raw.alis/*).
2. Alignment out: the output file containing one one-hot-encoded alignment per genome.
3. Alignment index out: Order list containing the order of the features in the feature array.  It contains PLF and alignment index value for the given PLF.  
4. File suffix: (*optional*) suffix of the files in the *Alignment fasta directory*.

An example run can be seen below:

```bash
python PATH/TO/scripts/makeAlignments.py Nguyen_et_al_2020/Klebsiella/Kleb.raw.alis Nguyen_et_al_2020/Klebsiella/ali.out.tab Nguyen_et_al_2020/Klebsiella/ali.out.ind
```

### shuffleLabels.py

This script is used to shuffle the labels in a tabular file for the *buildModel.py* script in GenomicModelCreator.  It takes one option, the name of a tabular file to shuffle and outputs to stdout.  

An example of this script is shown below.  

```bash
python PATH/TO/scripts/shuffleLabels.py Nguyen_et_al_2020/Klebsiella/Kleb.sir.filt.plf.tab > tabular_file_shuffled
```
