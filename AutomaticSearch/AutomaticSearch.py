
import requests								# for making queries to archive.org
import json										# for parsing the results of our query
from printResult import *			# function for printing 

'''
AUTOMATIC SEARCH OF ARCHIVE.ORG
Jeff Thompson | 2013 | www.jeffreythompson.org

Automatically search and return metadata for items in Archive.org's vast
database of text, sound, and video.

Built for a Tumblr-based residency with Archive.org - thanks!

Search categories:
Most useful:			creator, description, subject, title
Possibly useful:	call_number, downloads, format, year

Media types (both capitalized and not - might need to test to see if this makes a difference)
Audio, image, other, text (also texts), video, audio, data, movies, software, web

More information on fancier queries of the Archive:
Searching:				http://archive.org/advancedsearch.php#raw
Getting metadata:	http://blog.archive.org/2013/07/04/metadata-api
More metadata:		http://blog.archive.org/2013/02/09/files-xml-and-metadata-api-now-showing-video-files-width-height-and-duration

Mass downloading:
Instructions:			http://blog.archive.org/2012/04/26/downloading-in-bulk-using-wget
Install wget:			http://osxdaily.com/2012/05/22/install-wget-mac-os-x
Possible error:		http://blog.salientdigital.com/2012/05/16/how-to-fix-no-acceptable-c-compiler-found-in-path-on-mac-os-x-lion

Very helpful resources on JSON/Python:
Basics of JSON:		http://docs.python.org/2/library/json.html
Using Requests:		http://www.python-requests.org/en/latest/user/quickstart
More Requests:		http://www.pythonforbeginners.com/python-on-the-web/using-requests-in-python
Other API stuff:	http://www.pythonforbeginners.com/python-on-the-web/how-to-access-various-web-services-in-python
Preview JSON:			http://jsoneditoronline.org

'''

searchTerm = 'hair'

searchField = 'description'			# what category to search in (try also: title, year, etc)
sortBy = 'year'									# how to order the results (can also be by rating, downloads, etc)
sortDirection = 'asc'						# asc or desc for ascending/descending
numItems = 10		 								# how many results to return
format = 'json'									# format for results

# try also limiting by mediatype:
mediatype = 'text'							# text, image, audio, video, software, etc


print '\n\nAUTOMATIC JSON SEARCH OF ARCHIVE.ORG'
print '[ retrieving first ' + str(numItems) + ' results... ]\n'

# submit data request
data = { 'q': searchField + ':' + searchTerm, 'sort': sortBy + '+' + sortDirection, 'rows': numItems, 'output': format, 'save': 'yes#raw' }
headers = { 'Content-type': 'application/json' }
response = requests.post('http://archive.org/advancedsearch.php', params=data, headers=headers)

# convert to dictionary (easier to parse)
searchResults = json.loads(response.text)

# print details (VERY hackable and extendable)
print 'Search URL:  ' + response.url + '\n'			# resulting search URL (can also be pasted into your browser)
print ('- ' * 36) + '\n'												# divider between listings

for item in searchResults['response']['docs']:		# iterate details
	printDetails(item)																# print using separate function to parse the resulting dict

	metadataRequest = requests.post('http://archive.org/metadata/' + item['identifier'])
	meta = json.loads(metadataRequest.text)
	printMetadata(meta, item['identifier'])
	
	# divider between listings
	print '- ' * 36 + '\n'

# done!

