# entry.py
# Author: Marcus Jackson

# Class encapsulating a journal entry

import processing
from topic import Topic

class Entry(object):
	"""
	text -- a string containing the journal entry text
	tokenizedSentences -- a list of sentences as lists of tokens that make up the sentence
	topics -- a list of Topic objects
	"""

	def __init__(self, text, topicsMap):
		""""""
		self.text = text
		self.tokenizedSentences = processing.tokenize_text(text)
		self.tokenizedSentences = [processing.lowercase_arr(processing.stem_and_lemmatize_arr(arr))
			for arr in self.tokenizedSentences]
		self.topics = []
		for topicName in topicsMap:
			processedTopicList = [processing.lowercase_arr(processing.stem_and_lemmatize_arr(
				string.split(" "))) for string in topicsMap[topicName]]
			self.topics.append(Topic(topicName, processedTopicList, self.tokenizedSentences))
		matchTotal = sum([topic.numMatches for topic in self.topics])
		if (matchTotal == 0): matchTotal = 1
		self.topicPercentages = {topic.topicName: topic.numMatches * 1.0 / matchTotal for 
			topic in self.topics}

	def print_matches(self):
		for topic in self.topics:
			print(topic.topicName + ": " + str(topic.topicMatches))