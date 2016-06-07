# settings.py
# All paths are based on the base folder

import os.path

# Folder for lexicons
FOLDER_LEXICON = 'lexicon'

# A file sectioned by topic keynames with a list of tokens for that topic
FILE_TOPICS = 'topics.txt'
PATH_TOPICS = os.path.join(FOLDER_LEXICON, FILE_TOPICS)

# A file sectioned by pronoun keynames with a list of tokens for that pronoun
FILE_PRONOUNS = 'pronouns.txt'
PATH_PRONOUNS = os.path.join(FOLDER_LEXICON, FILE_PRONOUNS)

#
FOLDER_DATA = 'data'
FOLDER_BY_DAY = 'by_day'
def get_entry_by_day(year, month, day):
	return os.path.join(FOLDER_DATA, FOLDER_BY_DAY, year + "-" + month + "-" + day + ".txt")

ENGLISH_STOP_WORDS = os.path.join(FOLDER_LEXICON, 'english.stop')