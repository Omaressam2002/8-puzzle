import heapdict
import numpy as np
from State import state
from utils import *

def A_star(start:state,goal:state,criterion,display=False):
    flag = False
    if start.state == goal.state:
        return state
    qu = heapdict.heapdict()
    explored = set()
    frontiers = set()
    cost = calc_heuristic2(start,goal,criterion)
    qu[start] = cost
    frontiers.add(start.toString())
    search_depth = 0
    while len(qu) != 0:
        # to check for children and enqueue them
        start = qu.popitem()[0]
        
        frontiers.remove(start.toString())
        
        explored.add(start.toString())
        search_depth = max(search_depth,start.level)
        
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
                explored.add(child.toString())
                return child,explored,max(search_depth,child.level)
            children.append(child)
        if (col-1) >= 0 :
        # swap el zero ma3 el peice el 3al shemalo we enque it to the frontier list : zero <=> zero-1
            child = state(start.state)
            child.state[zero],child.state[zero-1] = child.state[zero-1],child.state[zero]
            if goal.state == child.state :
                child.setParent(start)
                explored.add(child.toString())
                return child,explored,max(search_depth,child.level)
            children.append(child)
        if (row+1) <= 2 :
            # swap el zero ma3 el peice el ta7teeh we enque it to the frontier list : zero <=> zero+3
            child = state(start.state)
            child.state[zero],child.state[zero+3] = child.state[zero+3],child.state[zero]
            if goal.state == child.state :
                child.setParent(start)
                explored.add(child.toString())
                return child,explored,max(search_depth,child.level)
            children.append(child)
        if (row-1) >= 0  :
            # swap el zero ma3 el peice el foo2eeh we enque it to the frontier list : zero <=> zero-3
            child = state(start.state)
            child.state[zero],child.state[zero-3] = child.state[zero-3],child.state[zero]
            if goal.state == child.state :
                child.setParent(start)
                explored.add(child.toString())
                return child,explored,max(search_depth,child.level)
            children.append(child)

        # kol wa7da minhom hanetcheck enha makanetsh fel frontier list abl kida we ba3dein hanenque it 
        for child in children:
            # law it was never there put immediately
            childS = child.toString()
            # taree2a ageeb beeha el prev child min gher loop
            if not (childS in explored) and not (childS in frontiers):
                child.setParent(start)
                frontiers.add(childS)
                cost = calc_heuristic2(child,goal,criterion) + child.level
                qu[child] = cost
            # else check for decrease key
            elif (childS in frontiers):
                prev_child  = [c for c in  qu.keys() if (c.state==child.state)]
                prev_child = prev_child[0]
                prev_cost = qu[prev_child]
                cost = calc_heuristic2(child,goal,criterion) + child.level
                #decrease key
                if cost < prev_cost:
                    prev_child.setParent(start)
                    prev_child.children = child.children
                    qu[prev_child] = cost
    if not flag:
        print("solution not Found")


def Astar_interface(start,goal,criterion="euclidean"): # returns a np array of states
    start = state(start)
    goal = state(goal)
    child,explored,search_depth = A_star(start,goal,criterion)
    list_of_states = listofState(child)
    return np.array(list_of_states),len(list_of_states),child,start,explored,search_depth