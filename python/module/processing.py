# processing.py
# Author: Marcus Jackson

# Methods used in processing a entry text

import nltk
from collections import Counter
from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

"""Create a list of sentences from the text in the form of a list of token arrays"""
def tokenize_text(text):
	return [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]

"""Convert to lowercase each token in the given token array"""
def lowercase_arr(arr):
	return tuple([token.lower() for token in arr])

"""Stem and lemmatize each token in the given token array"""
def stem_and_lemmatize_arr(arr):
	stemmer = PorterStemmer()
	lmtzr = WordNetLemmatizer()
	return tuple([stemmer.stem(lmtzr.lemmatize(token)) for token in arr])
	# return [stemmer.stem((lmtzr.lemmatize(string))) for token in string.split(" ") for string in arr]
	# return [stemmer.stem((lmtzr.lemmatize(string))) for string in arr]
	# return [stemmer.stem((lmtzr.lemmatize(string))) for string in arr]
	# return [" ".join(tuple([string + "_" for string in tup])) for tup in arr]

# """Stem and lemmatize each token in the token array in the given list of arrays"""
# def stem_and_lemmatize_arrays(arrays):
# 	stemmer = PorterStemmer()
# 	lmtzr = WordNetLemmatizer()
# 	return [stemmer.stem((lmtzr.lemmatize(string))) for string in arr for arr in arrays]