# topics.py
# Author: Marcus Jackson

# Class for handling determining the topic composition of a journal entry

from collections import Counter

class Topic(object):
	"""
	topicName -- keyname for the topic
	topicList -- list of tuples of stemmed and lemmatized tokens that go with this topic keyname
	tokenizedSentences -- sentences of the entry as list of list of tokens
	topicMatches -- a map from topic string to a count of times it was matched
	numMatches -- the # of matches that were made for this topic with the entry
	"""

	def __init__(self, topicName, topicList, tokenizedSentences):
		self.topicName = topicName
		self.topicList = topicList
		self.tokenizedSentences = tokenizedSentences
		self.topicMatches = Counter()
		for sentence in tokenizedSentences:
			self._count_matches(sentence)
		self.numMatches = sum(self.topicMatches.values())


	"""Helper: Count # of matches between the given sentence and strings for this topic"""
	def _count_matches(self, sentence):
		topicList = self.topicList
		topicMatches = self.topicMatches
		for tup in topicList:
			numWords = len(tup)
			for index in xrange(0, len(sentence) - (numWords - 1)):
				tokens = tuple(sentence[index : index + numWords])
				if tokens == tup: topicMatches[tup] += 1
		self.topicMatches = topicMatches