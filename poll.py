import geography

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
    
        for state in geography.stateList:
            if state in self.title:
                self.state = state
                self.electionType = self.title.replace(self.state+" ","")
                break

    def __str__(self):
        return self.title+" by "+self.company + " predicted "+self.spread
