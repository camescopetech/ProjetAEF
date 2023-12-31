import automaton_q1 as q1
import pandas as pd
import automatons_tests as test
import os
import re
import random
import minimal_q12 as q12
import automaton_q2_q3 as q2


def find_regex(automaton) :
    # Process :
    # 1. look ending path with no loop
    # 2. find every loop
    # 3. for each ending path, spot every loop (and imbricated cycle = loop who can be followed through the precedent loop) which could be used and who does not took the end path way.
    # Each loop can be followed only once per position of the path. Do this at every position of the ending_path
    # 4.The regex will be cleaned and optimize with subfunction below
    df = q1.get_good_type(automaton, 'dataFrame')
    cycles = find_cycle(df) # 1.

    ini_state = df[df.initial_state == True].index[0]
    paths = end_path(df,ini_state) # 2.
    res = []
    for path in paths : # start 3.

        current_natural_path_index = 0
        word = []
        current_cycles = []

        states_full = path[0]
        letters_full = path[1]

        # initialize stack with inital state then end_path data
        stack = [(ini_state,'start',False)] 
        for i in range(len(states_full)) :
            stack.append((states_full[i],letters_full[i],True))
            
        while stack :

            letter = stack[0][1]
            current_state = stack[0][0]
            next_default_state = stack[0][1]
            is_default_path = stack[0][2]
            if is_default_path :
                current_cycles = []
                current_natural_path_index += 1
            stack.pop(0) # we unstack here because we add loops states at the beggining and all data saved in variables

            if current_state :
                for cycle in cycles :

                    if current_state in cycle[0] and cycle not in current_cycles :  #new cycle found but maybe not correct
                    
                        current_cycles.append(cycle)
                        debut_cycle = cycle[0].index(current_state)
                        # on ne prend pas le cycle si pas prochain. On prend si dernier etat ou cycle demarre pas par suite path
                        if (current_natural_path_index+1 >= len(states_full)) or cycle[0][(debut_cycle+1)%len(cycle[0])] != path[0][(current_natural_path_index+1)]: # if the loop is not taking ending_path next state first, loop ok
                            for i in range(len(cycle[0])):
                                stack.insert(i,(cycle[0][(debut_cycle+i)%len(cycle[0])],cycle[1][(debut_cycle+i)%len(cycle[0])],False))
                            stack.insert(len(cycle[0]),('False',['*',len(cycle[0]) ,len(current_cycles)], False))

            word.append(letter) 
        res.append(word)
    return optimize(refactor(star(res)))    



def find_cycle(automaton) :   
    df = q1.get_good_type(automaton, 'dataFrame')
    alphabet = list(df.columns)[:-2]
    cycles_found = []
    sorted_cycles = []
    stack =[(df[df.initial_state == True].index[0],[],[])] #the stack contains a tuple of 3 elements : the current state, the ordered list of already visited states and the letters corresponding to this pathing.

    while stack :
        curr_state = stack[0][0]  
        path = stack[0][1] #add current state to visited_states
        letters_list =stack[0][2]
        for letter in alphabet : 
            next_state = q1.is_transition_valid(df, letter, curr_state)
            if  next_state : #for each letter, if there is a valid transition
                if next_state[0] in path : #state already visited can be visited : we found a cycle
                    debut_cycle = path.index(next_state[0])
                    cycle = list(path[debut_cycle:])
                    if sorted(cycle) not in sorted_cycles : # Be sure this cycle is new and is not an already foud cycle from a different start
                        cycles_found.append((cycle,letters_list[debut_cycle+1:]+[letter]))
                        sorted_cycles.append(sorted(cycle))
                else : 
                    stack.append((next_state[0],path+ next_state,letters_list+[letter])) #supply stack with updated values
        stack.pop(0)            
    return cycles_found

 

