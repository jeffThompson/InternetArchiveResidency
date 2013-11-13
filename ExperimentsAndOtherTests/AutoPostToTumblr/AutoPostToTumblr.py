'''
AUTO POST TO TUMBLR
Jeff Thompson | 2013 | www.jeffreythompson.org

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

blog_address = 'jeff-thompson-iatr.tumblr.com'
input_directory = 'ImagesToUpload/'
csv_file = 'brightness_sorted.csv'

print '\n\nAUTO POST TO TUMBLR\n'

id = []
brightness = []
url = []
images = []

gif_folders = os.listdir(input_directory)

# get data about each post
pattern = re.compile('\s*,\s*')
with open(csv_file) as csv:	
	for entry in csv:
		data = pattern.split(entry)
		id.append(data[0])
		brightness.append(data[1])
		url.append(data[2])
		
		if data[0] in gif_folders:
			for file in os.listdir(input_directory + data[0]):
				if file.endswith('.gif'):
					images.append(input_directory + data[0] + '/' + file)

# authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'xxxx',
  'xxxx',
  'xxxx',
  'xxxx'
)

for i in range(len(images)):
	print str(i) + ': ' + id[i]
	
	image = images[i]
	caption = url[i]
	caption = re.sub('>link<', '>' + id[i] + '<', caption)	# change from 'link' to the id
	tags = [ brightness[i] ]
	slug = id[i]
	
	response = client.create_photo(blog_address, data=image, caption=caption, tags=tags, slug=slug)
	if 'id' in response:
		print '  success!'
	else:
		print '  error uploading post, skipping...'
		# print response

print '\nALL DONE!\n\n'