import pandas as pd
from automaton_q1 import *
#from debut import * 

def is_automaton_deterministic(automaton):
    """ Verify if the automaton is deterministic. Return why if isn't else return nothing """
    if type(automaton)  == dict :                      # Verify if the automaton is a dictionary or a table. 
        dic = automaton
    elif type(automaton) == pd.DataFrame :
        dic = table_to_dict(automaton)                      # Transform the table on dictionary  
    else :
        raise TypeError(f'automaton_specified wron type : dict or dataframe expected, got {type(automaton)}')    
    initiaux = dic['initial_state']
    stats = dic['states']
    transis = dic['transitions']
    for stat in stats :                      # Verify number of transitions for each state
        listTransi = []                      # List of transition letter possible for each state
        for transi in transis :                      # Verify each transition of the automaton
            if stat == transi[0] :                      # Take only transitions from the current state
                if transi[2] in listTransi :                # Verify if the letter of the alphabet is already in the list of transitions possible
                    result = False                   # If yes, return an error because the letter is more than one time in transition possible
                    return (False,f"The state {stat} can follow more than one time the transition {transi[2]}") 
                    break    
                else:
                    listTransi.append(transi[2])                      # If not append the letter to the list of transitions
    return (True,"The automaton is deterministic")                      # WHen we are here we are sure that the automaton is deterministic 
               
def to_automaton_deterministic(automaton):
    """ Transform an non deterministic automanton to a deterministic automaton """
    if type(automaton)  == dict :                      # Verify if the automaton is a dictionary or a table. 
        afn = automaton
    elif type(automaton) == pd.DataFrame :
        afn = table_to_dict(automaton)                      # Transform the table on dictionary  
    else :
        raise TypeError(f'automaton_specified wron type : dict or dataframe expected, got {type(automaton)}')   
    afd = {                      # Empty automaton who become to be the final deterministic automaton 
        'alphabet': afn['alphabet'],
        'states': [],
        'initial_state': '',
        'final_states': [],
        'transitions': []
    }
    afn_states = sorted(afn['states'])                      # sorting to be more logical
    afd['initial_state'] = afn['initial_state']                      # There every time are only one initial state
    afd['states'].append(afd['initial_state'])                      
    queue = [afd['initial_state']]                       # CCreate a queue for stats not already treat
    created_states = set(afd['initial_state'])                      # Set of created states 
    while queue:                      # Buckle for treating every state
        current_afd_state = queue.pop(0)
        current_afn_states = current_afd_state.split(', ')                      # Separation in the case of the state contain "two" state    
        for letter in afn['alphabet']:                      # Treat for each letter 
            possible_states = set()                      # Set of states possible with the current letter
            
            for afn_state in current_afn_states:                      # Take all the transitions of each single state in the current states which can be for example "1, 2"
                for t in afn['transitions'] :                      # Verify each transition of the automaton
                    if t[0] == afn_state and t[2] == letter :                      # Take only transitions who interest us 
                        possible_states.update(t[1])                      # Add the reachable state to our set of possible states
            
            possible_states = sorted(possible_states)                      # Sort of more logical things
            new_afd_state = ', '.join(possible_states) or 'null'                      # Format our site for have for example "1, 2"                             
            if new_afd_state not in afd['states'] and new_afd_state != 'null' and new_afd_state not in created_states:                       # Verify if new_afd_state haven't already, be meet and already in queue or created state
                queue.append(new_afd_state)
                created_states.add(new_afd_state)
                afd['states'].append(new_afd_state)
                
            for state in possible_states:                      # Buckle for verifying if state is final states or not 
                if state in afn['final_states']:                      # Verify if it's a final state
                    afd['final_states'].append(new_afd_state)
            if new_afd_state != 'null':                      # Verify if isn't null for, add it to the list of transitions
                afd['transitions'].append([current_afd_state, new_afd_state, letter])
        afd['final_states'] = sorted(set(afd['final_states']))
    afd['transitions'] = sorted(afd['transitions'])
    
    return afd

#print(to_automaton_deterministic(automate_non_deter))

        
#print(is_automaton_deterministic(automate_deter))
