import automaton_q1 as q1
import pandas as pd
import automatons_tests as test
import determinist

def is_word_recognized(automaton, word) : 
    #decorator for recursing function below
    if  determinist.is_automaton_deterministic(automaton)[0] : # be deterministic simplify
        df = q1.get_good_type(automaton,'dataFrame') 
    else : 
        df =  df = q1.get_good_type(determinist.to_automaton_deterministic(automaton),'dataFrame') 
    alphabet = df.columns[:-2]
    print(df)
    # verification that avery letter of the word exist in this automaton
    for letter in word :
        if letter not in alphabet :
            return False # eliminate trivial case
    state = list(df[df.initial_state == True].index)[0]
    rec = []
    return is_word_recognized_rec(df,word,state,rec)
           

def is_word_recognized_rec(df,word,state,rec) :
    if not len(word) : # exit condition
        return df.final_states.loc[str(state)]
    else :
        if q1.is_transition_valid(df,word[0],state) :
            return is_word_recognized_rec(df,word[1:],', '.join(q1.is_transition_valid(df,word[0],state)),rec)
        else : return False        


def is_complete(automaton) :
    df = q1.get_good_type(automaton,'dataFrame')
    return not df[list(df.columns)[:-2]].isin([q1.null_transition]).any().any() # return False if there is a null value in the df



def completing(automaton) :
    df = q1.get_good_type(automaton,'dataFrame')
    # create a df of the single line, the phi state
    data_phi = {}
    for letter in df.columns : 
        data_phi[letter] = q1.phi_transition
        data_phi['initial_state'], data_phi['final_states'] = False, False
    # concat phi and original automaton    
    phi_state = pd.DataFrame( index=['phi'], data = data_phi)
    df = pd.concat([df, phi_state])
    df.replace(q1.null_transition,q1.phi_transition, inplace= True) # replace all null value by transition to phi
    return df

# print(completing(test.auto10))
# print(is_complete(completing(test.auto10)))
# print(is_word_recognized(test.auto8, 'abcdacbacbabcdacd'))
