from bs4 import BeautifulSoup
import urllib.request as ur
from poll import Poll

def scrapePolls():
    sock = ur.urlopen("https://www.realclearpolitics.com/epolls/latest_polls/elections/")
    soup = BeautifulSoup(sock,"html5lib")

    tables = soup.findAll("table",{"class":"sortable"})
    polls = []
    for i in tables:
        races = i.findAll("tr")
        for j in races:
            if(j.find("td",{"class":"lp-race"})):  
                polls.append(j)

    pollList = []

    for i in polls:
        p = Poll()
        
        pollTitle = i.find("td",{"class":"lp-race"}).find("a").contents[0]
        pollCompany = i.find("td",{"class":"lp-poll"}).find("a").contents[0]
        pollResults = i.find("td",{"class":"lp-results"}).find("a").contents[0]
        pollSpread = i.find("td",{"class":"lp-spread"}).find("span").contents[0]

        if("-" in pollTitle):
            pollDetails = pollTitle.split("-")[1]
            pollTitle = pollTitle.split("-")[0].strip()
            p.details = pollDetails.strip()

        p.title = pollTitle
        p.company = pollCompany
        p.results = pollResults
        p.spread = pollSpread

        p.parseData()

        pollList.append(p)

    return pollList

