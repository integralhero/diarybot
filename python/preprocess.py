import os.path
import glob
import numpy as np

path = "individuals"
filenames = [f for f in glob.glob(os.path.join(path, '2015*.txt'))]
documents = [open(f) for f in filenames]

stopWords = [word for word in ]

for doc in documents:
	for line in doc:
		 