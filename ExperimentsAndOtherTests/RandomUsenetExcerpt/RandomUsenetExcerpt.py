'''
RANDOM USENET EXCERPT
Jeff Thompson | 2013 | www.jeffreythompson.org

Via:
- http://archive.org/details/usenet-com

Requires the Tumblr Python API:
https://github.com/tumblr/pytumblr

And requires the Python Oauth2 library, found here:
https://github.com/simplegeo/python-oauth2

TO DO:
+ Post any quotes directly to Twitter (ie start with ", not has a " inside tag)

'''

import pytumblr		# Tumblr API
import os					# for listing files in directory
import re					# data parsing
import shutil			# for moving uploaded folders
import json				# for parsing settings
import nltk.data
import random
import re

input_filename = 'com.priv.txt'
num_posts = 100
blog_address = 'jeff-thompson-iatr.tumblr.com'
punctuation = re.compile(r'[-.?!,":;()|0-9]')

print '\n\nAUTO POST TO TUMBLR'

# gather some random bits
# load file and extract sentences
print 'extracting sentences from text (may take a while)...'
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
file = open(input_filename)
data = file.read()
excerpts = tokenizer.tokenize(data)

# authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'xxxx',
  'xxxx',
  'xxxx',
  'xxxx'
)

print 'uploading posts...'
for i in range(num_posts):
	print '  ' + str(i+1) + '/' + str(num_posts) + ':',
	
	which = random.randrange(0, len(excerpts))
	
	text = excerpts[which]
	tags = []
	words = re.split('\s+', text.lower())
	for word in words:
		tags.append(punctuation.sub("", word))
	
	response = client.create_text(blog_address, body=text, tags=tags)
	if 'id' in response:
		print '  success!'
	else:
		print '  error uploading post, skipping...'
		# print response

print '\nALL DONE!\n\n'