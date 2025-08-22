
<h1 align="center">rNMP distribution analysis</h1>
To obtain rNMP enrichment distribution around a fixed point in the genome for separate strands based on either given strand information of watson and crick strands
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
-->

[![Commits][Commits-shield]][Commits-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Website][website-shield]][website-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="##Installation">Installation</a></li>
      <ul>
        <li><a href="###Getting-the-code">Getting the code</a></li>
        <li><a href="###Creating-the-enviroment-with-required-dependencies">Creating the enviroment with required dependencies</a></li>
        <li><a href="###Additional-Dependencies">Additional Dependencies</a></li>
      </ul>
    </li>
    <li><a href="##Usage">Usage</a></li>
      <ul>
        <li><a href="###Defining-variables">Defining variables</a></li>
        <li><a href="###Preprocessing">Preprocessing</a></li>
        <li><a href="###Loading-Functions">Loading Functions</a></li>
       <li><a href="###Analyzing-and-processing-data-1">Analyzing, processing and visualizing data for TSS/TTS (ends) of ranges provided</a></li>
        <li><a href="###Analyzing-and-processing-data-2">Analyzing, processing and visualizing data for center of ranges provided</a></li>
      </ul>
    <li><a href="##Contributing">Contributing</a></li>
    <li><a href="##License">License</a></li>
    <li><a href="##Contact">Contact</a></li>
    <li><a href="##Citations">Citations</a></li>
  </ol>
</details>

<!-- Installation -->
## Installation
### Getting the code
The development version from [GitHub](https://github.com/) with:
```sh
git clone https://github.com/DKundnani//rNMP_point_vis.git
```
### Required dependencies 
* bedtools
* ucsc-bedGraphToBigWig
* Deeptools

### Additional Dependencies
* Input files (bed) containing single nucleotide locations, mainly for rNMP data. (another single nucleotide data can also be experimented on!)
* Reference genome files (.fa and .fai) of the organism being used(Also used to generate bed files)
* Range files in preferably bed format See [https://github.com/DKundnani/Omics-pipelines](https://github.com/DKundnani/Omics-pipelines)

<!-- USAGE -->
## Usage
### Defining variables
```bash
bin=100 #bin size to be used
hggenome='path/to/reference_genome.fa.fai' #genome size file
bed='path/to/bedfolder/' #all the .bed files to be processed
bw='path/to/bwfolder/' #output for bigwig files to be used, make sure you have _pos and _neg bigwig files in separate strands folder for each bed file as output
files='path/to/files' #Same file provided
ref='path/to/range.bed' #Reference bed file with chr,start,stop
celltypes='CD4T hESC-H9 HEK283T-WT HEK293T-RNASEH2A-KO-T3-17 HEK293T-RNASEH2A-KO-T3-8' #List of celllines to be visualized, matches the identifiers in files
out=$bw/out #Output folder where all the results will be stored
scripts='path/to/rNMP_point_vis/'
```
### Preprocessing
```bash
mkdir -p $bw
for file in $(ls $bed/*.bed)
do
bash $scripts/bedtoEF.sh $file $hggenome $bin $bw
done

```
### Loading Functions
```bash
source $scripts/Master.sh
```
### Analyzing, processing and visualizing data for TSS/TTS (ends) of ranges provided
```bash
cd $bw
mkdir -p $out/temp
mkdir -p $out/tab
for type in $celltypes; do
bref=$(basename $ref)
base="${bref%.*}"
awk 'BEGIN{FS=OFS="\t"} {if($6=="+") {print $1,$2,$3}}' $ref > $out/temp/${base}_pos.bed #Change this ONLY IF strand information in any other than 6th column.
awk 'BEGIN{FS=OFS="\t"} {if($6=="-") {print $1,$2,$3}}' $ref > $out/temp/${base}_neg.bed #Change this ONLY IF strand information in any other than 6th column.
deeptoolsref &
done
wait
cd $out
for type in $celltypes; do separatestrand_vis_legend & done #With legend, only for checking each cell type is assigned correct color
for type in $celltypes; do separatestrand_vis_nolegend & done #Vislualized for all files present in the output folder. Please clean up unwanted file of create separate output folder with wanted files only


```
### Analyzing, processing and visualizing data for center of ranges provided
```bash
cd $bw
for type in $celltypes; do
deeptoolscen &
done
wait
cd $out
separatestrand_vis_cen #Vislualized for all files present in the output folder. Please clean up unwanted file of create separate output folder with wanted files only

```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact
Deepali L. Kundnani - [deepali.kundnani@gmail.com](mailto::deepali.kundnani@gmail.com)    [![LinkedIn][linkedin-shield]][linkedin-url] 
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Citations
Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!+
* <b> Human ribomes reveal DNA-embedded ribonucleotides as a new type of epigenetic mark. </b>
Deepali Lalchand Kundnani, Taehwan Yang, Tejasvi Channagiri, Penghao Xu, Yeunsoo Lee, Mo Sun, Francisco Martinez-Figueroa, Supreet Randhawa, Ashlesha Gogate, Youngkyu Jeon, Stefania Marsili, Gary Newnam, Yilin Lu, Vivian Park, Sijia Tao, Justin Ling, Raymond Schinazi, Zachary Pursell, Abdulmelik Mohammed, Patricia Opresko, Bret Freudenthal, Baek Kim, Soojin Yi, Nataša Jonoska, Francesca Storici, <i>  bioRxiv </i> 2025, [https://doi.org/10.1101/2025.06.27.661996](https://doi.org/10.1101/2025.06.27.661996)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/DKundnani/rNMP_point_vis?style=for-the-badge
[contributors-url]: https://github.com/DKundnani/rNMP_point_vis/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DKundnani/rNMP_point_vis?style=for-the-badge
[forks-url]: https://github.com/DKundnani/rNMP_point_vis/forks
[stars-shield]: https://img.shields.io/github/stars/DKundnani/rNMP_point_vis?style=for-the-badge
[stars-url]: https://github.com/DKundnani/rNMP_point_vis/stargazers
[issues-shield]: https://img.shields.io/github/issues/DKundnani/rNMP_point_vis?style=for-the-badge
[issues-url]: https://github.com/DKundnani/rNMP_point_vis/issues
[license-shield]: https://img.shields.io/github/license/DKundnani/rNMP_point_vis?style=for-the-badge
[license-url]: https://github.com/DKundnani/rNMP_point_vis/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/deepalik
[product-screenshot]: images/screenshot.png
[commits-url]: https://github.com/DKundnani/rNMP_point_vis/pulse
[commits-shield]: https://img.shields.io/github/commit-activity/t/DKundnani/rNMP_point_vis?style=for-the-badge
[website-shield]: https://img.shields.io/website?url=http%3A%2F%2Fdkundnani.bio%2F&style=for-the-badge
[website-url]:http://dkundnani.bio/ 
