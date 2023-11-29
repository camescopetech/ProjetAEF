import pandas as pd
from debut import * 

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
        return "The automaton hasn't only one initial state"
    stats = dic['states']
    transis = dic['transitions']
    for stat in stats :
        listTransi = []
        for transi in transis :
            if stat == transi[0] :
                if transi[2] in listTransi :
                    result = False
                    return f"The state {stat} can follow more than one time the transition {transi[2]}"      
                    break    
                else:
                    listTransi.append(transi[2])


        
print(is_automaton_deterministic(automate))
