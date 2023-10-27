from queue import PriorityQueue

class Tiles:
    def __init__(self,indx,value):
        self.indx = int(indx)
        self.value = int(value)
        self.row = self.indx//3
        self.col = self.indx%3
        self.position = (self.row,self.col)


class state:
    def __init__(self,state):    
        self.state = list(state)
        self.parent = None
        self.children = []
        self.depth = 0
    def setParent(self,parent):
        self.parent = parent
        self.parent.children.append(self)
        self.depth+=1
    def printState(self):
        for i in range(3):
            ithrow = self.state[(3*i):(3*(i+1))]
            print(ithrow)
    def toString(self):
        print(''.join(self.state))

    def __lt__(self,other):
        return self.state < other.state
    

def manhattan_distance(state:state,goal:state):
    tiles_start = [Tiles(i,state.state[i]) for i in range(9)]
    tiles_end = [Tiles(i,goal.state[i]) for i in range(9)]

    tiles_start.sort(key=lambda x:x.value)
    tiles_end.sort(key=lambda x:x.value)

    tot_distance = 0
    for i in range(9):
        distance = abs(tiles_start[i].position[0] - tiles_end[i].position[0]) + abs(tiles_start[i].position[1] - tiles_end[i].position[1])
        tot_distance += distance

    return tot_distance

def euclidean_distance(state:state,goal:state):
    tiles_start = [Tiles(i,state.state[i]) for i in range(9)]
    tiles_end = [Tiles(i,goal.state[i]) for i in range(9)]

    tiles_start.sort(key=lambda x:x.value)
    tiles_end.sort(key=lambda x:x.value)

    tot_distance = 0
    for i in range(9):
        distance = ((tiles_start[i].position[0] - tiles_end[i].position[0])**2 + (tiles_start[i].position[1] - tiles_end[i].position[1])**2)**0.5
        tot_distance += distance

    return tot_distance

def traverse(state:state,steps=0):
    if state != None:
        steps+=1
        traverse(state.parent,steps)
        steps-=1
        print(steps)
        state.printState()
    else:
        print(steps-1)
        return 
    
def AStar(start_state:state , goal_state:state,heuristic_fn):
    frontier = PriorityQueue()
    frontier.put((0,start_state))
    explored = []
    depth = 0

    if start_state.state == goal_state.state:
        return start_state

    while not frontier.empty():
        _,parent_state = frontier.get()        
        explored.append(parent_state)
        blank_index = parent_state.state.index("0")
        blank_row = blank_index//3
        blank_col = blank_index%3
        depth+=1
        children = []
        
        if blank_col+1 <= 2:                        
            child = state(parent_state.state)
            child.state[blank_index],child.state[blank_index+1] = child.state[blank_index+1],child.state[blank_index]
            if child.state == goal_state.state:
                child.setParent(parent_state)
                return child
            children.append(child)        

        if blank_col-1 >= 0:
            child = state(parent_state.state)
            child.state[blank_index],child.state[blank_index-1] = child.state[blank_index-1],child.state[blank_index]                        
            if child.state == goal_state.state:                
                child.setParent(parent_state)
                return child
            children.append(child)

        if blank_row+1 <= 2:
            child = state(parent_state.state)
            child.state[blank_index],child.state[blank_index+3] = child.state[blank_index+3],child.state[blank_index]
            if child.state == goal_state.state:
                child.setParent(parent_state)
                return child
            
            children.append(child)

        if blank_row-1 >= 0:
            child = state(parent_state.state)
            child.state[blank_index],child.state[blank_index-3] = child.state[blank_index-3],child.state[blank_index]
            if child.state == goal_state.state:
                child.setParent(parent_state)
                return child
            children.append(child)

        
        for child in children:
            if not (child.state in explored):
                cost = heuristic_fn(child,goal_state)+ child.depth
                for priority, statee in frontier.queue:
                    if (child.state == statee.state) and priority < cost:
                        continue
                child.setParent(parent_state)
                frontier.put((cost,child))


start=state("125348670")
goal=state("012345678")
# ch = AStar(start,goal,manhattan_distance)
ch = AStar(start,goal,euclidean_distance)
traverse(ch)