
import json
import requests
from printResult import *			# function for printing 

'''
AUTOMATIC SEARCH OF ARCHIVE.ORG
Jeff Thompson | 2013 | www.jeffreythompson.org

Automatically search and return metadata for items in Archive.org's vast
database of text, sound, and video.

Built for a Tumblr-based residency with Archive.org - thanks!

Search fields:
creator, description, subject, title
call_number, downloads, format, year

More information on fancier queries of the Archive:
http://archive.org/advancedsearch.php#raw

Accessing metadata from Archive.org:
http://blog.archive.org/2013/07/04/metadata-api
http://blog.archive.org/2013/02/09/files-xml-and-metadata-api-now-showing-video-files-width-height-and-duration

Mass downloading:
http://blog.archive.org/2012/04/26/downloading-in-bulk-using-wget
http://osxdaily.com/2012/05/22/install-wget-mac-os-x
http://blog.salientdigital.com/2012/05/16/how-to-fix-no-acceptable-c-compiler-found-in-path-on-mac-os-x-lion

Very helpful resources on JSON/Python:
http://docs.python.org/2/library/json.html
http://www.python-requests.org/en/latest/user/quickstart
http://www.pythonforbeginners.com/python-on-the-web/using-requests-in-python
http://www.pythonforbeginners.com/python-on-the-web/how-to-access-various-web-services-in-python
http://jsoneditoronline.org

'''

searchTerm = 'marzipan'

searchField = 'description'			# what category to search in
sortBy = 'createdate'						# how to order the results
sortDirection = 'asc'						# asc or desc for ascending/descending
numItems = 1										# how many results to return
format = 'json'									# format for results

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
printResult(searchResults)											# print using separate function to parse the resulting dict
