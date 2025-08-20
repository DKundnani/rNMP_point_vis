#!usr/bin/env bash

#scripts=${dirname $0}

function deeptoolsref {
samefiles=$(grep $type $files | cut -f3 | sed 's/$/_pos.bw/g'| tr '\n' ' ')
oppfiles=$(grep $type $files | cut -f3 | sed 's/$/_neg.bw/g'| tr '\n' ' ')
computeMatrix reference-point -R $out/temp/${base}_pos.bed -a 3000 -b 3000 -S $(echo $samefiles $oppfiles) --referencePoint TSS -o $out/temp/${base}_${type}_pos_TSS.gz --outFileSortedRegions $out/temp/${base}_${type}_pos_TSS.bed --numberOfProcessors max -bs $bin --averageTypeBins sum  --missingDataAsZero 
computeMatrix reference-point -R $out/temp/${base}_pos.bed -a 3000 -b 3000 -S $(echo $samefiles $oppfiles) --referencePoint TES -o $out/temp/${base}_${type}_pos_TTS.gz --outFileSortedRegions $out/temp/${base}_${type}_pos_TTS.bed --numberOfProcessors max -bs $bin --averageTypeBins sum  --missingDataAsZero 
computeMatrix reference-point -R $out/temp/${base}_neg.bed -a 3000 -b 3000 -S $(echo $oppfiles $samefiles) --referencePoint TSS -o $out/temp/${base}_${type}_neg_TSS.gz --outFileSortedRegions $out/temp/${base}_${type}_neg_TSS.bed --numberOfProcessors max -bs $bin --averageTypeBins sum  --missingDataAsZero 
computeMatrix reference-point -R $out/temp/${base}_neg.bed -a 3000 -b 3000 -S $(echo $oppfiles $samefiles) --referencePoint TES -o $out/temp/${base}_${type}_neg_TTS.gz --outFileSortedRegions $out/temp/${base}_${type}_neg_TTS.bed --numberOfProcessors max -bs $bin --averageTypeBins sum  --missingDataAsZero   
plotProfile -m  $out/temp/${base}_${type}_pos_TSS.gz -out $out/temp/${base}_${type}_pos_TSS.png --outFileNameData $out/temp/${base}_${type}_pos_TSS.tab --numPlotsPerRow 1 --perGroup --yMin -10  --yMax 8 --legendLocation upper-right --endLabel TSS  --yAxisLabel "Ribonucleotide Enrichment Factor" 
plotProfile -m  $out/temp/${base}_${type}_neg_TSS.gz -out $out/temp/${base}_${type}_neg_TSS.png --outFileNameData $out/temp/${base}_${type}_neg_TSS.tab --numPlotsPerRow 1 --perGroup --yMin -10  --yMax 8 --legendLocation upper-right --endLabel TSS  --yAxisLabel "Ribonucleotide Enrichment Factor" 
plotProfile -m  $out/temp/${base}_${type}_pos_TTS.gz -out $out/temp/${base}_${type}_pos_TTS.png --outFileNameData $out/temp/${base}_${type}_pos_TTS.tab --numPlotsPerRow 1 --perGroup --yMin -10  --yMax 8 --legendLocation upper-right --endLabel TTS  --yAxisLabel "Ribonucleotide Enrichment Factor" 
plotProfile -m  $out/temp/${base}_${type}_neg_TTS.gz -out $out/temp/${base}_${type}_neg_TTS.png --outFileNameData $out/temp/${base}_${type}_neg_TTS.tab --numPlotsPerRow 1 --perGroup --yMin -10  --yMax 8 --legendLocation upper-right --endLabel TTS  --yAxisLabel "Ribonucleotide Enrichment Factor" 
python $scripts/merge_tab.py $out/temp/${base}_${type}_pos_TSS.tab $out/temp/${base}_${type}_neg_TTS.tab '3.0Kb' $out/tab/${base}_${type}_merged_TSS.tab positive
python $scripts/merge_tab.py $out/temp/${base}_${type}_pos_TTS.tab $out/temp/${base}_${type}_neg_TSS.tab '3.0Kb' $out/tab/${base}_${type}_merged_TTS.tab positive
}

function deeptoolscen {
samefiles=$(grep $type $files | cut -f3 | sed 's/$/_nucl_pos.bw/g'| tr '\n' ' ')
oppfiles=$(grep $type $files | cut -f3 | sed 's/$/_nucl_neg.bw/g'| tr '\n' ' ')
computeMatrix reference-point -R $ref -a 3000 -b 3000 -S $(echo $samefiles $oppfiles) --referencePoint center -o $out/${base}_${type}_cen.gz --outFileSortedRegions $out/${base}_${type}_cen.bed --numberOfProcessors max -bs 100 --averageTypeBins sum  --missingDataAsZero 
plotProfile -m  $out/${base}_${type}_cen.gz -out $out/${base}_${type}_cen.png --outFileNameData $out/${base}_${type}_cen.tab --numPlotsPerRow 1 --perGroup --yMin -0  --yMax 10 --legendLocation upper-right --endLabel center  --yAxisLabel "Ribonucleotide Enrichment Factor" 
}

function separatestrand_vis_nolegend {
python3 $scripts/all_celltypes_vis.py ${base}'_*TSS*tab' 4 '3.0Kb' TSS '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' nolegend separate publish
python3 $scripts/all_celltypes_vis.py ${base}'_*TTS*tab' 4 '3.0Kb' TTS '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' nolegend separate publish
}

function separatestrand_vis_legend {
python3 $scripts/all_celltypes_vis.py ${base}'_*TSS*tab' 4 '3.0Kb' TSS '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' legend separate publish
python3 $scripts/all_celltypes_vis.py ${base}'_*TTS*tab' 4 '3.0Kb' TTS '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' legend separate publish
}

function separatestrand_vis_cen {
python3 $scripts/all_celltypes_vis.py ${base}'_*cen*tab' 4 '3.0Kb' cntr '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' nolegend separate publish
}

