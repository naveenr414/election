from bs4 import BeautifulSoup
import urllib.request as ur
from poll import Poll
from urllib.parse import urljoin
import datetime
from geography import monthLong 

def findPollDetails(baseURL,race):
    href = urljoin(baseURL,race.find("td",{"class":"lp-results"}).find("a")['href'])
    href = "http"+href.split("http")[-1]
    detailSoup = BeautifulSoup(ur.urlopen(href),"html.parser")
    pollDetails = detailSoup.findAll("tr")

    row = 0
    while(row<len(pollDetails)):
        if(not pollDetails[row].has_attr('data-id')):
            del pollDetails[row]
        else:
            row+=1

    return pollDetails


def getPollInfo(baseURL,race,date):
    p = Poll()
    
    p.title = race.find("td",{"class":"lp-race"}).find("a").contents[0]
    p.company = race.find("td",{"class":"lp-poll"}).find("a").contents[0]
    p.results = race.find("td",{"class":"lp-results"}).find("a").contents[0]
    p.spread = race.find("td",{"class":"lp-spread"}).find("span").contents[0]
    p.parseData()

    pollDetails = findPollDetails(baseURL,race)
    best = -1
    bestDate = -1
    p.date = date

    rep = ""
    dem = ""

    for row in pollDetails:
        swing = row.findAll("td")[-1].findAll("span")[0]
        party = swing.get("class")
        if(party):
            if(party[0]=="rep"):
                rep=" ".join(swing.contents[0].split(" ")[:-1]).lower()
            elif(party[0]=="dem"):
                dem = " ".join(swing.contents[0].split(" ")[:-1]).lower()
        
    if(rep):
        p.repName = rep
        if(p.candidates[0].lower()==rep):
            p.demName = p.candidates[1]
        else:
            p.demName = p.candidates[0]
    elif(dem):
        p.demName = dem
        if(p.candidates[0].lower()==dem):
            p.repName = p.candidates[1]
        else:
            p.repName = p.candidates[0]

    p.demName = p.demName.lower()
    p.repName = p.repName.lower()

    for i in list(p.votes.keys()):
        if(i.lower()==p.demName):
            p.demVotes = p.votes[i]
        elif(i.lower()==p.repName):
            p.repVotes = p.votes[i]

    for row in pollDetails:
        pollDate = row.findAll("td")[1].contents[0].split(" ")[0]+"/18"
        pollDate = datetime.datetime.strptime(pollDate,"%m/%d/%y")
        if(best==-1 or abs((pollDate-p.date).seconds)<abs((bestDate-p.date).seconds)):
            best = row
            bestDate = pollDate

    p.sample = best.findAll("td")[2].contents[0]
    p.electionDate = bestDate

    p.voterClass = p.sample.split(" ")[1]
    p.voterCount = p.sample.split(" ")[0]
    p.moe = float(best.findAll("td")[3].contents[0])

    return p

def scrapePolls(year=2018):
    base = ""
    if(year==2018):
        base = "https://www.realclearpolitics.com/epolls/latest_polls/senate/"
    elif(year==2016):
        base = "https://web.archive.org/web/20171025011101/https://www.realclearpolitics.com/epolls/latest_polls/senate/"

    sock = ur.urlopen(base)
    soup = BeautifulSoup(sock,"html.parser")

    tables = soup.findAll("table")
    raceInfo = []
    currentDate = ""
    date = ""
    for table in tables:
        #Bold means a new date that polls were conducted
        bolds = table.findAll("b")
        if(len(bolds)!=0):
            currentDate = bolds[0].contents[0].split(", ")[-1].split()
            currentDate[0] = monthLong.index(currentDate[0])+1
            currentDate[1] = int(currentDate[1])
            date = str(currentDate[0])+"/"+str(currentDate[1])+"/16"
            date = datetime.datetime.strptime(date,"%m/%d/%y")
        
        races = table.findAll("tr")
        for race in races:
            if(race.find("td",{"class":"lp-race"})):  
                raceInfo.append((race,date))

    pollList = []

    for race,date in raceInfo:
        poll = getPollInfo(base,race,date)
        pollList.append(poll)

    return pollList

