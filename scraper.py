from bs4 import BeautifulSoup
import urllib.request as ur
from poll import Poll
from urllib.parse import urljoin
import datetime

def getPollInfo(i,base):
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

    for j in pollDetails:
        k = j.findAll("td")[1].contents[0].split(" ")[0]+"/18"
        tempDate= datetime.datetime.strptime(k,"%m/%d/%y")
        if(best==-1):
            best = j
            bestDate = tempDate
        elif(abs((tempDate-p.date).seconds)<abs((bestDate-p.date).seconds)):
            best = j
            bestDate = tempDate

    p.sample = best.findAll("td")[2].contents[0]

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

    tables = soup.findAll("table",{"class":"sortable"})
    polls = []
    for i in tables:
        races = i.findAll("tr")
        for j in races:
            if(j.find("td",{"class":"lp-race"})):  
                polls.append(j)

    pollList = []

    for i in polls:
        p = getPollInfo(i,base)
        pollList.append(p)

    return pollList

