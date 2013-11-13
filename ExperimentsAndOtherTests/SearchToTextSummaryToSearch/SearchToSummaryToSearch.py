#!/usr/bin/python

'''
SEARCH > SUMMARY > SEARCH
Jeff Thompson | 2013 | www.jeffreythompson.org


NOTES:
+		text files from Archive.org may need the '\n' character
		replaced with ' ' (can be done in TextWrangler or perhaps
		automatically?)

TO DO:
+		

REQUIRES:
+		Natural Language Toolkit (NLTK)

A curatorial experiment through a residency with the Internet Archive.
'''

import requests															# for making queries to archive.org
import json																	# for parsing the results of our query
from nltk.probability import FreqDist 			# for better text parsing
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk.data

# seed text file
input_filename = 'WarOfTheWorlds.txt'

num_words = 3											# how many words to form next query
num_search_results = 25						# how many search results to return
media_type = 'text'								# we want more text, right?
collection = 'gutenberg'					# search within Project Gutenberg
sort_by = 'downloads'							# how to order the results (can also be by year, rating, downloads, etc)
sort_direction = 'asc'						# asc or desc for ascending/descending
format = 'json'										# format for results

# add to list of files (to keep track of order)
with open("SourceFiles.csv", "a") as file:
	file.write(input_filename[0:-4])

# read text from file, format into one big string
print '\nreading from file...'
input = ''
with open("SourceFiles/" + input_filename) as file:
	for line in file:
		input += line


# create list of most frequent words, list from most- to least-frequent
# taken from Tristan Havelick's 'summarize.py' (https://github.com/thavelick/summarize)
print 'getting ' + str(num_words) + ' most frequent words...'
tokenizer = RegexpTokenizer('\w+')
base_words = [ word.lower() for word in tokenizer.tokenize(input) ]
words = [word for word in base_words if word not in stopwords.words()]
word_frequencies = FreqDist(words)
most_frequent_words = [pair[0] for pair in word_frequencies.items()[:num_words]]

# print result
print ''
index = 1
search_terms = ''
for word in most_frequent_words:
	print str(index) + ':\t' + word
	search_terms += word + ' '
	index += 1
print '\nnext query: "' + search_terms + '"'

# append search term to files
with open("SourceFiles.csv", "a") as file:
	file.write("\n" + search_terms.strip() + ",")

# submit data request
data = { 'q': search_terms, 'collection': collection, 'sort': sort_by + '+' + sort_direction, 'rows': num_search_results, 'output': format, 'save': 'yes#raw' }
headers = { 'Content-type': 'application/json' }
response = requests.post('http://archive.org/advancedsearch.php', params=data, headers=headers)

# convert to dictionary (easier to parse)
search_results = json.loads(response.text)

# run search query
print '\nsearch URL:  ' + response.url + '\n'			# resulting search URL (can also be pasted into your browser)'
print '\nretrieving first ' + str(num_search_results) + ' search results...'

# iterate details
for item in search_results['response']['docs']:
	print '\n' + ('- ' * 36) + '\n'												# divider between listings
	print 'Title:       ' + item['title']						# object title
	print 'Format:     ',														# what format is the object in
	for format in item['format']:
		print format + ',',
	print ''
	print 'URL:         www.archive.org/details/' + item['identifier']

print '\nDONE!\n\n'