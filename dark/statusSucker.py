#all of the imports required for this script
import requests
import sys
from bs4 import BeautifulSoup
import datetime

#pulls in the list of websites from CSV
websites = [x.strip('\n') for x in open(sys.argv[1],'r').read().split(',')]
products = []

#For all websites it connects via requests and parses for title, status code, and notes the date/time of when this occurs
#Appends above to output list
for site in websites:
    r = requests.get(site)
    t = r.text
    soup = BeautifulSoup(t, features = "html.parser")
    title = soup.title.string
    page_text = soup.get_text()
    sc = r.status_code
    dt = datetime.datetime.now()
    products.append('{}:{}:{}:{}\n'.format(site,sc,title,dt))

out = ','.join(products)+'\n'

#Writes output to our CSV for use in our database
with open('statusCodes.csv', 'w') as f:
    f.write(out)
