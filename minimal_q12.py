import pandas as pd
import automaton_q1 as q1
import automatons_tests as test
import re

def minimal_automaton(automaton) : #based on find_cycles
 
    df = q1.get_good_type(automaton, 'dataFrame')
    alphabet = list(df.columns)[:-2]
    initial_state = df[df.initial_state == True].index[0]
    stack = [(initial_state,[initial_state])] # initialize the stack. Every element of it is a tuple containing the current state and the list of previous states
    final_state = list(df[df.final_states == True].index) 
    usefull_states = {initial_state} # must kept inital state
    maybe = []

    while stack :
        
        current_state = stack[0][0]
        path = stack[0][1]
        if current_state in final_state : #ending path : the states are usefull
            usefull_states.update(set(path + [current_state]))
  
        for letter in alphabet : #look for new states to find other paths
            next_state = q1.is_transition_valid(df, letter, current_state)
            if  next_state : 
                for state in next_state :
                    if state not in path : #state not already in the current path
                        stack.append((state, path + [state])) # supply stack with updated values
                    else : maybe.append((state,path)) # we are in a loop : the states are usefull if we get back to an usefull element without loop
        stack.pop(0)
   
    # add element usefull only in loops
    for el in maybe : 
        if el[0] in usefull_states :
            usefull_states.update(el[1])
    
    df_good =  df[df.index.isin(usefull_states)] #delete useless state (ok if determinist)
   
    for letter in alphabet : # for not determinist transitions
        df_good.loc[df_good[letter].str.contains(', '),letter] = df_good[letter].apply(lambda x :  ', '.join([el for el in x.split(', ') if el in usefull_states]))
    df_good = df_good.replace('',q1.null_transition)  # if not determinist transitions and all to useless states

    #delete transitions to useless states while ignoring not determinist transitions
    df_good.loc[:,alphabet] = df_good[alphabet].applymap(lambda x: x if re.search(',',x) else q1.null_transition if x not in usefull_states  else x) 

    return  df_good         


# print(q1.get_good_type(test.auto11,'dataFrame'))
# print(minimal_automaton(test.auto11))
