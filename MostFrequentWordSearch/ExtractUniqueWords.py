
'''
EXTRACT UNIQUE WORDS
Jeff Thompson | 2013 | www.jeffreythompson.org

Counts all words in a given text, then outputs by
order of most- to least-frequent.

'''

from nltk.probability import FreqDist 			# for better text parsing
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk.data
import os																		# for clearing terminal window

input_filename = 'OldMortality.txt'
output_filename = 'OldMortality_500MostCommonWords.txt'
num_words = 500

# clear window
os.system('cls' if os.name=='nt' else 'clear')
print ''

# read text from file, format into one big string
print 'reading text from file...'
input = ''
with open(input_filename) as file:
	for line in file:
		input += line

# create list of most frequent words, list from most- to least-frequent
# taken from Tristan Havelick's 'summarize.py' (https://github.com/thavelick/summarize)
print 'counting word frequencies...'
tokenizer = RegexpTokenizer('\w+')
base_words = [ word.lower() for word in tokenizer.tokenize(input) ]
words = [ word for word in base_words if word not in stopwords.words() ]
word_frequencies = FreqDist(words)

# iterate words, save to file
print 'saving the result...\n'
with open(output_filename, 'a') as output:
	print '  INDEX' + (' ' * 5) + 'WORD' + (' ' * 11) + 'COUNT'
	for index, word in enumerate(word_frequencies.items()):
		if index > num_words:
			break
		print '  ' + str(index) + (' ' * (10 - len(str(index)))) + word[0] + (' ' * (15 - len(word[0]))) + str(word[1])
		output.write(word[0] + '\n')

print '\nALL DONE!' + ('\n' * 4)