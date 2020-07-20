# Automate.sh

The bash script in this directory is designed to automate the building of alignment-based models from the alignments in this repo.  It utilizes the *GenomicModelCreator* submodule.  As such, you'll need to init and download this submodule using git before this script can run successfully.  This can be done by running the following from this repo's root directory (not this directory, but this directory's parent).

``` bash
git submodule init
git submodule update
```

Note that the *GenomicModelCreator* submodule has some requirements of its own as well:
- [KMC](http://sun.aei.polsl.pl/REFRESH/index.php?page=projects&project=kmc&subpage=about) must be installed and the *kmc*, *kmc_dump*, and *kmc_tools* executibles must be in your path.
- Python 2.7 along with various packages and libraries must be installed: numpy ([website](https://numpy.org), [anaconda](https://anaconda.org/anaconda/numpy)), sklearn ([website](https://scikit-learn.org/stable/), [anaconda](https://anaconda.org/anaconda/scikit-learn)), scipy ([website](https://www.scipy.org), [anaconda](https://anaconda.org/anaconda/scipy)), xgboost ([website](https://xgboost.readthedocs.io/en/latest/), [anaconda](https://anaconda.org/conda-forge/xgboost)).  For ease of setup, it's recommended that Anaconda be used for this, but it's not required.
- Make sure the *KMC* directory in the *GenomicModelCreator* directory is in your PATHS.  Note the *KMC* directory will only appear after you have init and update the submodule as described above!

## Running the Script

Once everything is set up, running the script is simple.  In bash, you run the following:

``` bash
bash /pathtoautomate/automate.sh [output_dir] <threads>
```

*output_dir* is the output directory in which you want all the output placed.  Note this directory will be cleared out using *rm -rf* before the script runs!  *threads* is an optional argument where you can specify the number of threads to use.  This defaults to 1.

Once you've run this, the script will automate it's way through building 4 alignment-based models for *Klebsiella*, *Mycobacterium*, *Salmonella*, and *Staphylococcus*.  

Note that the output directory does *not* need to reside within the repo and the bash script can be called from outside the repo as well.  

## Memory Requirements

These XGBoost models for alignments still require lots of RAM despite only utilizing non-redudant alignments on 100 genes.  Below is the recommended amount of memory (RAM) for each of the models:

|Model           |Memory|
|----------------|------|
|*Klebsiella*    |64 GB |
|*Mycobacterium* |128 GB|
|*Salmonella*    |128 GB|
|*Staphylococcus*|32 GB |

These are very loose minimum requirements.  In the event you run into an *out of memory* error, it normally means you didn't have enough RAM.  

If you wish to skip any given species from running (due to RAM/time constraints) you can do so by editing line 35 in the *automate.sh* script to remove the species you wish to not run.  

## Basic Logic of Script

The script starts by checking for the output directory and clearing it out before running.  

For each species, the script will run the *makeAlignments.py* script located in the *../Scripts/* directory and then use that as input into the *buildModel.py* script in the *../GenomicModelCreator/* directory.  

