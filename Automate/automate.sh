#!/bin/bash
#
# bash automate.sh [output directory] <threads=1>
# output directory : Directory to store output.  Note that
#                    THIS DIRECTORY WILL BE EMPTIED at the 
#                    start of the script using an rm -rf 
#                    command.
# threads : Number of threads to use

###
# Initialize parameters
###

if [ $# -lt 1 ]; then
	echo "bash automate.sh [output directory]"
	exit 1
fi

THREADS=1
if [ $# -gt 1 ]; then
	THREADS=$2
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SDIR=$DIR/../Scripts
UDIR=$DIR/..

###
# Make/clear output directory
###

oDir=$(echo $1 | sed 's/\/$//g')

if [ ! -d $oDir ]; then
	mkdir $oDir
else
	rm -rf $oDir
	mkdir $oDir
fi

###
# Download data
###

echo "Downloading data..."
cp ~/PLFams_static.tar.gz $oDir
# curl [INSERT URL HERE!!!]
echo "Decompressing data..."
tar -xzf $oDir/PLFams_static.tar.gz -C $oDir

RDIR=$oDir/PLFams_static

###
# Make Model Directory
###

moDir=$oDir/models
if [ ! -d $moDir ]; then
	mkdir $moDir
fi
for i in $(echo Klebsiella Mycobacterium Salmonella Staphylococcus); do
	if [ ! -d $moDir/$i ]; then
		mkdir $moDir/$i
	fi
done

###
# Alignment Models
###

echo "Doing alignment models"
for i in $(echo Staphylococcus); do
	echo $i
	aliDir=$RDIR/$i/*.raw.alis
	outAli=$RDIR/$i/ali.tab
	outInd=$RDIR/$i/ali.ord

	python $SDIR/makeAlignments.py $aliDir $outAli $outInd

	tab=$RDIR/$i/*.sir.filt.plf.tab

	tempDir=$oDir/temp

	$UDIR/GenomicModelCreator/buildModel.py -t $tab -T $tempDir -o $moDir/$i/model_ali -n $THREADS -d 16 -P True -c True -J True -S AMRcls -w True -L $outAli
done

###
# Gene Set Models
###

for i in $(echo Staphylococcus); do
	echo $i

	tab=$RDIR/$i/*.sir.filt.plf.tab
	tempDir=$oDir/temp

	for j in $(echo 25 50 100 250 500); do
		for k in $RDIR/$i/fasta.$j.*; do
			echo $k
			oMod=$moDir/$i/model_gset_$(basename $k | sed 's/fasta\.//g' | sed 's/\./_/g')
			$UDIR/GenomicModelCreator/buildModel.py -f $k -t $tab -T $tempDir -o $oMod -n $THREADS -d 16 -k 15 -P True -c True -J True -S AMRcls -w True 
		done
	done
done

###
# Randomized Models
###

for i in $(echo Staphylococcus); do
	echo $i
	tab=$RDIR/$i/*.sir.filt.plf.tab
	tempDir=$oDir/temp

	rTab=$oDir/rand.tab
	python $SDIR/shuffleLabels.py $tab > $rTab

	for j in $(echo 0 1 2 3 4 5 6 7 8 9); do
		echo $i $j
		fDir=$RDIR/$i/fasta.100.$j
		oMod=$moDir/$i/model_rand_$j
		$UDIR/GenomicModelCreator/buildModel.py -f $fDir -t $rTab -T $tempDir -o $oMod -n $THREADS -d 16 -k 15 -P True -c True -J True -S AMRcls -w True
	done
done

###
# Clade/Phylogeny models
###

for i in $(echo Staphylococcus); do
	tab=$RDIR/$i/*.sir.filt.plf.tab
	tempDir=$oDir/temp
	fDir=$RDIR/$i/fasta.100.0

	for j in $RDIR/$i/clades_use/*; do
		cldSz=$(basename $j | cut -f1 -d'.')
		for k in $(echo 0 1 2 3); do
			echo $i $j $k

			oMod=$moDir/$i/model_clade_"$cldSz"_$k

			$UDIR/GenomicModelCreator/buildModel.py -f $fDir -t $tab -T $tempDir -o $oMod -n $THREADS -d 16 -k 15 -P True -c True -J True -S AMRcls -u $k -U $j
		done
	done
done

###
# Lowest 10 important genes over 10 samples of 100 genes models
###

for i in $(echo Staphylococcus); do
	echo $i
	tab=$RDIR/$i/*.sir.filt.plf.tab
	tempDir=$oDir/temp
	fDir=$RDIR/$i/fasta.low10
	oDir=$moDir/$i/model_low10

	$UDIR/GenomicModelCreator/buildModel.py -f $fDir -t $tab -T $tempDir -o $oMod -n $THREADS -d 16 -k 15 -P True -c True -J True -S AMRcls -w True
done


