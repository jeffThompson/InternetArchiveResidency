
import json
import requests

# A (somewhat detailed) function to print the result of a query; since
# it's a bit clunky in our regular code :)

# pass JSON dictionary
def printResult(searchResults):

	for item in searchResults['response']['docs']:		# iterate details
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
		metadataRequest = requests.post('http://archive.org/metadata/' + item['identifier'])
		meta = json.loads(metadataRequest.text)
		print 'Media type:  ' + meta['metadata']['mediatype']	

		# get file URL
		print '\nFile URLs:'
		index = 0
		for file in meta['files']:
			format = file['format']
			url = 'http://archive.org/download/' + item['identifier'] + '/' + file['name']
			print str(index) + ':           ' + file['format'] + ' (' + url + ')'
			index += 1
		print ''
	
		# divider between listings
		print '- ' * 36
	
	# done!
	print ''