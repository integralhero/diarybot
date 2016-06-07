import os.path
import glob
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def fun(a,N):
    return np.argsort(a)[::-1][:N]

path = "individuals"
filenames = [f for f in glob.glob(os.path.join(path, '2015*.txt'))]
documents = [open(f) for f in filenames]
tfidf = TfidfVectorizer(input="file").fit_transform(documents)
for doc in documents:
    doc.close()


documents = [open(f) for f in filenames]
charLengths = [len(f.read().decode('utf8')) for f in documents]
for doc in documents:
    doc.close()


documents = [open(f) for f in filenames]
wordLengths = [0 for f in filenames]
for index, doc in enumerate(documents):
    for line in doc:
        words = line.split()
        wordLengths[index] += len(words)
    doc.close()


pairsim = tfidf * tfidf.T
arr = pairsim.A

numDocs = len(filenames)

scores = [0.0 for i in xrange(numDocs)]
nums = list(reversed(xrange(numDocs)))
for i in xrange(numDocs):
    for index, value in enumerate(fun(arr[i], numDocs)):
        scores[value] += nums[index]

