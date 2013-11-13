#!/usr/bin/python

'''
MOST FREQUENT WORD SEARCH
Jeff Thompson | 2013 | www.jeffreythompson.org

A curatorial experiment through a residency with the Internet Archive.

Searches for a given term, downloads the first result, parses the downloaded
text for the most frequent words, then uses the top word as a new search term.

The process is repeated until the search fails, then continues with a new
search from the next word in the list.

OAuth settings for posting to Tumblr are loaded from a separate file, which
contains a Python dictionary for the consumer key, etc in the following format:

	settings = {
		'consumer_key': 'xxxx',
		'consumer_secret': 'xxxx',
		'access_token_key': 'xxxx',
		'access_token_secret': 'xxxx'
	}

REQUIRES:
+ Natural Language Toolkit (NLTK)
		http://nltk.org
+ Internet Archive search module
		https://pypi.python.org/pypi/internetarchive
+ OPTIONAL: Tumblr API for auto-posting
		https://github.com/tumblr/pytumblr

'''

import internetarchive as ia								# import easier Internet Archive searching
from nltk.probability import FreqDist				# NLTK for word parsing
from nltk.tokenize import RegexpTokenizer
import os																		# for listing files, etc
import pytumblr															# Tumblr API (optional)
from OAuthSettings import settings					# import from settings.py

# text file of input words
input_file_list = 'WordLists/OldMortality_500MostCommonWords.txt'

min_word_len = 5																	# minimum length of word, larger = more likely to be a unique word
collection = 'gutenberg'													# collection to search within
return_data = [ 'identifier', 'title' ]						# list of data to return (downloads, date, author, etc)
pathway_string_separator = ' &rarr; '							# character(s) between search term pathway; include spaces if desired
download_folder = 'DownloadedFiles'								# folder to save to
file_format = '.txt'															# file format(s) so download, separate with commas
num_top_words = 10																# number of words to list (no effect on search or parsing)
post_to_tumblr = True															# auto-post to Tumblr?
blog_address = 'jeff-thompson-iatr.tumblr.com'		# URL if posting to Tumblr
max_posts = 250																		# how many posts per day? currently Tumblr limits to 250

bold_start = '\033[1m'														# special characters for bold text output in Terminal window...
bold_end = '\033[0m'															# via http://askubuntu.com/a/45246
pathway_string = ''																# initialize string
num_posted = 0																		# count # of posts


# UNNECESSARY FANCINESS
# clear terminal window first :)
os.system('cls' if os.name=='nt' else 'clear')

# creates a divider between listings based on size of Terminal window
columns = 40
rows, columns = os.popen('stty size', 'r').read().split()
display_divider = '- ' * (int(columns)/2)


# IMPORT ALL WORDS FROM FILE
print '\n' + bold_start + 'MOST FREQUENT WORD SEARCH' + bold_end
print 'loading words for search...\n'
all_words = []
with open(input_file_list) as file:
	for word in file:
		all_words.append(word.strip())
print display_divider + '\n'


