#all of the imports required for this script
import requests
import csv
import sys
from bs4 import BeautifulSoup
import datetime
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
nlp = English()

#pulls in the list of websites from CSV
websites = [x.strip('\n') for x in open(sys.argv[1],'r').read().split(',')]
products = []

#Creates dictionary of keywords for CSV
fields = []
rows = []
with open(sys.argv[2], 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    fields = next(csvreader)

    keywords = {}

    for row in csvreader:
        d = row
        if '' in d: #removes trailing white space
            index = d.index('')
            d = d[0:index]
        k = [x.lower() for x in d] #sets all of dictionary values to be lowercase
        keywords[row[0]] = k

#Establishes TOR Proxy
session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

#For all websites it connects via requests and parses for title, status code, and notes the date/time of when this occurs
#Appends above to output list
for site in websites:
    r = session.get(site)
    t = r.text
    soup = BeautifulSoup(t, features = "html.parser")
    title = soup.title.string #Gets title from HTML
    #Gets text from HTML and tokenizes text removing stop words, punctuation, white-space, and duplicate words
    page_text = soup.get_text()
    doc = nlp(page_text)
    token_list = []
    for token in doc:
        if (token.is_ascii == True and token.is_stop == False and token.is_punct == False and token.is_space == False):
            if (token.text not in token_list):
                token_list.append(token.text)
    #Gets status code and datetime
    sc = r.status_code
    dt = datetime.datetime.now()
    #Parses tokens for keywords
    categories = []
    for cats in keywords:
        for i in token_list:
            if i.lower() in keywords.get(cats):
                if (cats not in categories):
                    categories.append(cats)

    products.append('{}:{}:{}:{}:{}\n'.format(site,sc,title,categories,dt))

out = ','.join(products)+'\n'

#Writes output to our CSV for use in our database
with open('statusCodes.csv', 'w') as f:
    f.write(out)
