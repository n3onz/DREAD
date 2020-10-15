import requests
import sys

websites = [x.strip('\n') for x in open(sys.argv[1],'r').read().split(',')]

products = []

for site in websites:
    r = requests.get(site)
    sc = r.status_code
    products.append('{}:{}'.format(site,sc))

out = ','.join(products)+'\n'

with open('statusCodes.csv', 'w') as f:
    f.write(out)

