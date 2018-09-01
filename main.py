from scraper import *
from geography import *
from poll import Poll

pollList = scrape2016()

for i in pollList:
    print(i.state,i.votes)
