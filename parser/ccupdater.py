import os
import schedule
import time
import requests
from bs4 import BeautifulSoup

def updater():
    site = 'https://commoncrawl.org/the-data/get-started/'

    r = requests.get(site)
    t = r.text
    soup = BeautifulSoup(t, features = 'html.parser')
    
    
    counter = 0
    new_link_spot = 0
    new_link = ''
    
    for link in soup.find_all('a'):
        if (link.get('href') == 'https://commoncrawl.s3.amazonaws.com/'):
            new_link_spot = counter - 1
        counter += 1
    
    new_link = soup.find_all('a')[new_link_spot]
    new_link = new_link.get('href')
    
    updated = 1
    with open('ccLink.txt', 'r') as f:
        if (f.read() != new_link):
            updated = 0
    
    with open('ccLink.txt', 'w') as f:
        f.write(new_link)
        if (updated == 0):
            print('Updated CC link!')
        else:
            print('Link was already up to date!')
    
    soup2 = BeautifulSoup(requests.get(new_link).text, features = 'html.parser')
    
    dl_link = ''
    for link in soup2.find_all('a'):
        if 'wet.paths.gz' in link.get('href'):
            dl_link = link.get('href')
    
    download = 'wget ' + dl_link
    print(download)
    os.system(download)

schedule.every().day.at("06:00").do(updater)

while True:
    schedule.run_pending()
    time.sleep(60)

