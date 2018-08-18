from bs4 import BeautifulSoup, Comment
import urllib.request as ur

stateList = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
          'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
          'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
          'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
          'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
          'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
          'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
          'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
          'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
          'West Virginia', 'Wisconsin', 'Wyoming']
monthList = ["Jan","Feb","March","April","May","June","July","Aug","Sept","Nov","Dec"]

def findPollDates():
    sock = ur.urlopen("https://www.washingtonpost.com/graphics/2017/politics/2018-election-calendar/?noredirect=on&utm_term=.f8ee422d2339")
    soup = BeautifulSoup(sock,"html5lib")
    rows = soup.findAll("div",{"table-row"})

    for i in rows:
        electionName = i.find("span",{"class":"table-row--header-name"}).contents[0]
        comments = i.findAll(text=lambda text:isinstance(text, Comment))[0]
        electionDate = BeautifulSoup(comments,"html5lib").find("p",{"class":"election-note"}).contents[0]
        electionDate = electionDate.split(" ")[1:3]

        electionDate[0] = electionDate[0].replace(".","")
        electionDate[0] = monthList.index(electionDate[0])+1
        electionDate[1] = int(electionDate[1][:-2])

        electionDate = str(electionDate[0])+"/"+str(electionDate[1])
        
        print(electionName,electionDate)

findPollDates()
