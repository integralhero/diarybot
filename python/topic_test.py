import nltk
import os.path
import glob
import re
import sys
sys.path.insert(0, "code")
import misc
from collections import Counter
from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# path = "individuals"
# filenames = [f for f in glob.glob(os.path.join(path, '2015*.txt'))]
# documents = [open(f) for f in filenames]

def stemAndLemmat():
	with open(os.path.join('individuals', '2015-01-14.txt'), 'r') as f:
	    sample = f.read()
	    sample = unicode(sample, 'utf8')
	     
	sentences = nltk.sent_tokenize(sample)
	tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

	porter_stemmer = PorterStemmer()
	lmtzr = WordNetLemmatizer()

	result = []
	for sent in tokenized_sentences:
		newSent = []
		for token in sent:
			newToken = porter_stemmer.stem((lmtzr.lemmatize(token)))
			# if (token != newToken): print(token + "   " + newToken)
			newSent.append(newToken)
		result.append(newSent)
	return result

def stemAndLemmatArr(arr):
	porter_stemmer = PorterStemmer()
	lmtzr = WordNetLemmatizer()

	result = []
	for token in arr:
		newToken = porter_stemmer.stem((lmtzr.lemmatize(token)))
		# if (token != newToken): print(token + "   " + newToken)
		result.append(newToken)
	return result

def tallyTopics(listOfSents, topicsDict):
	result = defaultdict(lambda: Counter())
	for sent in listOfSents:
		for token in sent:
			for key in topicsDict:
				for word in topicsDict[key]:
					if token == word: result[key][word] += 1
	return result


sample = stemAndLemmat()
topicsDict = misc.load_dict("general_topics.txt")
for key in topicsDict:
	topicsDict[key] = stemAndLemmatArr(topicsDict[key])
result = tallyTopics(sample, topicsDict)
totals = Counter()

for key in result:
	counts = result[key]
	print(key + ": ")
	for word in counts:
		totals[key] += result[key][word]
		print("   " + word + ": " + str(result[key][word]))



for key in totals:
	print(key + ": " + str(totals[key]))
