from bs4 import BeautifulSoup
import urllib.request as ur
from poll import Poll

sock = ur.urlopen("https://www.realclearpolitics.com/epolls/latest_polls/")
soup = BeautifulSoup(sock,"html5lib")

polls = soup.findAll("tr",{"class":"alt"})
pollList = []

for i in polls:
    p = Poll()
    
    pollTitle = i.find("td",{"class":"lp-race"}).find("a").contents[0]
    pollCompany = i.find("td",{"class":"lp-poll"}).find("a").contents[0]
    pollResults = i.find("td",{"class":"lp-results"}).find("a").contents[0]
    pollSpread = i.find("td",{"class":"lp-spread"}).find("span").contents[0]

    p.title = pollTitle
    p.company = pollCompany
    p.results = pollResults
    p.spread = pollSpread

    pollList.append(p)

for i in pollList:
    print(i)
