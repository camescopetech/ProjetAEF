import automaton_q1 as q1
import pandas as pd

def is_word_recognized_old(automaton,word):
    df = q1.get_good_type(automaton,'dataFrame')
    current_state = list(df[df.initial_state == True].index)[0]
    w = word
    while len(w) :
        if df[w[0]].loc[str(current_state)] == q1.null_transition :
            return False
        current_state = df[w[0]].loc[str(current_state)]

        w = w[1:]
    return df.final_states.loc[str(current_state)]

def is_word_recognized(automaton, word, state = None, rec = []) : # a opti/nettoyer/rendre beau
    df = q1.get_good_type(automaton,'dataFrame')
    if state == None :
        state = list(df[df.initial_state == True].index)[0]
    rec = []
    rec += [is_word_recognized_rec(df,word,state,rec)]
    return True in rec
           



def is_word_recognized_rec(df,word,state,rec) :
    # print(word,state)
    if not len(word) :
        return df.final_states.loc[str(state)]
    else :
        if q1.is_transition_valid(df,word[0],state) :
            for stat in q1.is_transition_valid(df,word[0],state) :
                # print(rec)
                rec.append(is_word_recognized_rec(df,word[1:],stat,rec))
        else : return False        

# print(is_word_recognized(q1.automate,'baababbaba')) 




# print(q1.automate)

# print(df_auto.final_states.loc[str(3)])}))

def is_complete(automaton) :
    df = q1.get_good_type(automaton,'dataFrame')
    return not df[list(df.columns)[:-2]].isin([q1.null_transition]).any().any()


#print(df_auto[list(df_auto.columns)[:-2]])


#print(get_good_type(df_auto,'dict'))

def completing(automaton) :
    df = q1.get_good_type(automaton,'dataFrame')
    data_phi = {}
    for letter in df.columns :
        data_phi[letter] = q1.phi_transition
        data_phi['initial_state'], data_phi['final_states'] = False, False
    phi_state = pd.DataFrame( index=['phi'], data = data_phi)
    df = pd.concat([df, phi_state])
    df.replace(q1.null_transition,q1.phi_transition, inplace= True)
    return df

print(is_complete(completing(q1.automate)))
# print([phi_transition for _ in range(len(df_auto.columns)-2)])
# print(range(len(df_auto.columns)-2))
# print(completing(q1.automate))
