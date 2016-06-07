import os.path
import glob
import re

path = 'journals'
pattern = re.compile('([A-Z][a-z]+day) ([0-9]{1,2}) ([A-Z][a-z]+) ([0-9]{4})')
months = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", 
	"July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12"}

for filename in glob.glob(os.path.join(path, '*.txt')):
	f = open(filename, 'r')
	for line in f:
		match = pattern.search(line)
		break
	# dayOfWeek, dayNumber, month, year = match.group(1, 2, 3, 4)
	
	while(True):
		broke = False
		dateTuple = match.group(1, 2, 3, 4)
		dayNumber = dateTuple[1]
		if len(dayNumber) == 1: dayNumber = "0" + dayNumber
		writeTo = open(os.path.join("individuals", dateTuple[3] + "-" 
			+ months[dateTuple[2]] + "-" + dayNumber + '.txt'), 'w')
		writeTo.write(line)

		for line in f:
			match = pattern.search(line)
			if not match:
				if (line.strip() != ''): writeTo.write(line)
			else:
				broke = True
				writeTo.close()
				break
		if not broke: break