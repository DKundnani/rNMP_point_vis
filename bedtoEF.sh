#! usr/bin/bash
#Common functions
#Author: Deepali L Kundnani 
#Institute: Georgia Institute of Technology
#Dependencies: bedtools, bedGraphToBigWig

#please provide positional parameters
#first is for the file(s) to be sorted
#second the chr sizesfile

#Usage: 
#for file in $(ls *.bed);do bash bedtoEF.sh $file genome.sizes; done

if [ "$1" = "" ]; then
    echo "a file with columne of file names"
    echo "for file in $(ls *.bed);do bash bedtoEF.sh file.bed genome.sizes binsize; done"
fi

if [ "$2" = "" ]; then
    echo "Please enter the genome size or fa.fai files with only the chromosomes required"
    echo "for file in $(ls *.bed);do bash bedtoEF.sh file.bed genome.sizes binsize; done"
else 
    genome=$(echo $2)
fi

if [ "$3" = "" ]; then
    bin=1
    echo "Accounting for binsize as 1 in the normalization factor so the values in the same bin can be added. If you want to change bin size, please provide another bin size as the third argument and rerun the code"
    echo "for file in $(ls *.bed);do bash bedtoEF.sh file.bed genome.sizes binsize; done"
else 
    bin=$(echo $3)
fi

if [ "$4" = "" ]; then
    out='.'
    echo "Current directory used for output"
    echo "for file in $(ls *.bed);do bash bedtoEF.sh file.bed genome.sizes binsize; done"
else 
    out=$(echo $4)
fi

if [ "$1" = "-h" ]; then
    echo "for file in $(ls *.bed);do bash bedtoEF.sh $file genome.sizes; done"
    echo "file/files as first positional paramater"
    echo "genome.sizes or fa.fai files with only the chromosomes required as the second positional parameter"
fi

file=$1
echo "............Working on: "$(basename $file)"............"

echo "1.Counting avergae rNMP value normalized for binsize $bin"
ribocount=$(cat $file | wc -l)

genomesize=$(cut -f2 $genome | paste -sd+ | bc) #Alternate is to count positions instead of genome size
#genomesize=$(cat $file | cut -f1-2 | uniq | wc -l)
riboperbaseforbin=$(echo $ribocount*$bin/$genomesize | bc -l)

echo "2.Getting bedgraph and BigWig files for both strands"
##Both Strands
bedtools genomecov -dz -scale $(echo 1/$riboperbaseforbin|bc -l) -i $file -g $genome | awk -F'\t' '{print $1"\t"$2"\t"$2+1"\t"$3}'> $out/$(basename $file .bed).bg
bedGraphToBigWig $out/$(basename $file .bed).bg $genome $out/$(basename $file .bed).bw

echo "3.Separating Strand information"
grep -e '\s+$' $file >  $out/$(basename $file .bed)_pos.bed
grep -e '\s-$' $file >  $out/$(basename $file .bed)_neg.bed

echo "4.Getting bedgraph and BigWig files for separate strands"
##Separate Strands
bedtools genomecov -dz -scale $(echo 2/$riboperbaseforbin|bc -l) -i  $out/$(basename $file .bed)_pos.bed -g $genome | awk -F'\t' '{print $1"\t"$2"\t"$2+1"\t"$3}' >  $out/$(basename $file .bed)_pos.bg
bedGraphToBigWig  $out/$(basename $file .bed)_pos.bg $genome  $out/$(basename $file .bed)_pos.bw
bedtools genomecov -dz -scale $(echo 2/$riboperbaseforbin|bc -l) -i  $out/$(basename $file .bed)_neg.bed -g $genome | awk -F'\t' '{print $1"\t"$2"\t"$2+1"\t"$3}' >  $out/$(basename $file .bed)_neg.bg
bedGraphToBigWig $out/$(basename $file .bed)_neg.bg $genome $out/$(basename $file .bed)_neg.bw

echo "5.Combining and sorting bedgraphs for positive and negative strand in .norm format"
sed 's/$/\t.\t+/' $out/$(basename $file .bed)_pos.bg > $out/$(basename $file .bed).norm
sed 's/$/\t.\t-/' $out/$(basename $file .bed)_neg.bg >> $out/$(basename $file .bed).norm
bedtools sort -i $out/$(basename $file .bed).norm > $out/sorted_$(basename $file .bed).norm

[ ! -d $out/both_strands ] && [ ! -d $out/separate_strands ] && mkdir $out/both_strands $out/separate_strands

mv $out/$(basename $file .bed)_neg* $out/separate_strands/
mv $out/$(basename $file .bed)_pos* $out/separate_strands/
mv $out/$(basename $file .bed)* $out/both_strands/
 

#computeMatrix scale-regions -R /storage/coda1/p-fstorici3/0/shared/MSshared/expression/anno-ranges/hg38_transcript.bed --beforeRegionStartLength 10000 --afterRegionStartLength 10000 -S FS190_nucl.bw FS203_nucl.bw FS305_nucl.bw FS336_nucl.bw -o missingvalue_1.gz --outFileSortedRegions missingvalue_1.bed --numberOfProcessors max --regionBodyLength 30000 -bs 500 --missingDataAsZero --averageTypeBins sum

#plotProfile -m missingvalue_1.gz -out missingvalue_1.pdf --numPlotsPerRow 2 --perGroup  --yMin 0