# RUN SEARCH ON ALL WORDS! 
for i, search_term in enumerate(all_words):
	
	# CLEAR AND PRINT PREVIOUS DETAILS
	os.system('cls' if os.name=='nt' else 'clear')
	print '\n' + bold_start + 'previous path (' + str(num_posted+1) + '/' + str(max_posts) + '): ' + bold_end + pathway_string
	print '\n' + display_divider + '\n'
	print bold_start + str(i+1) + '/' + str(len(all_words)) + ': ' + bold_end,

	# RESET VARIABLES	
	pathway_string = search_term								# build string of search terms
	output_filename = search_term + '.csv'			# output results to file
	html_pathway_string = ''										# html-formatted string with links
	first_search = True
	traversed_ids = []													# to ensure we don't traverse the same file twice
	searched_terms = []													# ensure we don't get the same search terms either


	# CREATE CSV IF IT DOESN'T ALREADY EXIST
	# write header, input search term
	if not os.path.exists('SearchPathways/' + output_filename):
		with open('SearchPathways/' + output_filename, 'a') as csv:
			csv.write('search_term,id,title,downloaded_file')


	# SEARCH UNTIL SOMETHING BREAKS :)
	# ie: when we get no search results, etc...
	no_results = False
	while True:

		# FORMAT QUERY
		print bold_start + 'searching for "' + search_term + '"...' + bold_end
		search_query = search_term.lower() + ' AND (collection:' + collection + ')'
		search = ia.Search(search_query, return_data)

		# SEARCH
		if (search.num_found > 0) and search_term not in searched_terms:
			searched_terms.append(search_term.lower())
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
				html_pathway_string += '<strong><a class="linkToIA" href="http://archive.org/details/' + id + '" target="_blank">' + search_term + '</a></strong>'
			else:
				html_pathway_string += pathway_string_separator + '<a class="linkToIA" href="http://archive.org/details/' + id + '" target="_blank">' + search_term + '</a>'
		
		else:
			print '  no search results for that query, sorry!\n'
			if first_search:
				no_results = True
				html_pathway_string += search_term
			else:
				# add last (no results) search term to end of pathway
				html_pathway_string += pathway_string_separator + search_term
			break


		# DOWNLOAD
		print '\ndownloading files from the first search result...'
		download_string = 'wget -r -H -nc -np -nH -q --cut-dirs=2 -e robots=off -l1 -A ' + file_format + ' -P ' + download_folder + ' http://archive.org/download/' + id
		os.system(download_string)

		try:
			downloaded_files = os.listdir(download_folder + '/' + id)
			for file in downloaded_files:
				if 'meta' not in file and file.endswith('.txt'):
					print '  ' + file
					downloaded_filename = download_folder + '/' + id + '/' + file
					break
		except OSError:
			print 'error finding downloaded file, skipping...'
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
			try:
				test_encoding = term.encode('ascii', 'ignore')
			except UnicodeDecodeError:
				continue
			if term != search_term:
				search_term = term
				break
		print '\nnext search term: "' + search_term + '"' + '\n'
		pathway_string += pathway_string_separator + search_term


		# SAVE DATA TO FILE
		# append to existing file as csv-formatted data
		# note: saves title in quotes in case of commas
		if pathway_string != search_term:
			with open('SearchPathways/' + output_filename, 'a') as csv:
				try:
					line_to_save = '\n' + search_term + ',' + id + ',"' + title + '",' + downloaded_filename
					csv.write(line_to_save.encode('ascii', 'ignore'))
				except UnicodeDecodeError:
					print 'error writing line to file, skipping...'
					csv.write('error,error,error,error')


		# PRINT A DIVIDER AND CONTINUE SEARCHING
		print display_divider + '\n'


	# IF SPECIFIED, POST TO TUMBLR :)
	# authenticate via OAuth and post using Tumblr API - easy!
	if post_to_tumblr and pathway_string != search_term:
		if no_results:
				print '\n' + bold_start + 'skipping the Tumblr post...' + bold_end + '\n  could not find anything for that search :('
		else:
			print display_divider
			print '\n' + bold_start + 'posting results to Tumblr...' + bold_end

			# LOAD OAUTH DETAILS FROM FILE TO ACCESS TWITTER
			client = pytumblr.TumblrRestClient(
				settings['consumer_key'],
				settings['consumer_secret'],
				settings['access_token_key'],
				settings['access_token_secret']
			)

			response = client.create_text(blog_address, body=html_pathway_string)
			if 'id' in response:
				print '  post successful!'
				num_posted += 1
				if num_posted > max_posts:
					break
			else:
				print '  error uploading post, sorry... :('

	# PRINT RESULTING PATHWAY, THEN NEXT!
	print '\n' + bold_start + 'resulting pathway:' + bold_end + '\n' + pathway_string
	print '\n\n' + bold_start + 'DONE!' + bold_end
	print '\n' + display_divider + '\n'
	
# ALL DONE!
print '\nALL DONE! :)'

