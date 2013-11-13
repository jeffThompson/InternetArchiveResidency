
'''
DELETE EMPTY SEARCH FILES
Jeff Thompson | 2013 | www.jeffreythompson.org

A hack to delete unwanted search files that have no results.

'''

import os
os.system('cls' if os.name=='nt' else 'clear')

input_dir = 'SearchPathways_AllWords/'
files = os.listdir(input_dir)
blank_count = 0

for i, file in enumerate(files):
	with open(input_dir + file) as f:		# open file
		if '.DS_Store' in str(f):					# skip .DS_Store...
			continue
		line_count = 0
		for line in f:
			line_count += 1
		if line_count == 1:								# delete!
			print str(i+1) + '/' + str(len(files)) + ':' + '\t' + 'deleting "' + str(f.name) + '"...'
			os.remove(f.name)
			blank_count += 1

print '\n' + 'deleted ' + str(blank_count) + ' blank files...'
print 'ALL DONE!' + '\n\n\n'