import numpy as np
from State import state

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
