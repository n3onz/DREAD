#all of the imports needed for this script
import os
import schedule
import time
import requests
from bs4 import BeautifulSoup

#main function for this updater
def updater():
    site = 'https://commoncrawl.org/the-data/get-started/' #main page for all Common Crawls

    #connects to Common Crawl website and pulls the text into a BS4 object
    r = requests.get(site)
    t = r.text
    soup = BeautifulSoup(t, features = 'html.parser')
    
    
    counter = 0
    new_link_spot = 0
    new_link = ''
    
    #Searches for AWS link which is first object below most updated CC and decrements by one to locate link to newest CC
    for link in soup.find_all('a'):
        if (link.get('href') == 'https://commoncrawl.s3.amazonaws.com/'):
            new_link_spot = counter - 1
        counter += 1
    
    new_link = soup.find_all('a')[new_link_spot]
    new_link = new_link.get('href') #gets the link from HTML for newest CC link
    
    updated = 1
    #Checks to see if our link is already the most up-to-date
    with open('ccLink.txt', 'r') as f:
        if (f.read() != new_link):
            updated = 0
    
    with open('ccLink.txt', 'w') as f:
        f.write(new_link)
        if (updated == 0):
            print('Updated CC link!')
        else:
            print('Link was already up to date!')
    if (updated == 0): 
        #Parses the up-to-date link and finds the download link to the .WET file we need
        soup2 = BeautifulSoup(requests.get(new_link).text, features = 'html.parser')
        dl_link = ''
        for link in soup2.find_all('a'):
            if 'wet.paths.gz' in link.get('href'):
                dl_link = link.get('href')
        
        #Downloads the file via wget to the system
        download = 'wget ' + dl_link
        os.system(download)

#Scheduled to check for updates everyday at 0600 system time
schedule.every().day.at("06:00").do(updater)

#Checks the time every 60 seconds to see if it is time to download
while True:
    schedule.run_pending()
    time.sleep(60)
