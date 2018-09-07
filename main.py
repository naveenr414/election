from scraper import *
from geography import *
from poll import Poll
import datetime

pollList = scrapePolls(year=2016)
races = {}
s = []

for i in pollList:
    candidates = list(i.votes.keys())
    if(candidates[0]+"_"+candidates[1] not in races):
        races[candidates[0]+"_"+candidates[1]] = []

    voteOne = int(i.results.split(", ")[0].split()[-1])
    voteTwo = int(i.results.split(", ")[1].split()[-1])
    races[candidates[0]+"_"+candidates[1]].append((voteOne,voteTwo,i.company,i.date))
    s.append(i.company)

for i in list(races.keys()):
    races[i] = sorted(races[i],key=lambda x: x[-1],reverse=True)[0]
    
w = open("2016races.csv","w")
columns = ["race","repScore","demScore","poller","daysTillElection"]
w.write(",".join(columns))
w.write("\n")

electionDate = datetime.datetime.strptime("11/8/16","%m/%d/%y")

for i in list(races.keys()):
    tempColumn = [i,races[i][0],races[i][1],races[i][2],abs(races[i][3]-electionDate).days]
    print(tempColumn)
