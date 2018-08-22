from scraper import *
from geography import *
from poll import Poll

pollList = scrapePolls()

for i in pollList:
    print(i.state,i.votes)
