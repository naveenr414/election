from bs4 import BeautifulSoup
import urllib.request as ur
from poll import Poll
from urllib.parse import urljoin

def scrapePolls():
    base = "https://www.realclearpolitics.com/epolls/latest_polls/elections/"
    sock = ur.urlopen(base)
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

        href = urljoin(base,i.find("td",{"class":"lp-results"}).find("a")['href'])
        detailSoup = BeautifulSoup(ur.urlopen(href),"html5lib")
        pollDetails = detailSoup.findAll("tr")

        l = []
        for j in pollDetails:
            if(j.has_attr('data-id')):
                l.append(j)
        pollDetails = l

        for j in pollDetails:
            k = j.find("td",{"class":"noCenter"}).find("a",{"class":"normal_pollster_name"}).contents
            print(pollTitle,k)

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

