import automaton_q1 as q1
import pandas as pd


def find_language(automaton) :

    df = q1.get_good_type(automaton, 'dataFrame')
    alphabet = list(df.columns)[:-2]
    state = df[df.initial_state == True].index[0]
    regex = ''
    print(state,state)
    for letter in alphabet :
        out_transition = q1.is_transition_valid(automaton, letter, state)
    if  not out_transition  : return ''

    # a = language_rec(df, regex, state, alphabet)
    return
        

def language_rec(automaton, regex, state,alphabet) : 
    for letter in alphabet : 
        # print(state)
        next_states = q1.is_transition_valid(automaton, str(letter), state)
    if state in  next_states:
        if regex != '' and regex[-1] == state :
            regex += '*'
        else : regex += state + '*'
        next_states.remove(state)
    if len(next_states > 1) :
        regex = [language_rec(automaton, regex, next_states[i]) for i  in range(len(next_states))]

    elif len(next_states == 1): 
        return language_rec(automaton, regex + next_states[0],next_states[0],alphabet)
    else : return regex

print(find_language(q1.automate))