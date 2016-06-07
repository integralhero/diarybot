import nltk
import os.path
import glob
import re

with open(os.path.join('individuals', '2015-01-14.txt'), 'r') as f:
    sample = f.read()
    sample = unicode(sample, 'utf8')
     
sentences = nltk.sent_tokenize(sample)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
chunked_sentences = nltk.ne_chunk_sents(tagged_sentences)

chunk_types=['LOCATION', 'ORGANIZATION', 'PERSON', 'DURATION', 'DATE', 'CARDINAL', 'PERCENT', 
	'MONEY', 'MEASURE', 'TIME', 'FACILITY', 'GPE']

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() != 'S':
            entity_names.append((t.label(), ' '.join([child[0] for child in t])))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

entity_names = []
for tree in chunked_sentences:
    # Print results per sentence
    # print extract_entity_names(tree)

    entity_names.extend(extract_entity_names(tree))

# Print all entity names
#print entity_names

# Print unique entity names
set(entity_names)
for entity, value in set(entity_names):
	if (entity == "PERSON"): print entity + ": " + value