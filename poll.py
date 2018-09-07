import geography
import datetime

class Poll:
    def __init__(self):
        self.title = ""
        self.company = ""
        self.spread = ""
        self.details = ""
        self.results = ""

    def parseData(self):
        #Figure out if its a state ballot
        self.state = ""
        self.electionType = ""
        self.party = ""

        oneWord = self.title.split()[0]
        twoWord = " ".join(self.title.split()[0:2])

        if(oneWord in geography.stateList):
            self.state = oneWord
        elif(twoWord in geography.stateList):
            self.state = twoWord

        if(self.state!=""):
            self.electionType = self.title.replace(self.state+" ","")

        dates = geography.findPollDates()
        self.date = datetime.datetime.strptime("11/6/18","%m/%d/%y")
        for i in dates:
            if self.title.lower() in i[0].lower():
                self.date = i[1]

        results = self.results.split(", ")
        self.candidates = []
        self.votes = {}
        for i in results:
            num = 0
            if(len(i.split())>1):
                num = int(i.split()[-1])

            name = " ".join(i.split()[:-1])
            if(len(i.split())==1):
                name = i
    
            self.candidates.append(name)
            self.votes[name] = num
            
        if("-" in self.title):
            pollDetails = self.title.split("-")[1]
            self.title = self.title.split("-")[0].strip()
            self.details = pollDetails.strip()


    def __str__(self):
        return self.title+" by "+self.company + " predicted "+self.spread
