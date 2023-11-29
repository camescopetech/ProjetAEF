import automaton_q1 as q1
import pandas as pd
import re
import random
import time

automate = {
    'alphabet': ['a','b'],
    'states' : ['0','1','2','3'],
    'initial_state' : '0',
    'final_states' : ['2','3'],
    'transitions': [
        ['0','1','b'],
        ['0','3','a'],
        ['1','1','a'],
        ['1','2','b'],
        ['3','3','a']
    ]
}

states = automate['transitions'][0][1]
print(states)

def adjacent(state):
    return state

def is_accessible(automate, state):

    states = automate['states']
    visited = []
    initial_state = automate['initial_state']
    visited.append(initial_state)

    # While stack isn't empty
    while visited != []:
        #current state is the last state visited
        current_state = visited.pop()

        # if current state is the one visited the state is accessible
        if current_state == state:
            return True

        # else we look for all the adjacent state of our current state
        else :
            adjacents = adjacent(state)
            for adjacent in adjacents :
                # if the adjacent state hasn't been visited we had it to the visited stack
                if adjacent not in visited :
                    visited.append(adjacent)

    # state isn't accessible
    return False

def is_coaccessible(state):
    return state

def excise(automate):

    inaccesible_states = []
    coaccessible_states = []
    states = automate['states']

    for state in states:
        if not is_accessible(state):
            inaccesible_states.append(state)

    for state in states:
        if not is_coaccessible(state):
            coaccessible_states.append(state)

    for state in states :
        if state in inaccesible_states or state in coaccessible_states :
            return 1
