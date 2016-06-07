# loaddata.py
# Author: Marcus Jackson
# 
# Methods for loading data specific to this project

import io
from collections import defaultdict

"""Open the keyname sectioned file and return dictionary of keyname to keyname's list of strings"""
def load_keyname_sectioned_text(file_name):
	with open(file_name, 'r') as f:
		result = {}

		# Handles section by section of the file
		while(True):
			# First line of each section is a keyname
			keyName = f.readline().rstrip('\n')
			if keyName == "": break # if gets empty string, then has reached end of file
			words = []

			# Reads in each string for that keyname
			while(True):
				line = f.readline().rstrip('\n')
				# If gets empty string, reached end of section
				if line == "": break
				# line = tuple(line.split())
				words.append(line)
			# Removes any duplicates
			result[keyName] = list(set(words))
		return result

def load_entry_text(file_name):
	with io.open(file_name, 'r', encoding='utf8') as f:
		return f.read()

def load_simple_set(file_name):
	with open(file_name, 'r') as f:
		result = []
		for line in f:
			result.append(line.rstrip('\n'))
		return set(result)

def load_tab_separated_list(file_name):
	with io.open(file_name, 'r', encoding='utf8') as f:
		result = defaultdict(lambda: [])
		for line in f:
			keyValue = line.rstrip('\n').replace("_", " ").split('\t')
			result[keyValue[1]].append(keyValue[0])
		return dict(result)