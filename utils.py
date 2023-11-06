import numpy as np
from State import state

class Tiles:
    def __init__(self,indx,value):
        self.indx = int(indx)
        self.value = int(value)
        self.row = self.indx//3
        self.col = self.indx%3
        self.position = (self.row,self.col)

def manhattan_distance(state:state,goal:state):
    tiles_start = [Tiles(i,state.state[i]) for i in range(9)]
    tiles_end = [Tiles(i,goal.state[i]) for i in range(9)]

    tiles_start.sort(key=lambda x:x.value)
    tiles_end.sort(key=lambda x:x.value)

    tot_distance = 0
    for i in range(1,9):
        distance = abs(tiles_start[i].position[0] - tiles_end[i].position[0]) + abs(tiles_start[i].position[1] - tiles_end[i].position[1])
        
        tot_distance += distance

    return tot_distance

def euclidean_distance(state:state,goal:state):
    tiles_start = [Tiles(i,state.state[i]) for i in range(9)]
    tiles_end = [Tiles(i,goal.state[i]) for i in range(9)]

    tiles_start.sort(key=lambda x:x.value)
    tiles_end.sort(key=lambda x:x.value)

    tot_distance = 0
    for i in range(1,9):
        distance = ((tiles_start[i].position[0] - tiles_end[i].position[0])**2 + (tiles_start[i].position[1] - tiles_end[i].position[1])**2)**0.5
        tot_distance += distance

    return tot_distance
   
def calc_heuristic2(state : state,goal:state,criterion='euclidean'):
    if criterion == 'euclidean':
        return euclidean_distance(state,goal)
    else:
        return manhattan_distance(state,goal)


def listofState(state:state):
    list_of_states = []
    while state:
        list_of_states.append(state.state)
        state = state.parent
    return np.array(list_of_states)

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



def calc_heuristic(state:list,criterion='euclidean'):
    hn = 0 
    goal_ids = [(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    for i in state:
        idx = state.index(i)
        # idx of the peice
        row = (idx)//3
        col = (idx)%3
        idx = (row,col)
        
        goal_idx = goal_ids[int(i)-1]
        hn += calc_cost(idx,goal_idx,criterion)
    return hn

def calc_cost(idx:tuple,goal:tuple,criterion):
    if criterion == "euclidean" :
        return (((idx[0]-goal[0])**2)+((idx[1]-goal[1])**2))**0.5
    elif criterion == "manhattan" :
        return abs(idx[0]-goal[0])+abs(idx[1]-goal[1])

