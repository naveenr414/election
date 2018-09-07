from bs4 import BeautifulSoup, Comment
import urllib.request as ur
import datetime

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
monthLong = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def findPollDates():
    dateList = open("dates.txt").read().split("\n")[:-1]
    for i in range(len(dateList)):
        dateList[i] = dateList[i].split(" - ")
        stateName = dateList[i][0]
        stateDate = dateList[i][1]
        
        dateList[i][0] = stateName.strip()
        dateList[i][1] = datetime.datetime.strptime(stateDate,"%m/%d/%y")

    return dateList

def updatePollDates(): 
    sock = ur.urlopen("https://www.washingtonpost.com/graphics/2017/politics/2018-election-calendar/?noredirect=on&utm_term=.f8ee422d2339")
    soup = BeautifulSoup(sock,"html5lib")
    rows = soup.findAll("div",{"table-row"})

    w = open("dates.txt","w")

    for i in rows:
        electionName = i.find("span",{"class":"table-row--header-name"}).contents[0]

        #Find all comments
        comments = i.findAll(text=lambda text:isinstance(text, Comment))[0]
        electionDate = BeautifulSoup(comments,"html5lib").find("p",{"class":"election-note"}).contents[0]
        electionDate = electionDate.split(" ")[1:3]

        month = electionDate[0].replace(".","").strip()
        day = int(electionDate[1][:-2])
        month = monthList.index(month)+1
        electionDate = str(month)+"/"+str(day)+"/18"

        w.write(electionName)
        w.write(" - ")
        w.write(electionDate)
        w.write("\n")
        
    w.close()