def end_path(df,state) : 
    #find every path possible without any cycle, return a list of tuples containing a list of state and a list of letters.

    alphabet = list(df.columns)[:-2]
    stack = [(state,[state],[])] # initialize the stack. Every element of it is a tuple containing the current state, the list of previous state, and the letter used to get here
    final_state = list(df[df.final_states == True].index) 
    paths_found = [] 

    while stack :
        current_state = stack[0][0]
        path = stack[0][1]
        letters_list = stack[0][2]

        if current_state in final_state : #condition de fin trouvée
            paths_found.append((path[1:],letters_list))
  
        for letter in alphabet : #look for new states to find other paths
            next_state = q1.is_transition_valid(df, letter, current_state)
            if  next_state : 
                if next_state[0] not in path : #state not already in the current path
                    stack.append((next_state[0], path + next_state,letters_list + [letter])) # supply stack with updated values
       
        stack.pop(0)        
    return  paths_found          


def star(result) :
    # Before entering there, loops are indicated by an el like [,len_loop, False]
    # remplacer les cycles par un el de la liste. Un el meme pour plusieurs cycles imbriquées. On repère un cycle par un el qui est une liste
    res = [] #final result stored here
    
    for liste in result :
        temp_res = [] # 2 steps in this function : first is replacing loops indicator and items by a single element with a star at the end
        for i in range(len(liste)) :
            # find_regex is build to have the deeper loops in first. So, we can unstack loops from the begining with no intrication issue
            current_loop = []
            if type(liste[i]) == list : # current element is a loop  indicator
                len_loop = liste[i][1]
                k=0
                for el in temp_res[-len_loop:] : # build variable k which is the real value of the length of the cycle : the intricated loops add one to the length of the current loop
                    if el[0] =='(' : 
                        k+=1

                #remove the state who are in the loop from the temporary result and add the concatenation of the loop with a star instead
                if len_loop > 1 : 
                    current_loop = f'({"".join(temp_res[-(len_loop+k):])})*'
                    temp_res = temp_res[:(-len_loop-k)]
                    temp_res.append(current_loop)
                else : temp_res[-1] = temp_res[-1] + '*'    
            else : 
                temp_res.append(liste[i]) # add the current state to temporary res if not a loop indicator

        # second step : combine 2 consecutives loops into a single one, to be sure both could be used without order in the final regex
        good_res = [] 
        for  i in range(len(temp_res)-1) : #looking for 2 consecutives loops. Multiple tests for first and last items who has to be treated separatly to avoid errors
            if temp_res[i][0] =='(' and temp_res[i+1][0] =='(' : 
                good_res.append(f'({temp_res[i]+temp_res[i+1]})*')
            elif not(temp_res[i][0] =='(' and temp_res[i-1][0] =='(') : 
                good_res.append(temp_res[i])
        
        if not(temp_res[i+1][0] =='(' and temp_res[i][0] =='(') :
            good_res.append(temp_res[i+1])  
        res.append(good_res[1:])
    return(res)               





def refactor(results) :
    # For each end_path we have a sub regex
    # We add greatest_common_prefix + [(fin_mot1|fin_mot2)] to the list, then we iterate again until we got no common prefix
    liste = results.copy()
    res = []
    while liste :
        word = liste[0]
        prefix = []
        new_word = []
        temp = 0
        for other_word in liste[1:] :
            # use commonprefix to get the element (and if there is one) who can be factorized the most with the current element
            if len(os.path.commonprefix([word,other_word])) > len(prefix) :
                prefix = os.path.commonprefix([word,other_word])
                temp = liste.index(other_word)      
        if prefix :
            if not word[len(prefix):] : #if full match, parenthesis for prefix of more than one character
                if len(liste[temp][len(prefix):]) == 1 : new_word = prefix+ [f'{"".join(liste[temp][len(prefix):])}?']
                else : new_word = prefix + [f'({"".join(liste[temp][len(prefix):])})?']

            elif not liste[temp][len(prefix):] : 
                if len(word[len(prefix):]) == 1 : new_word = prefix + [f'{"".join(word[len(prefix):])}?']
                else : new_word = prefix + [f'({"".join(word[len(prefix):])})?']
            
            else :       
                new_word = prefix + [f'({"".join(word[len(prefix):])}|{"".join(liste[temp][len(prefix):])})'] 
            liste.pop(temp)
            liste[0] = new_word
        else : #no common prefix so start again with next word
            res+= word + ['|']
            liste.pop(0) 

    finished =  res[:-1] #last item is |  
    return finished


