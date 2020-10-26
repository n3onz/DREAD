# Crawl Parsing
Our project utilizes the Common Crawl, a plain text mapping of the clear web to find .onion sites for our database.

## Checking For Common Crawl Updates
The Common Crawl releases updated crawls with relative frequency. We use our ccupdater.py script to run in the background and check once daily to see if the Common Crawl we updated, and downloads the updated Common Crawl to aquamentus. It is scheduled to check every day at 0600.

## Parsing the Common Crawl
Our Common Crawl parser takes the Common Crawl .WET file and checks for .onion addresses using regular expressions. It outputs a .CSV with all of the .onion addresses that it found.
