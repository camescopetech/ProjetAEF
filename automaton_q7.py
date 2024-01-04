from operator import concat
import recognize_complete_q2_q3_q4 as q2
import automaton_q1 as q1
from readline import append_history_file
import pandas as pd

null_transition  = 'null'
phi_transition = 'phi'



# ************************ FONCTION COMPLEMENT ******************************

def complem_automaton(automaton):
    complem_dict = {
        'alphabet': automaton['alphabet'],
        'states': automaton['states'],
        'initial_state': automaton['initial_state'],  
         # Every state that is not a final state becomes a final state, and vice versa.
        'final_states': [state for state in automaton['states'] if state not in automaton['final_states']],
        'transitions': automaton['transitions']
    }
    
    #df = q1.dict_to_table(complem_dict)
    #return df
    return complem_dict



# if not q2.is_complete(automate):
#     df_automate = q2.completing(automate)

# df_automate = complem_automaton(automate)
# print(df_automate)



# ************************ FONCTION MIROIR ******************************

def miroir_automaton(automaton):
    miroir_dict = {
        'alphabet': automaton['alphabet'],
        'states': automaton['states'],
        'initial_state': automaton['final_states'],  # Invert final states as initial states
        'final_states': [automaton['initial_state']],  # Invert initial state as final state
        'transitions': [[transition[1], transition[0], transition[2]] for transition in automaton['transitions']]
        # Reverse the direction of transitions
    }

    #df = q1.dict_to_table(miroir_dict)
    #return df
    return miroir_dict



# if not q2.is_complete(automate):
#     df_automate = q2.completing(automate)

# df_automate = miroir_automaton(automate)
# print(df_automate)




# ************************** FONCTION PROD *********************

def produit_aefs(automate1, automate2):
    # Check that the alphabets are the same for both automata
    if automate1['alphabet'] != automate2['alphabet']:
        raise ValueError("Les alphabets des deux automates doivent etre identiques.")


    states1 = automate1['states']
    states2 = automate2['states']

    initial1 = automate1['initial_state']
    initial2 = automate2['initial_state']


    prodAutom = {
        'alphabet': automate1['alphabet'],
        'states': [f'{state1},{state2}' for state1 in states1 for state2 in states2],
        'initial_state': [f'{initial1},{initial2}'],
        'final_states': [],
        'transitions': []
    }


    # final state
    # A state is final in the product if and only if each component is final in its respective automaton
    if automate1['final_states'] and automate2['final_states']:
        prodAutom['final_states'] = [f"{automate1['final_states']},{automate2['final_states']}"]



     # Function for finding transitions for a given combined state
    def find_transitions(state_combined):
        state1, state2 = state_combined.split(',')
        transitions_found = []

        for symbol in prodAutom['alphabet']:
            next_states1 = [t[1] for t in automate1['transitions'] if t[0] == state1 and t[2] == symbol]
            next_states2 = [t[1] for t in automate2['transitions'] if t[0] == state2 and t[2] == symbol]

            for ns1 in next_states1:
                for ns2 in next_states2:
                    transitions_found.append([state_combined, f"{ns1},{ns2}", symbol])

        return transitions_found

    # Add transitions to the production automaton
    states_to_process = [prodAutom['initial_state'][0]]  # Using element 0 of the list
    processed_states = set()

    while states_to_process:
        current_state = states_to_process.pop()
        processed_states.add(current_state)

        transitions = find_transitions(current_state)
        for transition in transitions:
            if transition not in prodAutom['transitions']:
                prodAutom['transitions'].append(transition)
                if transition[1] not in processed_states:
                    states_to_process.append(transition[1])



                
    #df = q1.dict_to_table(prodAutom)
    #return df
    return prodAutom
                    



# pd.set_option('display.max_rows', None)  # Aucune limite sur le nombre de lignes
# pd.set_option('display.max_columns', None)  # Aucune limite sur le nombre de colonnes
# pd.set_option('display.width', None)  # Ajuster la largeur pour accommoder chaque colonne
# pd.set_option('display.max_colwidth', None)  # Aucune limite sur la largeur du contenu de la colonne

# print(produit_aefs(automate,automate2))



# ************************** FONCTION CONCAT *********************

def concatAEF(automate1,automate2):

    if automate1['alphabet'] != automate2['alphabet']:
        raise ValueError("Concat impossible les alphabets sont différents")

    concatAutom = {
        'alphabet': automate1['alphabet'],
        'states': automate1['states'] + automate2['states'],
        'initial_state': automate1['initial_state'],
        'final_states': automate2['final_states'],
        'transitions': []
    }


    # add transitions from the first automate
    for transition in automate1['transitions']:
        concatAutom['transitions'].append(transition)


    # add transitions from the second automate
    for transition in automate2['transitions']:
        new_transition = [state.replace(',', '') if i != 2 else state for i, state in enumerate(transition)]
        concatAutom['transitions'].append(new_transition)   


    #df = q1.dict_to_table(concatAutom)
    #return df
    return concatAutom




# print(concatAEF(automate,automate2))






