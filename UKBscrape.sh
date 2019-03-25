#!/bin/bash -x
# Outline draft of a script to scrape UKB for list of all field IDs seen at the showcase
# Thomas E. Nichols, University of Oxford, 2018
#
URL=(\
     'http://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=0&vt=11' \
	 'http://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=0&vt=21' \
	 'http://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=0&vt=22' \
	 'http://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=0&vt=31' \
	 'http://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=0&vt=41' \
	 'http://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=0&vt=51' \
	 'http://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=0&vt=61' \
	 'http://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=0&vt=101'\
	 'https://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=20&vt=-1'\
	 'https://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=10&vt=-1'\
         'https://biobank.ctsu.ox.ac.uk/crystal/list.cgi?it=30&vt=-1')
Type=( 'Integer' \
	   'CategoricalSingle' \
	   'CategoricalMultiple' \
	   'Continuous' \
	   'Text' \
	   'Date' \
	   'Time' \
	   'Compound' )

mkdir -p IDLabCat
cp /dev/null IDLabCat/IDs_All.txt

for ((i=0;i<${#URL[@]};i++)) ; do
    wget -O /tmp/$$ "${URL[i]}"

    	### Scrape the field IDs
    grep 'field.cgi?id=' /tmp/$$ | sed 's/^.*field.cgi?id=\([0-9]*\).*$/\1/' > "IDLabCat/IDs_${Type[i]}.txt"
    cat IDLabCat/IDs_${Type[i]}.txt >> IDLabCat/IDs_All.txt

	### Scrape the categories
    grep "field.cgi?id" /tmp/$$ | sed 's@.*label.cgi\?id=[0-9]*.>*\([A-Z].*\)@\1@;s@</a>.*$@@' > "IDLabCat/Cats_${Type[i]}.txt"
    cat IDLabCat/Cats_${Type[i]}.txt >> IDLabCat/Cats_All.txt

	### Scrape the Labels
    grep "field.cgi?id" /tmp/$$ | sed 's@.*field.cgi\?id=[0-9]*.>*\(.*\)</a>@\1@;s@</a>.*$@@' > "IDLabCat/Labels_${Type[i]}.txt"
    cat IDLabCat/Labels_${Type[i]}.txt >> IDLabCat/Labels_All.txt

done
