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

*output_dir* is the output directory in which you want all the output placed.  *threads* is an optional argument where you can specify the number of threads to use.  This defaults to 1.

Once you've run this, the script will automate it's way through downloading the data from the FTP using a `curl` command and storing it in the output directory.  If you've already downloaded and extracted the data, specify the parent directory of the Nguyen_et_al_2020 directory as the output and comment out lines 51-54 which download and extract the data out, the lines are spelled out below:

```bash
echo "Downloading data..."
curl ftp://ftp.patricbrc.org/datasets/Nguyen_et_al_2020.tar.gz > $oDir/Nguyen_et_al_2020.tar.gz
echo "Decompressing data..."
tar -xzf $oDir/Nguyen_et_al_2020.tar.gz -C $oDir
```

For more information regarding what is in the downloaded data see the main repo's README file.  

Then it will begin building multiple types of models for Staphylococcus (*Klebsiella*, *Mycobacterium*, and *Salmonella* can also be added, however).  These models will be stored in the *models* directory that will be created inside the specified output directory. The following types of models will be built:
- Alignment-based models
- Clade-weighted models (no weight, weight by clade size, weight by S/R distribution in clade, weight by both)
- Gene sets (10 replicates of 100 genes, 1 replicate of 25, 50, 250, and 500 genes)
- Shuffled labels (10 replicates of 100 genes)

Note that the output directory does *not* need to reside within the repo and the bash script can be called from outside the repo as well. 

## Script Output

Inside the output directory of the script there will be a some directories:
- *models* Directory: Contains 1 directory per species which hold the respective models for each species.  
- *Nguyen_et_al_2020* Directory: The raw data used to run the models.  This raw data matches that which was used in the paper.  
- *Nguyen_et_al_2020.tar.gz* File: Tarball which was downloaded and extracted to the *Nguyen_et_al_2020* directory.  
- *rand.tab* File: Generated on the fly, random shuffling of the last run shuffled labels model.  
- *temp* Directory: A directory used to store temporary data while building models.  This can be cleared.

The *models* directory will contain 4 directories (one for each species) which each contain multiple models which have the following within their directory structure:
- all : directory containing the 5 of 10 folds run.  Each fold contains a *.pred*, *.train_hist.txt*, *.true*, *.tree*, and *pkl* file representing the predicted labels for the test set, training history (merror for train, validation, and test), true values for the testing set, text representation of the tree ensemble, and the model itself in pkl format.  Additionally, statistic files of metrics also are included *confusion_matrix.tab*, *f1.tab*, *raw_acc.tab*, and *VMEME.tab*.  *model.params* is included for the XGBoost parameters used in the model.
- model.attrOrder : attribute order for the features of the model.
- model.genomes.list : list of genomes used to train the model.
- model.labels.map : label mapping
- model.params : parameters sent to model script
- temp.txt : temprary file (used for debugging)
- weights.list : list of weights (used for debugging)


