from scraper import *
from geography import *
from poll import Poll

pollList = scrape2016()
races = {}
s = []

for i in pollList:
    candidates = list(i.votes.keys())
    if(candidates[0]+"_"+candidates[1] not in races):
        races[candidates[0]+"_"+candidates[1]] = []

    voteOne = int(i.results.split(", ")[0].split()[-1])
    voteTwo = int(i.results.split(", ")[1].split()[-1])
    races[candidates[0]+"_"+candidates[1]].append((i.date,voteOne,voteTwo,i.company))
    s.append(i.company)

for i in list(races.keys()):
    races[i] = sorted(races[i],key=lambda x: x[0],reverse=True)[0]
    
