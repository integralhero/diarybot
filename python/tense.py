from nltk import word_tokenize, pos_tag
import sys
sys.path.insert(0, "module")
import settings
import loaddata as ld
import processing
# import operator

def determine_tense_input(text):
    text = word_tokenize(text)
    tagged = pos_tag(text)

    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    return(tense)

if __name__ == '__main__': 
	# print(get_topic(ld.load_entry_text(settings.get_entry_by_day("2015", "01", "25"))))
	if (len(sys.argv) == 4):
		text = ld.load_entry_text(settings.get_entry_by_day(sys.argv[1], sys.argv[2], 
				sys.argv[3]))
	else:
		print("Must be 3 arguments: year, month, day")
		exit(1)

	sentences = processing.tokenize_text(text)
	for sentence in sentences:
		print(sentence)
		tense = determine_tense_input(sentence)
		# predicted = max(tense.iteritems(), key=operator.itemgetter(1))[0]
		print("   " + str(tense))
		print ""