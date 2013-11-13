from nltk.probability import FreqDist 			# for better text parsing
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk.data

input_filename = 'mrt2w10.txt'

print 'loading text from file...'
input = ''
with open(input_filename) as file:
	for line in file:
		input += line

print 'extracting unique words (may take a while)...'
tokenizer = RegexpTokenizer('\w+')
base_words = [ word.lower() for word in tokenizer.tokenize(input) ]
words = [ word for word in base_words if word not in stopwords.words() ]
word_frequencies = FreqDist(words)

for word in word_frequencies:
	print word