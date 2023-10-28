import heapdict
import numpy as np
from State import state
from utils import *

def A_star(start:state,goal:state,display=False,criterion="euclidean"):
    found = False
    if start.state == goal.state:
        return state
    qu = heapdict.heapdict()
    cost = calc_heuristic(start.state)
    qu[start] = cost
    explored = []
    while len(qu) != 0:
        # to check for children and enqueue them
        start = qu.popitem()[0]

        explored.append(start.state)

        zero = start.state.index("0")
        row = (zero)//3
        col = (zero)%3
    
        # neighbors
        children = []
        
        #finding neighbors
        if (col+1) <= 2 :
            # swap el zero ma3 el peice el 3al yeemeeno we enque it to the frontier list : zero <=> zero+1
            child = state(start.state)
            child.state[zero],child.state[zero+1] = child.state[zero+1],child.state[zero]
            if goal.state == child.state :
                child.setParent(start)
                return child
            children.append(child)
        if (col-1) >= 0 :
        # swap el zero ma3 el peice el 3al shemalo we enque it to the frontier list : zero <=> zero-1
            child = state(start.state)
            child.state[zero],child.state[zero-1] = child.state[zero-1],child.state[zero]
            if goal.state == child.state :
                child.setParent(start)
                return child
            children.append(child)
        if (row+1) <= 2 :
            # swap el zero ma3 el peice el ta7teeh we enque it to the frontier list : zero <=> zero+3
            child = state(start.state)
            child.state[zero],child.state[zero+3] = child.state[zero+3],child.state[zero]
            if goal.state == child.state :
                child.setParent(start)
                return child
            children.append(child)
        if (row-1) >= 0  :
            # swap el zero ma3 el peice el foo2eeh we enque it to the frontier list : zero <=> zero-3
            child = state(start.state)
            child.state[zero],child.state[zero-3] = child.state[zero-3],child.state[zero]
            if goal.state == child.state :
                child.setParent(start)
                return child
            children.append(child)

        frontiers = [x.state for x in qu.keys()]
        # kol wa7da minhom hanetcheck enha makanetsh fel frontier list abl kida we ba3dein hanzo2aha 
        for child in children:
            # law it was never there put immediately
            if not (child.state in explored) and not (child.state in frontiers):
                child.setParent(start)
                cost = calc_heuristic(child.state,criterion) + child.level
                qu[child] = cost
            elif (child.state in frontiers):
                child  = [c for c in  qu.keys() if (c.state==child.state)][0]
                prev_cost = qu[child] 
                cost = calc_heuristic(child.state,criterion) + child.level
                #decrease key
                if cost < prev_cost:
                    qu[child] = cost
    if not flag:
        print("solution not Found")


def Astar_interface(start,goal,criterion="euclidean"): # returns a np array of states
    start = state(start.tolist())
    goal = state(goal.tolist())
    child = A_star(start,goal,criterion)
    list_of_states = listofState(child)
    return np.array(list_of_states),len(list_of_states),child,start