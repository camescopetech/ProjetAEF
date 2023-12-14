import pandas as pd
from automaton_q1 import *
#from debut import * 

def is_automaton_deterministic(automaton):
    """ Verify if the automaton is deterministic. Return why if isn't else return nothing """
    if type(automaton)  == dict :
        dic = automaton
    elif type(automaton) == pd.DataFrame :
        dic = table_to_dict(automaton)  
    else :
        raise TypeError(f'automaton_specified wron type : dict or dataframe expected, got {type(automaton)}')    
    initiaux = dic['initial_state']
    if len(dic['initial_state']) != 1:
        return (False,"The automaton hasn't only one initial state")
    stats = dic['states']
    transis = dic['transitions']
    for stat in stats :
        listTransi = []
        for transi in transis :
            if stat == transi[0] :
                if transi[2] in listTransi :
                    result = False
                    return (False,f"The state {stat} can follow more than one time the transition {transi[2]}") 
                    break    
                else:
                    listTransi.append(transi[2])
    return (True,"The automaton is deterministic")
               
def to_automaton_deterministic(afn):
    afd = {
        'alphabet': afn['alphabet'],
        'states': [],
        'initial_state': '',
        'final_states': [],
        'transitions': []
    }
    afn_states = sorted(afn['states'])
    afd['initial_state'] = afn['initial_state']
    afd['states'].append(afd['initial_state'])
    queue = [afd['initial_state']]  
    created_states = set(afd['initial_state'])
    while queue:
        current_afd_state = queue.pop(0)
        current_afn_states = current_afd_state.split(', ')    
        for letter in afn['alphabet']:
            possible_states = set()
            
            for afn_state in current_afn_states:
                for t in afn['transitions'] :
                    if t[0] == afn_state and t[2] == letter :
                        transitions = t[1]
                        possible_states.update(transitions)
            
            possible_states = sorted(possible_states)
            new_afd_state = ', '.join(possible_states) or 'null'                                
            if new_afd_state not in afd['states'] and new_afd_state != 'null' and new_afd_state not in created_states:
                queue.append(new_afd_state)
                created_states.add(new_afd_state)
                afd['states'].append(new_afd_state)
                
            for state in possible_states:
                if state in afn['final_states']:
                    afd['final_states'].append(new_afd_state)
            if new_afd_state != 'null':
                afd['transitions'].append([current_afd_state, new_afd_state, letter])
        afd['final_states'] = sorted(set(afd['final_states']))
    afd['transitions'] = sorted(afd['transitions'])
    
    return afd

#print(to_automaton_deterministic(automate_non_deter))

        
#print(is_automaton_deterministic(automate_deter))
