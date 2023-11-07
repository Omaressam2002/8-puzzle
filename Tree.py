from State import state
class tree:
    def __init__(self,root:state):
        self.root = root
    def traverseTree(self,root:state,cost=False):
        if not root:
            return
        else :
            for child in root.children:
                self.traverseTree(child)
            print(root.level)
            root.printState()
