# summarization.py
# Author: Marcus Jackson

import os
os.chdir(".\python")
import sys
sys.path.insert(0, "module")
import loaddata as ld
import settings
import entry
import processing
from collections import Counter

"""Return a tuple of # of words in text and dictionary of entity to # of appearances in text"""
def get_statistics(text):
	return

"""Return dictionary of topic keyword to percentage in text"""
def get_topic(text, topicsMap = None):
	if not topicsMap: topicsMap = ld.load_keyname_sectioned_text(settings.PATH_TOPICS)
	entryObj = entry.Entry(text, topicsMap)
	entryObj.print_matches()
	return entryObj.topicPercentages
	# return entry.Entry(text, topicsMap).topicPercentages

def get_pronoun_usage(text, topicsMap = None):
	if not topicsMap: topicsMap = ld.load_keyname_sectioned_text(settings.PATH_PRONOUNS)
	entryObj = entry.Entry(text, topicsMap)
	# entryObj.print_matches()
	return entryObj.topicPercentages

def get_most_common_words(text, N):
	stopWords = ld.load_simple_set(settings.ENGLISH_STOP_WORDS)
	result = Counter()
	tokenized_t = processing.tokenize_text(text);
	for sent in tokenized_t:
		for token in sent:
			result[token.lower().replace(u"\u2019", "'")] += 1
	result = [(key, value) for key, value in sorted(result.iteritems(), key=lambda (k,v): (v,k), reverse=True)]
	newResult = []
	for tup in result:
		if tup[0] not in stopWords and tup[0]:
			newResult.append(tup)
	return newResult[0:N]

def print_dictionary(dict):
	for key in dict: print str(key) + "\t" + str(dict[key])

if __name__ == '__main__': 
	# print(get_topic(ld.load_entry_text(settings.get_entry_by_day("2015", "01", "25"))))
	if (len(sys.argv) == 3 or len(sys.argv) == 4):
		if (sys.argv[1] == "topic"):
			print_dictionary(get_topic(sys.argv[2]))
		elif (sys.argv[1] == "pronoun"):
			print_dictionary(get_pronoun_usage(sys.argv[2]))
		elif (sys.argv[1] == "common"):
			print(get_most_common_words(sys.argv[2], int(sys.argv[3])))
		else:
			print ("summary_type must be valid")
	else:
		print("Must be 4 arguments: summary_type, text")

# if __name__ == '__main__': 
# 	# print(get_topic(ld.load_entry_text(settings.get_entry_by_day("2015", "01", "25"))))
# 	if (len(sys.argv) == 5 or len(sys.argv) == 6):
# 		if (sys.argv[1] == "topic"):
# 			print(get_topic(ld.load_entry_text(settings.get_entry_by_day(sys.argv[2], sys.argv[3], 
# 				sys.argv[4]))))
# 		elif (sys.argv[1] == "pronoun"):
# 			print(get_pronoun_usage(ld.load_entry_text(settings.get_entry_by_day(sys.argv[2], sys.argv[3], 
# 				sys.argv[4]))))
# 		elif (sys.argv[1] == "common"):
# 			print(get_most_common_words(ld.load_entry_text(settings.get_entry_by_day(sys.argv[2], sys.argv[3],
# 				sys.argv[4])), int(sys.argv[5])))
# 		else:
# 			print ("summary_type must be valid")
# 	else:
# 		print("Must be 4 arguments: summary_type, year, month, day")