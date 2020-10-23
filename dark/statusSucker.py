import requests
import sys
from bs4 import BeautifulSoup
import datetime

websites = [x.strip('\n') for x in open(sys.argv[1],'r').read().split(',')]

products = []

for site in websites:
    r = requests.get(site)
    t = r.text
    soup = BeautifulSoup(t, features = "html.parser")
    title = soup.title.string
    sc = r.status_code
    dt = datetime.datetime.now()
    products.append('{}:{}:{}:{}'.format(site,sc,title,dt))

out = ','.join(products)+'\n'

with open('statusCodes.csv', 'w') as f:
    f.write(out)
