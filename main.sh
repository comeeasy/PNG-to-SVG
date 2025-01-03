#! /bin/bash

echo "Various steps to get the final svg format output."

echo "01 - thresholding"
python ./Src/01-ResizeThreshold.py --inDir $1 --outDir "./Src/temp/01"

echo "02 - png2ppm"
inputdir='./Src/temp/01/'
outputdir='./Src/temp/02/'
if [ ! -e $"$outputdir" ]
then
   mkdir $"$outputdir"
fi
for g in $inputdir*
do
    FILE1=$(basename "${g}")
    FILE1="${FILE1%%.*}"
    convert $inputdir$(basename "${g}") $"$outputdir/$FILE1.ppm"
done

echo "03 - ppm2svg"
inputdir='./Src/temp/02/'
outputdir='./Src/temp/03/'
if [ ! -e $"$outputdir" ]
then
   mkdir $"$outputdir"
fi
for g in $inputdir*
do
    FILE1=$(basename "${g}")
    FILE1="${FILE1%%.*}"
    autotrace -centerline -color-count 2 -output-file $"$outputdir/$FILE1.svg" -output-format SVG $inputdir$(basename "${g}") || echo "autotrace failed"
done

echo "04 - svg - Cleaning"
python ./Src/04-svgCleaning.py --inDir "./Src/temp/03/" --outDir "./Src/temp/04"

echo "05 - svg - 1M - 1Path"
python ./Src/05-svg1M1Path.py --inDir "./Src/temp/04/" --outDir "./Src/temp/05" 

echo "06 - svg - 06-SmallPathRemoval"
python ./Src/06-SmallPathRemoval.py --inDir "./Src/temp/05/" --outDir "./Src/temp/06" --minLen "$3"

echo "07 - svg - longest path first"
python ./Src/07-LongestPathFirst.py --inDir "./Src/temp/06/" --outDir "./Src/temp/07"

echo "08 - svg - reorder paths: nearest starting point."
python ./Src/08-ReorderPath-Mat.py --inDir "./Src/temp/07/" --outDir "./Src/temp/08"

echo "09 - svg file cleaning"
python ./Src/09-svgCleaning.py --inDir "./Src/temp/08/" --outDir "./Src/temp/09"

cp ./Src/temp/09/* $2

rm -rf ./Src/temp/*