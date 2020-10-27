import sys
import csv

fields = []
rows = []

with open(sys.argv[1], 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    fields = next(csvreader)
    
    keywords = {}
    for row in csvreader:
        d = row[1:]
        if '' in d:
            index = d.index('')
            d = d[0:index]
        keywords[row[0]] = d
print(keywords)