def optimize(regex) : 
    word = regex
    res = '^('
    i = 0
    while i < len(regex)-1 :
        k = i
        while  word[i+1] == word[i]:
             if i < len(regex) : i += 1
        if word[i+1] == word[i] + '*' :
                i+=1
                if i == k+1 : res += word[i][:-1] + '+'
                else : res += fr'{word[i][:-1]}{{{i-k+1},}}'
        elif i != k :  res  += word[i] + '{' + str(i-k+1) + '}'     
        else : res += word[i]
        i += 1

    return res + word[-1] + ')$'

def optimize(regex) : 
    #add +, {}, {x,} to regex
    word = regex
    res = '^('
    i = 0
    # i is the position. Does not iterate one by one cause we group identical el with k
    while i < len(regex)-1 :
        k = i
        while  word[i+1] == word[i]:
             if i < len(regex) : i += 1
        if word[i+1] == word[i] + '*' :
                i+=1
                if i == k+1 : res += word[i][:-1] + '+'
                else : res += fr'{word[i][:-1]}{{{i-k+1},}}'
        elif i != k :  res  += word[i] + '{' + str(i-k+1) + '}'     
        else : res += word[i]
        i += 1

    return res + word[-1] + ')$'

def find_language(automaton) :
    # just return the regex into a mathematically correct language
    auto = q1.get_good_type(automaton,'dict')
    return f'{{w ∈ {{{", ".join(auto["alphabet"])}}}| w satisfait {find_regex(auto)}}}'



def is_automate_equivalent(automaton1,automaton2) :
    dict1 = q1.get_good_type(q12.minimal_automaton(automaton1),'dict')
    dict2 = q1.get_good_type(q12.minimal_automaton(automaton2),'dict')
    alphabet = dict1['alphabet']

    # eliminate trivial False case
    if  alphabet != dict2['alphabet']:
        return False
    
    # could be faster with regex below but not good enough as today
    # regex1 = find_regex(dict1)
    # regex2 = find_regex(dict2)
    # if regex1 == regex2 :
        # return True

    words1 = generate_words(dict1,len(dict1['states']*len(alphabet))*len(dict1['transitions'])//2) # arbitrary number words wanted. could be shorter
    words2 = generate_words(dict2,len(dict2['states']*len(alphabet))*len(dict2['transitions'])//2)
    for word in set(words1) :
        if not q2.is_word_recognized(dict2, word) :
            if q2.is_word_recognized(dict1,word) : #no longer needed but reenforce safety
                return False

    for word in set(words2) :
        if not q2.is_word_recognized(dict1, word) :
            if q2.is_word_recognized(dict2,word) : #no longer needed but reenforce safety
                return False
    return True  
    
def generate_words(dict, number_words_wanted) :
    res = []
    while len(set(res)) < number_words_wanted  or len(res) < number_words_wanted*5 :
        current_word = []
        current_state = dict['initial_state']
        while len(current_word) < len(dict['states'] * len(dict['alphabet']))  :

            if current_state in dict['final_states'] : # valid word for this automaton
                res.append(''.join(current_word))
                # case of a final state unescapable
                if current_state not in [transi[0] for transi in dict['transitions']] :
                    break   #to escape

            #randomly select a letter to generate a correct word
            next_letter = random.choice(dict['alphabet'])
            next_state = q1.is_transition_valid(dict, next_letter,current_state)
            if  next_state : #check letter correct
                current_word.append(next_letter)
                current_state = random.choice(next_state) # case not determinist, multiple possibilities          
    return res


# 3 petis print pour les 3 questions :

# print(find_language(test.auto8))
 
# print(find_regex(test.auto9))

