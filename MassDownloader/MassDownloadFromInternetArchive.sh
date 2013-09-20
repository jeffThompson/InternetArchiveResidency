#!/bin/bash
# MASS DOWNLOAD FROM INTERNET ARCHIVE
# Jeff Thompson | 2013 | www.jeffreythompson.org
#
# Fancier wrapper for a basic 'wget' command to download files
# from the Internet Archive.

inputFile='brightness.txt'
baseURL='http://archive.org/download/'
downloadFolder='downloadedFiles/'

echo ""
echo "MASS DOWNLOAD FROM INTERNET ARCHIVE"
echo "Jeff Thompson | 2013 | www.jeffreythompson.org"
echo ""
echo "Reading from \"$inputFile\""
echo ""

numFiles=$(wc -l < $inputFile | sed -e 's/^ *//g' -e 's/ *$//g')		# num of files, with whitespace removed
i=1

while read line
do
	url=$baseURL$line	
	echo "$i / $numFiles		$url"
	
	# get PDFs only
	# wget -r -H -nc -np -nH -q --cut-dirs=2 -e robots=off -l1 -A .pdf -P $downloadFolder $url
	
	# get thumbnails (GIFs) only
	wget -r -H -nc -np -nH -q --cut-dirs=2 -e robots=off -l1 -A .gif -P $downloadFolder $url

	let i++
done < $inputFile

echo ""
echo "DONE!"
echo ""