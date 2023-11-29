import json
import ast

def conversion(automate):
    try:

        structure_python = ast.literal_eval(automate)
        chaine_json = json.dumps(structure_python)
        
        return chaine_json
    except (SyntaxError, ValueError) as e:
        #print(f"Erreur lors de la conversion : {e}")
        return None
    
def isNoneOccurenceList(automate,key):

    list = automate.get(key, [])

    return len(list) == len(set(list))

def isAutomateString(automate):

    automate = conversion(automate)

    #ERROR1: not a json
    if automate is None:
        return 1
    
    automate = json.loads(automate)
    
    #ERROR2: the keys are false"
    keys_json = ['alphabet','states','initial_state','final_states','transitions']
    if keys_json != list(automate) :
        return 2
    
    alphabet = automate.get('alphabet', [])
    states = automate.get('states', [])
    initial_state = automate.get('initial_state', [])
    final_states = automate.get('final_states', [])
    transitions = automate.get('transitions', [])

    #ERROR3: Transition must have tree element
    for transition in transitions:
        if len(transition) != 3:
            return 3

    #ERROR4: 'initial_state' must have one element
    if len(initial_state) != 1:
        return 4

    #ERROR5: Element in 'alphabet', 'states' and 'final_states' must have any occurence
    keys_json = ['alphabet','states','final_states']
    for key in keys_json:
        if not isNoneOccurenceList(automate,key):
            return 5
        
    #--------------------------------
    #ERROR6: alphabet is not correct"
    listAlphabet = []
    for transition in transitions:
        listAlphabet.append(transition[2])    

    if sorted(alphabet) != sorted(set(listAlphabet)):
        return 6

    #ERROR7: states is not correct"
    listState= []
    for transition in transitions:
        listState.append(transition[0])   
        listState.append(transition[1])   

    if sorted(states) != sorted(set(listState)):
        return 7
 
    #--------------------------------
    #ERROR8: states must contain initial_state
    if initial_state[0] not in states:
        return 8
    
    #ERROR9: states must contain final_states
    for final_state in final_states:
        if final_state not in states:
            return 9

    return 0