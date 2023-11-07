import numpy as np
from State import state
from utils import *

def BFS(start:state,goal:state,display=False):
    flag = False
    qu = [ start ]
    explored = set()
    search_depth = 0
    if start.state == goal.state:
        return start
    while len(qu) != 0:
        # to check for children and enqueue them
        start = qu[0]
        qu.remove(qu[0])

        explored.add(start.toString())
        # explored state level
        search_depth = max(search_depth,start.level)
    
        zero = start.state.index("0")
        row = (zero)//3
        col = (zero)%3
    
        # neighbors
        children = []
        # finding neighbors
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

        #frontiers = [c.state for c in qu]
        # kol wa7da minhom hanetcheck enha makanetsh fel frontier list abl kida we ba3dein hanenque it 
        for child in children:
            childS = child.toString()
            if not (childS in explored):
                child.setParent(start)
                qu.append(child)
    if not flag:
        print("solution not Found")


def BFS_interface(start,goal): # returns a np array of states
    start = state(start)
    goal = state(goal)
    child,explored,search_depth = BFS(start,goal)
    list_of_states = listofState(child)
    return np.array(list_of_states),len(list_of_states),child,start,explored,search_depth