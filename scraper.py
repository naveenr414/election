from bs4 import BeautifulSoup
import urllib.request as ur
from poll import Poll
from urllib.parse import urljoin
import datetime

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def getPollInfo(i,base,d):
    p = Poll()
    
    pollTitle = i.find("td",{"class":"lp-race"}).find("a").contents[0]
    pollCompany = i.find("td",{"class":"lp-poll"}).find("a").contents[0]
    pollResults = i.find("td",{"class":"lp-results"}).find("a").contents[0]
    pollSpread = i.find("td",{"class":"lp-spread"}).find("span").contents[0]

    href = urljoin(base,i.find("td",{"class":"lp-results"}).find("a")['href'])
    href = "http"+href.split("http")[-1]
    detailSoup = BeautifulSoup(ur.urlopen(href),"html.parser")
    pollDetails = detailSoup.findAll("tr")

    l = []
    for j in pollDetails:
        if(j.has_attr('data-id')):
            l.append(j)
    pollDetails = l

    p.title = pollTitle
    p.company = pollCompany
    p.results = pollResults
    p.spread = pollSpread
    p.parseData()

    best = -1
    bestDate = -1
    p.date = d

    rep = ""
    dem = ""

    for j in pollDetails:
        sp = j.findAll("td")[-1].findAll("span")[0]
        political = sp.get("class")
        if(political):
            if(political[0]=="rep"):
                rep=" ".join(sp.contents[0].split(" ")[:-1]).lower()
            elif(political[0]=="dem"):
                dem = " ".join(sp.contents[0].split(" ")[:-1]).lower()
        k = j.findAll("td")[1].contents[0].split(" ")[0]+"/18"
        tempDate= datetime.datetime.strptime(k,"%m/%d/%y")
        if(best==-1):
            best = j
            bestDate = tempDate
        elif(abs((tempDate-p.date).seconds)<abs((bestDate-p.date).seconds)):
            best = j
            bestDate = tempDate

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

    print(p.demName,p.demVotes,p.repName,p.repVotes)

    p.sample = best.findAll("td")[2].contents[0]
    p.electionDate = bestDate

    p.voterClass = p.sample.split(" ")[1]
    p.voterCount = p.sample.split(" ")[0]
    p.moe = float(best.findAll("td")[3].contents[0])


    if("-" in pollTitle):
        pollDetails = pollTitle.split("-")[1]
        pollTitle = pollTitle.split("-")[0].strip()
        p.details = pollDetails.strip()

    return p

def scrapePolls():
    base = "https://www.realclearpolitics.com/epolls/latest_polls/elections/"
    sock = ur.urlopen(base)
    soup = BeautifulSoup(sock,"html.parser")

    tables = soup.findAll("table",{"class":"sortable"})
    polls = []
    for i in tables:
        races = i.findAll("tr")
        for j in races:
            if(j.find("td",{"class":"lp-race"})):  
                polls.append(j)

    pollList = []

    for i in polls:
        p = getPollInfo(i)
        pollList.append(p)

    return pollList

def scrape2016():
    base = "https://web.archive.org/web/20171025011101/https://www.realclearpolitics.com/epolls/latest_polls/senate/"
    sock = ur.urlopen(base)
    soup = BeautifulSoup(sock,"html.parser")

    tables = soup.findAll("table")
    polls = []
    currentDate = ""
    d = 0
    for i in tables:
        bolds = i.findAll("b")
        if(len(bolds)!=0):
            currentDate = bolds[0].contents[0].split(", ")[-1].split()
            currentDate[0] = months.index(currentDate[0])+1
            currentDate[1] = int(currentDate[1])
            d = str(currentDate[0])+"/"+str(currentDate[1])+"/16"
            d = datetime.datetime.strptime(d,"%m/%d/%y")
        races = i.findAll("tr")
        for j in races:
            if(j.find("td",{"class":"lp-race"})):  
                polls.append((j,d))

    pollList = []

    for i,d in polls:
        p = getPollInfo(i,base,d)
        pollList.append(p)

    return pollList

