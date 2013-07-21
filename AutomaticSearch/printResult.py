
import json					# have to reimport since we're getting metadata separately :(
import requests

# A (somewhat detailed) function to print the result of a query; since
# it's a bit clunky in our regular code :)

# pass JSON dictionary
def printDetails(item):
	print 'Title:       ' + item['title']						# object title

	print 'Format:     ',														# what format is the object in
	for format in item['format']:
		print format + ',',
	print ''
	
	print 'Collection: ',														# which collection is the item in?
	for collection in item['collection']:
		print collection + ',',
	print ''
	
	# the URL for the listing
	print 'URL:         www.archive.org/details/' + item['identifier']


# get metadata (also try things like PPI, camera, etc)
def printMetadata(meta, identifier):
	print 'Media type:  ' + meta['metadata']['mediatype']	

	# get file URL
	print '\nFile URLs:'
	index = 0
	for file in meta['files']:
		format = file['format']
		url = 'http://archive.org/download/' + identifier + '/' + file['name']
		print "%02d" % index + ':          ' + file['format'] + ' (' + url + ')'
		index += 1
	print ''