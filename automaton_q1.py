import pandas as pd
# import numpy as np

null_transition = 'null'
phi_transition = 'phi'

def dict_to_table(dico) : 
    states = dico['states']
    df = pd.DataFrame(index = states)
    for letter in dico['alphabet'] :
        values = [null_transition for _ in range(len(states))]
        for transition in dico['transitions'] :
            start_position = -1
            end_position = null_transition
            if transition[2] == letter :
                k = 0     #hashtable maybe but complex
                while(start_position == -1 or end_position == null_transition) :
                    temp = states[k]
                    if transition[1] == temp :
                        end_position = temp
                    if transition[0] == temp :
                        start_position = k
                    k+=1
                if not end_position in values[start_position] : 
                    values[start_position] = f'{values[start_position]}, {end_position}'
        for value in values :
            if ', ' in value :
                values[values.index(value)] = value[len(null_transition)+2:]
        df[letter] = values

    df['initial_state'] = False
    df['final_states'] = False  
    
    for i in range(len(states)) :
        if dico['initial_state'] == df.index[i] :
            df.loc[states[i],'initial_state'] = True

    final_states = dico['final_states'].copy()  
    k = 0
    while  len(final_states) != 0 :
        if final_states[0] == df.index[k] :
            df.loc[states[k],'final_states'] = True
            k=0
            final_states.pop(0)
        k+=1    
    return df


def table_to_dict(df) :
    
    transition = []
    for col in list(df.columns[:-2]) :
        for row in list(df.index) :
            if df[str(col)].loc[str(row)] != null_transition:
                splitted_states = df[str(col)].loc[row].split(', ') #case not determinist, multiple states (one if determinist)
                for arrival_state in splitted_states :
                    transition.append([row,arrival_state,col])
                        
    dico = {
    'alphabet': list(df.columns[:-2]),
    'states' : list(df.index),
    'initial_state' : list(df[df.initial_state == True].index)[0],
    'final_states' : list(df[df.final_states == True].index),
    'transitions': sorted(transition)}

    return dico

def get_good_type(automaton,wanted_type) :
    assert wanted_type in ['dict','dataFrame'] and type(automaton) in [dict, pd.DataFrame]
    if wanted_type == 'dataFrame' :
        if type(automaton)  == dict :
            return dict_to_table(automaton)
        return automaton
        
    if type(automaton) == dict :
        return automaton
    return table_to_dict(automaton)

def save_automaton(automaton,file_path='Untitled.txt') :
    with open(file_path,'w') as file :
        file.write(str(automaton))

#save_automaton(automate,'test.txt') 

def import_automaton(file_path) :
    with open(file_path,'r') as file :
        automaton = eval(file.read())
    return automaton



def is_transition_valid(df, letter, state) :
    if df[str(letter)].loc[str(state)] == null_transition :
        return False
    else : return df[str(letter)].loc[str(state)].split(', ')
