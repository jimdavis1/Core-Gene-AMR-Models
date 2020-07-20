#!/bin/bash
#
# bash automate.sh [output directory] <threads=1>
# output directory : Directory to store output.  Note that
#                    THIS DIRECTORY WILL BE EMPTIED at the 
#                    start of the script using an rm -rf 
#                    command.
# threads : Number of threads to use

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
RDIR=$DIR/..

oDir=$(echo $1 | sed 's/\/$//g')

if [ ! -d $oDir ]; then
	mkdir $oDir
else
	rm -rf $oDir
	mkdir $oDir
fi

for i in $(echo Klebsiella Mycobacterium Salmonella Staphylococcus); do
	echo $i
	if [ ! -d $oDir/$i ]; then
		mkdir $oDir/$i
	fi

	aliDir=$RDIR/$i/*.raw.alis
	outAli=$oDir/$i/ali.tab
	outInd=$oDir/$i/ali.ord

	python $SDIR/makeAlignments.py $aliDir $outAli $outInd

	tab=$RDIR/$i/*.sir.filt.plf.tab

	tempDir=$oDir/temp

	$RDIR/GenomicModelCreator/buildModel.py -t $tab -T $tempDir -o $oDir/$i/model_ali -n $THREADS -d 16 -P True -c True -J True -S AMRcls -w True -L $outAli
done