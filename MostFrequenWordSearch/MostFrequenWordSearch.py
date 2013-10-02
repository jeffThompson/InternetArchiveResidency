#!/usr/bin/python

'''
MOST FREQUENT WORD SEARCH
Jeff Thompson | 2013 | www.jeffreythompson.org

A curatorial experiment through a residency with the Internet Archive.

Searches for a given term, downloads the first result, parses the downloaded
text for the most frequent words, then uses the top word as a new search term.

The process is repeated until the search fails.


REQUIRES:
+ Natural Language Toolkit (NLTK)
		http://nltk.org
+ Internet Archive search module
		https://pypi.python.org/pypi/internetarchive
+ OPTIONAL: Tumblr API for auto-posting
		https://github.com/tumblr/pytumblr

TO DO:
+ do we really want to skip words 'project' and 'gutenberg'?
+ did html formatted string work?
+ skip already-traversed files/entries

'''

import internetarchive as ia								# import easier Internet Archive searching
from nltk.probability import FreqDist				# NLTK for word parsing
from nltk.tokenize import RegexpTokenizer
import os																		# for listing files, etc
import pytumblr															# Tumblr API (optional)
 
search_term = 'random'											# term to search for (multiple words ok w/ spaces between)
min_word_len = 5														# minimum length of word, larger = more likely to be a unique word
collection = 'gutenberg'										# collection to search within
return_data = [ 'identifier', 'title' ]			# list of data to return (downloads, date, author, etc)
pathway_string_separator = ' &rarr; '				# character(s) between search term pathway; include spaces if desired

download_folder = 'DownloadedFiles'					# folder to save to
file_format = '.txt'												# file format(s) so download, separate with commas
num_top_words = 10													# number of words to list (no effect on search or parsing)

post_to_tumblr = True															# auto-post to Tumblr?
blog_address = 'jeff-thompson-iatr.tumblr.com'		# URL if posting to Tumblr

output_filename = search_term + '.csv'			# output results to file
pathway_string = search_term								# build string of search terms
html_pathway_string = ''										# html-formatted string with links
first_search = True
traversed_ids = []													# to ensure we don't traverse the same file twice
bold_start = '\033[1m'											# special characters for bold text output in Terminal window...
bold_end = '\033[0m'												# via http://askubuntu.com/a/45246


# CREATE CSV IF IT DOESN'T ALREADY EXIST
# write header, input search term
if not os.path.exists(output_filename):
	with open(output_filename, 'a') as csv:
		csv.write('search_term,id,title,downloaded_file')


# UNNECESSARY FANCINESS
# creates a divider between listings based on size of Terminal window
columns = 40
rows, columns = os.popen('stty size', 'r').read().split()
display_divider = '- ' * (int(columns)/2)


# RUN PROCESS UNTIL SOMETHING BREAKS :)
# ie: when we get no search results, etc...
while True:

	# SEARCH
	print '\n' + bold_start + 'searching for "' + search_term + '"...' + bold_end
	search_query = search_term.lower() + ' AND (collection:' + collection + ')'
	search = ia.Search(search_query, return_data)
	if (search.num_found > 0):
		print '\nfound ' + str(search.num_found) + ' results:'
		for result in search.results:
			id = result['identifier']
			title = result['title']
			if id in traversed_ids:			# if already parsed, skip to next result in list
				print '  already traversed ' + id + ', moving to next result...'
				continue				
			else:
				if len(title) > 60:
					print '  "' + title[:60] + '..."'
				else:
					print '  "' + title + '"'
				break

		if first_search:
			first_search = False
			html_pathway_string += '<strong><a href="http://archive.org/details/' + id + '">' + search_term + '</a></strong>'
		else:
			html_pathway_string += pathway_string_separator + '<a href="http://archive.org/details/' + id + '">' + search_term + '</a>'
		
			
	else:
		print '  no search results for that query, sorry!\n'
		
		# add last (no results) search term to end of pathway
		html_pathway_string += pathway_string_separator + search_term
		break


	# DOWNLOAD
	print '\ndownloading files from the first search result...'
	download_string = 'wget -r -H -nc -np -nH -q --cut-dirs=2 -e robots=off -l1 -A ' + file_format + ' -P ' + download_folder + ' http://archive.org/download/' + id
	os.system(download_string)

	downloaded_files = os.listdir(download_folder + '/' + id)
	for file in downloaded_files:
		if 'meta' not in file and file.endswith('.txt'):
			print '  ' + file
			downloaded_filename = download_folder + '/' + id + '/' + file
			break


	# EXTRACT WORDS AND COUNT FREQUENCY
	print '\ncounting word frequencies in "' + file + '"...'
	text = ''
	with open(downloaded_filename) as file:
		for line in file:
			text += line
	tokenizer = RegexpTokenizer('\w+')
	words = []
	for word in tokenizer.tokenize(text):
		if len(word) > min_word_len:					# only add if long enough
			words.append(word.lower())					# make sure words are lowercase
	freq_dist = FreqDist(words)							# count resulting words


	# GET N MOST FREQUENT WORDS
	most_freq = []
	for i, word in enumerate(freq_dist.keys()):
		if word == 'project' or word == 'gutenberg':		# skip, just in case
			continue
		most_freq.append(word)
		if i < num_top_words:
			print '  ' + str(freq_dist[word]) + ': ' + word


	# GET NEXT SEARCH TERM
	for term in most_freq:
		if term != search_term:
			search_term = term
			break
	print '\nnext search term: "' + search_term + '"' + '\n'
	pathway_string += pathway_string_separator + search_term


	# SAVE DATA TO FILE
	# append to existing file as csv-formatted data
	# note: saves title in quotes in case of commas
	with open(output_filename, 'a') as csv:
		csv.write('\n' + search_term + ',' + id + ',"' + title + '",' + downloaded_filename)
	
	
	# PRINT A DIVIDER AND CONTINUE
	print display_divider


# IF SPECIFIED, POST TO TUMBLR :)
# authenticate via OAuth and post using Tumblr API - easy!
if post_to_tumblr:
	print display_divider
	print '\n' + bold_start + 'posting results to Tumblr...' + bold_end

	client = pytumblr.TumblrRestClient(
		'zL2GXi09jX2KcPQcnrJoyXGBUGETAB7bl4TVpYDd4ODB8ZBoMA',
		'CAjlOmh61JXafXAShg5MtRYHYSqFzWhK4pJ1r98BwLrdXqu2PP',
		'CvUc32kSnkx8JCVKmKUessqdQBw6Dn3ACGpPuWnURlNKHodC9L',
		'ZKTolmjfXqxNCynnRkQVYTQQO5gj20F9YXhCRa8v6L10D0epNk'
	)
	
	response = client.create_text(blog_address, body=html_pathway_string)
	if 'id' in response:
		print '  post successful!'
	else:
		print '  error uploading post, sorry... :('
	
	
# ALL DONE! PRINT RESULTING PATHWAY
print '\n' + display_divider + '\n'
print bold_start + 'resulting pathway:' + bold_end + '\n' + pathway_string
print '\n' + bold_start + 'html-formatted pathway:' + bold_end + '\n' + html_pathway_string
print '\n\nDONE!'
print ('\n' * 3)
