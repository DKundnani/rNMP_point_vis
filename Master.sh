#!usr/bin/env bash

scripts=${dirname $0}


function deeptoolscen {
samefiles=$(grep $group $files | cut -f3 | sed 's/$/_nucl_pos.bw/g'| tr '\n' ' ')
oppfiles=$(grep $group $files | cut -f3 | sed 's/$/_nucl_neg.bw/g'| tr '\n' ' ')
bref=$(basename $ref)
base="${bref%.*}"
computeMatrix reference-point -R $ref -a 3000 -b 3000 -S $(echo $samefiles $oppfiles) --referencePoint center -o $out/${base}_${group}_cen.gz --outFileSortedRegions $out/${base}_${group}_cen.bed --numberOfProcessors max -bs 100 --averageTypeBins sum  --missingDataAsZero 
plotProfile -m  $out/${base}_${group}_cen.gz -out $out/${base}_${group}_cen.png --outFileNameData $out/${base}_${group}_cen.tab --numPlotsPerRow 1 --perGroup --yMin -0  --yMax 10 --legendLocation upper-right --endLabel center  --yAxisLabel "Ribonucleotide Enrichment Factor" 
}

function separatestrand_vis_nolegend {
python3 $scripts/Deeptools_sep_all_cellline_TSS_TTS.py '$base_*TSS*tab' 4 '3.0Kb' TSS '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' nolegend separate
python3 $scripts/Deeptools_sep_all_cellline_TSS_TTS.py '$base_*TTS*tab' 4 '3.0Kb' TTS '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' nolegend separate
}

function separatestrand_vis_legend {
python3 $scripts/Deeptools_sep_all_cellline_TSS_TTS.py '$base_*TSS*tab' 4 '3.0Kb' TSS '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' legend separate
python3 $scripts/Deeptools_sep_all_cellline_TSS_TTS.py '$base_*TTS*tab' 4 '3.0Kb' TTS '#FF7F0E,#D62728,#9467BD,#E377C2,#2CA02C' legend separate
}

