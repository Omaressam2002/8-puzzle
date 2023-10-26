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
        # parent is another state object
        self.state = list(state)
        self.parent = None
        self.children = []
    def setParent(self,parent):
        self.parent = parent
        self.parent.children.append(self)
    def printState(self):
        for i in range(3):
            ithrow = self.state[(3*i):(3*(i+1))]
            print(ithrow)
    def toString(self):
        print(''.join(self.state))

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


def AStar(start_state:state , goal_state:state,heuristic_fn):
    frontier = PriorityQueue()
    frontier.put((0,start_state))
    explored = []
    depth = 0

    if start_state.state == goal_state.state:
        return start_state

    while not frontier.empty():
        parent_state = frontier.get()[1]
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
            # frontier.put((heuristic_fn(child,goal_state) + depth,child))

        if blank_col-1 >= 0:
            child = state(parent_state.state)
            child.state[blank_index],child.state[blank_index-1] = child.state[blank_index-1],child.state[blank_index]
            if child.state == goal_state.state:
                child.setParent(parent_state)
                return child
            children.append(child)
            # frontier.put((heuristic_fn(child,goal_state) + depth,child))

        if blank_row+1 <= 2:
            child = state(parent_state.state)
            child.state[blank_index],child.state[blank_index+3] = child.state[blank_index+3],child.state[blank_index]
            if child.state == goal_state.state:
                child.setParent(parent_state)
                return child
            
            children.append(child)
            # frontier.put((heuristic_fn(child,goal_state) + depth,child))


        if blank_row-1 >= 0:
            child = state(parent_state.state)
            child.state[blank_index],child.state[blank_index-3] = child.state[blank_index-3],child.state[blank_index]
            if child.state == goal_state.state:
                child.setParent(parent_state)
                return child
            children.append(child)
            # frontier.put((heuristic_fn(child,goal_state) + depth,child))

        
        for child in children:
            if not (child.state in explored) and not (child in frontier.queue):
                child.setParent(parent_state)
                cost = heuristic_fn(child,goal_state)+depth
                frontier.put((cost,child))







ststate = state("123456780")
endstate = state("123457608")
# print(ststate.state)
AStar(ststate,endstate,manhattan_distance)