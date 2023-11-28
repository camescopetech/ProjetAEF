import automaton_q1 as q1
import pandas as pd
import re
import random
import time


def find_regex(automaton) : #automaton must be determinist, stack of tuple(state, word,precedent_state) 

    res = []
    df = q1.get_good_type(automaton, 'dataFrame')
    alphabet = list(df.columns)[:-2]

    stack =[(df[df.initial_state == True].index[0],'^',df[df.initial_state == True].index[0])]

    while stack :

        state = stack[0][0]
        precedent_state = stack[0][2]
        word = stack[0][1]
        suite = []
        # print(precedent_state) 

        for letter in alphabet :
            # print(letter,state)
            next_state = q1.is_transition_valid(df, str(letter), str(state))
            # print(next_state)
            if next_state :
                # print(next_state,precedent_state)
                # if letter == word[-1] and str(state) == next_state[0]:
                if next_state[0] == precedent_state :
                    word += '(*)'
                else :   
                    suite += next_state[0]
                    # print(word+letter)
                    stack.append((next_state[0],word+f'({letter})',state))
        if suite == [] :
            # print(res)
            if df.final_states.loc[str(state)] : #inutile si automate émondé
                res.append(word+'$')
        stack.pop(0)        
    return good_regex(res)        


def good_regex(regex) :
    res = '('
    for reg in regex :
        letter_list = []
        letters = re.findall(r'\(.*?\)',reg)
        for letter in letters :
            letter_list.append(letter[1:-1])
        i = 0    
        while i < len(letter_list) :
            k = i
            current_letter = letter_list[k]

            while i <len(letter_list)-1 and letter_list[i+1] == current_letter :
                i+=1

            if  i < len(letter_list)-1 and letter_list[i+1] == '*' :
                if i-k == 1 : res += current_letter + '+'
                elif i == k : res += current_letter + '*'
                else : res += fr'{current_letter}{{{i-k},}}'
                i+=1

            else : 
                if i == k :  res += current_letter
                else : res  += current_letter + '{' + str(i-k+1) + '}'

            i += 1      
        res+= '|'

    return res[:-1] + ')'

print(find_regex(q1.automate_deter)) 

# print(good_regex(['^(a)(a)(*)$', '^(b)(b)(b)(*)$', '^(b)(a)(*)(b)$']))

def find_language(automaton) :
    auto = q1.get_good_type(automaton,'dict')
    return f'{{w ∈ {{{", ".join(auto["alphabet"])}}}| w satisfait {find_regex(auto)}}}'

# print(find_language(q1.automate_deter))

def is_automate_equivalent(automaton1,automaton2) :
    dict1 = q1.get_good_type(automaton1, 'dict')
    dict2 = q1.get_good_type(automaton2, 'dict')
    alphabet = dict1['alphabet']
    if  alphabet != dict2['alphabet'] :
        return False
    
    regex1 = find_regex(dict1)
    regex2 = find_regex(dict2)
    if regex1 == regex2 :
        return True

    n = 0
    start = time.time()
    while time.time() < start +10 :
        exemple = generate_word(alphabet)
        if bool(re.match(regex1, exemple)) != bool(re.match(regex2, exemple)) :
            return False
        n+=1
    return True    

    
def generate_word(alphabet) :
    max_len = 10 * len(alphabet)
    new_word = ''
    while random.random() > len(new_word) / max_len :
        new_word += random.choice(alphabet)
    return new_word    

# for _ in range(10):
#     print(generate_word(['a','b','c','d']))    


print(is_automate_equivalent(q1.automate_deter,q1.df_auto_deter))