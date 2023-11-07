class state:
    def __init__(self,state):
        self.level = 0
        self.state = list(state)
        self.parent = None
        self.children = []
        self.cost = None
    def setParent(self,parent):
        self.parent = parent
        self.parent.children.append(self)
        self.level = self.parent.level + 1
    def printState(self):
        for i in range(3):
            ithrow = self.state[(3*i):(3*(i+1))]
            print(ithrow)
    def toString(self):
        return ''.join(self.state)