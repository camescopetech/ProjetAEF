import pandas as pd
# import numpy as np

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

df_auto = pd.DataFrame(index = ['0','1','2','3'], data = {
    'a': ['3','1','-1','3'],
    'b' : ['1','2','-1','-1'],
    'initial_state': [True,False,False,False],
    'final_states':[False,False,True,True]
})
#print(df_auto)

def dict_to_table(dico) :
    states = dico['states']
    df = pd.DataFrame(index= states)
    for letter in dico['alphabet'] :
        values = ['-1' for _ in range(len(states))]
        for transition in dico['transitions'] :
            start_position = -1
            end_position = '-1'
            if transition[2] == letter :
                k = 0     #hashtable maybe
                while(start_position == -1 or end_position == '-1') :
                    temp = states[k]
                    if transition[1] == temp :
                        end_position = temp
                    if transition[0] == temp :
                        start_position = k
                    k+=1
                values[start_position] = end_position   
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
            if df[str(col)].loc[str(row)] != '-1':
                transition.append([row,df[str(col)].loc[row],col])

    dict = {
    'alphabet': list(df.columns[:-2]),
    'states' : list(df.index),
    'initial_state' : list(df[df.initial_state == True].index)[0],
    'final_states' : list(df[df.final_states == True].index),
    'transitions': sorted(transition)}

    return dict

# print(dict_to_table(automate))
# print(table_to_dict(df_auto))
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

#save_automaton(automate,'1er_Semestre/projet_python/test.txt') 

def import_automaton(file_path) :
    with open(file_path,'r') as file :
        automaton = eval(file.read())
    return automaton

auto2 = import_automaton('1er_Semestre/projet_python/test.txt')  
# print(dict_to_table(auto2))


def is_word_recognized(automaton,word):
    if type(automaton)  == dict :
        df = dict_to_table(automaton)
    elif type(automaton) == pd.DataFrame :
        df = automaton.copy ()  
    else :
        raise TypeError(f'automaton_specified wron type : dict or dataframe expected, got {type(automaton)}')    
    current_state = list(df[df.initial_state == True].index)[0]
    w = word
    while len(w) !=0 :
        if df[w[0]].loc[str(current_state)] == '-1' :
            return False
        current_state = df[w[0]].loc[str(current_state)]
        w = w[1:]
    return df.final_states.loc[str(current_state)]
        
print(is_word_recognized(automate,'aaaaa'))


# print(df_auto.final_states.loc[str(3)])}))
