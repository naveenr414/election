class Poll:
    def __init__(self):
        self.title = ""
        self.company = ""
        self.results = ""
        self.spread = ""

    def __str__(self):
        return self.title+" by "+self.company + " predicted "+self.spread
