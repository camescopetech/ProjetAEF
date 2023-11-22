import pandas as pd
# import numpy as np

null_transition = 'null'
phi_transition = 'phi'

automate = {
    'alphabet': ['a','b'],
    'states' : ['0','1','2','3'],
    'initial_state' : '0',
    'final_states' : ['2','3'],
    'transitions': [
        ['0','0','b'],
        ['0','1','a'],
        ['0','3','a'],

        ['1','1','b'],
        ['1','2','a'],
        ['1','2','b'],

        ['2','2','a'],
        ['2','2','b'],

        ['3','3','a']
    ]
}


df_auto = pd.DataFrame(index = ['0','1','2','3'], data = {
    'a': ['1, 3','2','2','3'],
    'b' : ['0','1, 2','2',null_transition],
    'initial_state': [True,False,False,False],
    'final_states':[False,False,True,True]
})
# print(df_auto)

def dict_to_table(dico) : #ok
    states = dico['states']
    df = pd.DataFrame(index= states)
    for letter in dico['alphabet'] :
        values = [null_transition for _ in range(len(states))]
        for transition in dico['transitions'] :
            start_position = -1
            end_position = null_transition
            if transition[2] == letter :
                k = 0     #hashtable maybe
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

        df[f'{letter}'] = values

    df['initial_state'] = False
    df['final_states'] = False  
    

    for i in range(len(states)) :
        if dico['initial_state'] == df.index[i] :
            df.loc[states[i],'initial_state'] = True

    final_states = dico['final_states'].copy()  
    k = 0
    # print(df)
    while  len(final_states)  != 0 :
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
                splitted_states = df[str(col)].loc[row].split(', ')
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

# print(dict_to_table(automate) == df_auto)
# print(table_to_dict(df_auto))
# print(automate)
# print(automate == table_to_dict(df_auto))
# print(table_to_dict(dict_to_table(automate)))

# print(table_to_dict(dict_to_table(automate)) == automate)


# df_test = dict_to_table(automate)
#print(df_test)
# print(list(df_test[df_test.final == True].index))
#print(table_to_dict(df_test))
# print(automate['transitions'] == sorted(automate['transitions']))
# print(sorted(automate['transitions']))

def save_automaton(automaton,file_path='Untitled.txt') :
    with open(file_path,'w') as file :
        file.write(str(automaton))

#save_automaton(automate,'test.txt') 

def import_automaton(file_path) :
    with open(file_path,'r') as file :
        automaton = eval(file.read())
    return automaton

#auto2 = import_automaton('test.txt')  
# print(dict_to_table(auto2))















#back  else :
            # raise TypeError(f'automaton_specified wrong type : dict or dataframe expected, got {type(automaton)}') 
