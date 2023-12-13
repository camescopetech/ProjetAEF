import automaton_q1 as q1
import pandas as pd
import re
import automatons_tests as test
import os


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
        # print(len(word)) 

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
        # print(res)
        if df.final_states.loc[str(state)] : #inutile si automate émondé
            res.append(word+'$')
        stack.pop(0) 
    print(res)           
    return good_regex(res)        


def good_regex(regex) :
    res = '^('
    for reg in regex :
        letter_list = []
        letters = re.findall(r'\(.*?\)',reg)
        for letter in letters :
            letter_list.append(letter[1:-1])
        i = 0    
        print(letter_list)
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

    return res[:-1] + ')$'

# print(find_regex(test.auto1)) 

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
    # print(regex1,regex2)
    words1 = generate_words(automaton1,alphabet)
    words2 = generate_words(automaton2,alphabet)
    # print(words1 + words2)
    for word in set(words1+words2) :
        # print(word)
        if bool(re.match(regex1, word)) != bool(re.match(regex2, word)) :
            return False
    return True  
    
def generate_words(automaton,alphabet) : #random genretion not efficient and too long
    df = q1.get_good_type(automaton, 'dataFrame')
    words = []
    stack =[(df[df.initial_state == True].index[0],'',df[df.initial_state == True].index[0])]

    while stack :
        state = stack[0][0]
        precedent_state = stack[0][2]
        word = stack[0][1]
        suite = []
        # print(precedent_state) 

        for letter in alphabet :
            next_state = q1.is_transition_valid(df, str(letter), str(state))
            if next_state :
                if next_state[0] == precedent_state :
                    df.loc[precedent_state,word[-1]] = q1.null_transition
                    # print(df)
                    stack.append((next_state[0],word[:-1],state))
                    for k in range(1,df.shape[0]+1) :
                        stack.append((next_state[0],word+letter*k,state))
                else :   
                    suite += next_state[0]
                    # print(word+letter)
                    stack.append((next_state[0],word+letter,state))
        if suite == [] :
            # print(res)
            words.append(word)
        stack.pop(0)        
    return words  
   

#La fonction ci-dessous marche uniquement pour les chemins directs et les etats finaux dans les boucles   
def find_regex2(automaton) : #automaton must be determinist, stack of tuple(state, word,marked). Looks like a BFS

    res = []
    df = q1.get_good_type(automaton, 'dataFrame')
    alphabet = list(df.columns)[:-2]
    fin_states = list(df[df.final_states == True].index)

    stack =[(df[df.initial_state == True].index[0],[],[])]

    while stack :
        print(stack)
        state = stack[0][0]
        path = stack[0][2]
        word = stack[0][1]
        # print(word,path) 

        for letter in alphabet :
            # print(word)
            # print(letter,state)
            next_state = q1.is_transition_valid(df, str(letter), str(state))
            # print(next_state)
            if next_state :
                # print(next_state,precedent_state)
                if next_state[0] in path : #Cas où on boucle
                    debut_boucle = path.index(next_state[0])
                    # print(debut_boucle)
                    if debut_boucle == len(word)-1 and df.final_states.loc[str(state)]:
                        Q = word.copy()
                        Q.append(letter + '*')
                        res.append(Q)    
                    else :     
                        Q = word[:debut_boucle+1]         # rewrite 4 lines below
                        # word.append(letter)
                        if len(word[debut_boucle+1:]) == 0 : P = letter+'*'
                        else : P = f'({"".join(word[debut_boucle+1:]) + letter})*'
                        # print('q = ' ,Q,'p = ',P)
                        # print(Q)
                        Q.append(P)
                        fin = []
                        fins = []
                        i=0
                        for letter in word[debut_boucle:] :   
                            
                            fin.append(letter)
                            print('stat',path[debut_boucle + i],path)
                            if path[debut_boucle + i] in fin_states : 
                                # print('lamerde',list(df[df.final_states == True].index))
                                # print('fins: ' ,Q + fin)
                                fins.append(Q + fin)
                            i+=1    
                        now = refactor(fins)
                        res.append(now)       
                else :   
                    # print(word+letter)
                    # path.append(next_state[0])
                    # word.append(letter)
                    stack.append((next_state[0],word+list(letter),path+next_state))
                    # if df.final_states.loc[str(state)] : #inutile si automate émondé
                    #     res.append(word)
                    #     print('res',word)
            else : 
                if state in fin_states : #works
                        if word not in res : 
                            res.append(word)
                            # print('res',word)
        stack.pop(0) 
    print(res)    
    # print(refactor(res) 
    # print(optimize(res))          
    return optimize(res) 

# print(q1.get_good_type(test.auto8,'dataFrame').final_states.loc['q6'])

#(aba|abc|abcd|a(c b a)*a|a(c b a)*ac|a(c b a)*acb|a(b c d a)*a|a(b c d a)*ab|a(b c d a)*abc|a(b c d a)*abcd)

# backup :
# fin = []
#                         fins = []
#                         for stat in word[debut_boucle:] :   
#                             fin.append(stat)
#                             if stat in df[df.final_states == True] : 
#                                 # print( Q + fin)
#                                 res.append(Q + fin)
    




def refactor(results) :
    # print(results)
    #utiliser commonprefix.Passer dans la liste et trouver le mots avec le plus grand prefixe commun.
    # Dépiler le mot des mots à comprimer
    # Le mot à ajouter est la liste commune + [(fin_mot1|fin_mot2)]
    # On garde le nouveau pour le comparer à tous ceux qui commencent pareil. 
    # On l'ajoute à une liste finale seulement quand commonprefix retourne [] avec tous les mots restants.
    liste = results.copy()
    res = []
    while liste :
        # print(res)
        word = liste[0]
        prefix = []
        new_word = []
        temp = 0
        
        # for el in liste :
        #     print('el', el)
        #     if type(el[0]) == list : el = el[0]
        for other_word in liste[1:] :
            # print('word',word,'other_word', other_word,'liste', liste)
        
            if len(os.path.commonprefix([word,other_word])) > len(prefix) :
                # print(prefix)
                prefix = os.path.commonprefix([word,other_word])
                temp = liste.index(other_word)
        # print(prefix,'ici')        
        if prefix :
            if not word[len(prefix):] : 
                print(word[len(prefix):])
                if len(liste[temp][len(prefix):]) == 1 : new_word = prefix+ [f'{"".join(liste[temp][len(prefix):])}?']
                else :new_word = prefix+ [f'({"".join(liste[temp][len(prefix):])})?']
            elif not liste[temp][len(prefix):] : 
                if len(word[len(prefix):]) == 1 : new_word = prefix + [f'{"".join(word[len(prefix):])}?']
                else : new_word = prefix + [f'({"".join(word[len(prefix):])})?']
            else :       
                new_word = prefix + [f'({"".join(word[len(prefix):])}|{"".join(liste[temp][len(prefix):])})'] # doit etre liste est str actuellement
            # print('new_word :',new_word)
            liste.pop(temp)
            liste[0] = new_word
            # print('liste',liste)
        else :
            # print('word',word)
            
            res+= word
            # print('res', res)      
            # liste.pop(temp) 
            liste.pop(0) 
    return res




def optimize(regex) : 
    res = '^('
    for reg in regex :
        word = reg
        # print(word)
        i = 0
        while i < len(word) :
            k = i
            current_letter = word[k]

            while i <len(word)-1 and word[i+1] == current_letter :
                i+=1

            if  i < len(word)-1 and word[i+1] == '*' :
                if i-k == 1 : res += current_letter + '+'
                elif i == k : res += current_letter + '*'
                else : res += fr'{current_letter}{{{i-k},}}'
                i+=1

            else : 
                if i == k :  res += current_letter
                else : res  += current_letter + '{' + str(i-k+1) + '}'

            i += 1      
        res+= '|'

    return res[:-1] + ')$'




    
def good_regex2(regex) :
    # Should do : recognize if a paterns happens multiple times in a row. Adjust regex with +,{n},{n,}
    res = '^('
    for reg in regex :
        letter_list = reg.copy()
        # gérer ici les *

        pattern_size = len(letter_list)//2
        while pattern_size > 0 :     
            # gérer les répétitions de lettres ici
            # générer toutes les sous listes de taille pattern_size

            pattern_size -= 1
        res+= '|'
    # essayer ensuite de factoriser ici
    # comparaison entre les sub regex
    return res[:-1] + ')$'

# print(find_regex2(test.auto8))
# print(find_regex(test.auto1))
# print(good_regex2(find_regex2(test.auto1)))


    
def generate_words(automaton,alphabet) : #random genretion not efficient and too long
    df = q1.get_good_type(automaton, 'dataFrame')
    words = []
    stack =[(df[df.initial_state == True].index[0],'',df[df.initial_state == True].index[0])]

    while stack :
        state = stack[0][0]
        precedent_state = stack[0][2]
        word = stack[0][1]
        suite = []
        # print(precedent_state) 

        for letter in alphabet :
            next_state = q1.is_transition_valid(df, str(letter), str(state))
            if next_state :
                if next_state[0] == precedent_state :
                    df.loc[precedent_state,word[-1]] = q1.null_transition
                    # print(df)
                    stack.append((next_state[0],word[:-1],state))
                    for k in range(1,df.shape[0]+1) :
                        stack.append((next_state[0],word+letter*k,state))
                else :   
                    suite += next_state[0]
                    # print(word+letter)
                    stack.append((next_state[0],word+letter,state))
        if suite == [] :
            # print(res)
            words.append(word)
        stack.pop(0)        
    return words  
   

# print(generate_words(q1.df_auto_deter,['a','b']))
# old
# for _ in range(10):
#     print(generate_word(['a','b','c','d']))    


# print(is_automate_equivalent(q1.automate_deter,q1.df_auto_deter))


# print(find_regex(test.auto2))

def find_regex_4(automaton) :
    # changer d'approche, identifie. Il faut verifier que les cycles imbriquées ne soit pas empruntés plusieurs fois. Ensuite on fait juste les chemins qui mènent au finals states
    
    # on cherche les chemins sans boucle qui mènent à un état final dans le but d'obtenir une liste qui va droit à l'état final. 
    # Ensuite, on passe dans les etats et on rajoute des les lettres des boucles avec *.
    # En cas de boucle imbriqué,
    # Regarder si la boucle ne démare pas comme le path fini.
    # A chaque état dans la boucle, on vérifie si l'état n'est pas membre d'une autre boucle


    # Large apres pavé au dessus
    # On cherche les boucles, on cherche les chemins qui finissent depuis les etats, on bricole
    # schéma : si des boucles démarre au meme endroit : (1?2?)*, si boucle démarre dans un état d'une boucle : (1a 2* 1b)*
    #Pour le moment on peut mettre des parenthese a chaque boucle ajouté

    df = q1.get_good_type(automaton, 'dataFrame')
    alphabet = list(df.columns)[:-2]
    cycles = find_cycle(df) # sort les boucles dans le df

    state = df[df.initial_state == True].index[0]
    paths = end_path(df,state)
    # print('paths', paths[0][1])
    res = []

    for path in paths :

        word = []
        current_cycles = []

        states_full = path[0]
        letters_full = path[1]

        #parlons de gestion des cycles : dès qu'on en trouve un, il faut regarder si il en entraine un autre, qu'il faut imbriquer dedans, et ainsi de suite. 
        # Une fois un cycle emprunté, il ne faut plus le prendre en compte.
        # Il faut écrire (1a (2a3(...)*2b)* 1b)*
        # Potentiel introduction du ? pour des cycles démarrant du même état
        # On met au début de la liste à chaque fois qu'on trouve une boucle, qu'on ajoute en entiers directement pour conserver l'ordre 
        stack = [('q1','start',True)]
        for i in range(len(states_full)) :
            stack.append((states_full[i],letters_full[i],True))
        #maitenant : il faut réinitialiser les cycles pour qu'il puissent être pris à chaque étape de l'avancement vers le mots final non bouclé    
        # intial_stack = stack.copy()

        while stack :

            # print('stack', stack)
            letter = stack[0][1]
            current_state = stack[0][0]
            is_default_path = stack[0][2]
            # print(is_default_path)
            if is_default_path :
                current_cycles = []

            # print('states',states, 'letters', letters)
            
            
            # print('letters' , letter)
            # print(type(states[0]))
            stack.pop(0)

            if current_state :
                for cycle in cycles :
                    #reste écriture de la regex à faire
                    temp_word = []
                    if current_state in cycle[0] and cycle not in current_cycles : #nouveau cycle trouvé
                      # print('iciciccezrgfze')
                        current_cycles.append(cycle)
                        # temp_word = []
                        debut_cycle = cycle[0].index(current_state)
                        for i in range(len(cycle[0])):
                             # print((debut_cycle+i)%len(cycle))
                             # print(len(cycle))
                            stack.insert(i,(cycle[0][(debut_cycle+i)%len(cycle[0])],cycle[1][(debut_cycle+i)%len(cycle[0])],False))
                            # print('la', cycle[1][(debut_cycle+i)%len(cycle[0])], cycle)
                            # temp_word.append(cycle[1][(debut_cycle+i)%len(cycle[1])])

                        #idée : a la fin de la boucle for, ajoute * + taille de la boucle + 1e, 2e, 3e... boucle. A la restitution, on regarde si * dans les taille de boucle caracteres precedant. Si oui boucle imbriqué
                        # Il faut impérativement traité la boucle la plus imbriquée en premier

                        stack.insert(len(cycle[0]),('False',['*',len(cycle[0]) ,len(current_cycles)], False))

                        # word.append('('+''.join(temp_word)+')*')
                # if not temp_word :
                     # print('letters', letters)
                    # word.append(letters[0])   
            
            word.append(letter) 

        res.append(word)
        # break #debug line
    # print(star(res))
    return star(res)    

def star(result) :
    # remplacer les cycles par un el de la liste. Un el meme pour plusieurs cycles imbriquées. On repère un cycle par un el qui est une liste
    res = []
    
    for liste in result :
        temp_res = []
        for i in range(len(liste)) :
            current_boucle = []
            # print('temp res', temp_res)
            if type(liste[i]) == list :
                
                len_boucle = liste[i][1] # #nono traiter la boucle avec le nb_max en premier
                # print('len_boucle',len_boucle)
                # print(temp_res[-len_boucle:],'i',i)
                k=0
                for el in temp_res[-len_boucle:] :
                    if el[0] =='(' : 
                        k+=1

                current_boucle = f'({"".join(temp_res[-(len_boucle+k):])})*'
                # print('boucle', current_boucle)
                temp_res = temp_res[:(-len_boucle-k)]
                temp_res.append(current_boucle)
            else : 
                temp_res.append(liste[i]) 
        # print('temp_res', temp_res)
        # 2 boucles d'afilée dans une seule boucle
        good_res = []
        for  i in range(len(temp_res)-1) :
            # print(good_res)
            if temp_res[i][0] =='(' and temp_res[i+1][0] =='(' :
                good_res.append(f'({temp_res[i]+temp_res[i+1]})*')
            elif    not(temp_res[i][0] =='(' and temp_res[i-1][0] =='(') : 
                good_res.append(temp_res[i])
        if not(temp_res[i+1][0] =='(' and temp_res[i][0] =='(') :
            good_res.append(temp_res[i+1])  
        res.append(good_res[1:])
        # print('res', res,'good_res',good_res)
    return(res)               




def find_cycle(automaton) :
    # pour chaque état, dresser la liste des transitions possibles
    # si l'on arrive à un état précédemment croisé,ajouté dans une liste des boucles une liste contenant les etats de la boucle (et mots ? )   
    df = q1.get_good_type(automaton, 'dataFrame')
    alphabet = list(df.columns)[:-2]
    cycles_found = []# print(find_regex2(test.auto8))
    sorted_cycles = []


    stack =[(df[df.initial_state == True].index[0],[],[])] # pour l'instant pas d'interet pour les mots formés, juste states <-- maintenant faut rajouter ça
    while stack :
        # print(stack)
        curr_state = stack[0][0]  
        path = stack[0][1]
        letters_list =stack[0][2]
        for letter in alphabet :
            next_state = q1.is_transition_valid(df, letter, curr_state)
            if  next_state :
                if next_state[0] in path :
                    debut_cycle = path.index(next_state[0])
                    cycle = list(path[debut_cycle:])
                    if sorted(cycle) not in sorted_cycles :
                        cycles_found.append((cycle,letters_list[debut_cycle+1:]+[letter]))
                        sorted_cycles.append(sorted(cycle))
                else : 
                    # print(path+list(next_state[0]))
                    stack.append((next_state[0],path+ next_state,letters_list+[letter]))
        stack.pop(0)            
    return cycles_found

# print(find_cycle(test.auto8))  

def end_path(df,state) : #doit trouver les moyens de finir sans boucle, retourne une liste où chaque element et la liste des lettres pour finir

    alphabet = list(df.columns)[:-2]
    stack = [(state,[state],[])]
    fin_state = list(df[df.final_states == True].index)
    res = []
    while stack :
        # print('stack :' , stack)
        current_state = stack[0][0]
        path = stack[0][1]
        letters_list = stack[0][2]

        if current_state in fin_state : #condition de fin trouvée
            res.append((path[1:],letters_list))

        #états suivant    
        for letter in alphabet :
            next_state = q1.is_transition_valid(df, letter, current_state)
            if  next_state :
                if next_state[0] not in path :
                    stack.append((next_state[0], path + next_state,letters_list + [letter]))
        stack.pop(0)        
    return  res          




def refactor2(results) :
    # print(results)
    #utiliser commonprefix.Passer dans la liste et trouver le mots avec le plus grand prefixe commun.
    # Dépiler le mot des mots à comprimer
    # Le mot à ajouter est la liste commune + [(fin_mot1|fin_mot2)]
    # On garde le nouveau pour le comparer à tous ceux qui commencent pareil. 
    # On l'ajoute à une liste finale seulement quand commonprefix retourne [] avec tous les mots restants.
    liste = results.copy()
    res = []
    while liste :
        # print(res)
        word = liste[0]
        prefix = []
        new_word = []
        temp = 0
        # print(word)
        # for el in liste :
        #     print('el', el)
        #     if type(el[0]) == list : el = el[0]
        for other_word in liste[1:] :
            # print('word',word,'other_word', other_word,'liste', liste)
        
            if len(os.path.commonprefix([word,other_word])) > len(prefix) :
                # print(prefix)
                prefix = os.path.commonprefix([word,other_word])
                temp = liste.index(other_word)
        # print(prefix,'ici')        
        if prefix :
            if not word[len(prefix):] : 
                print(word[len(prefix):])
                if len(liste[temp][len(prefix):]) == 1 : new_word = prefix+ [f'{"".join(liste[temp][len(prefix):])}?']
                else :new_word = prefix+ [f'({"".join(liste[temp][len(prefix):])})?']
            elif not liste[temp][len(prefix):] : 
                if len(word[len(prefix):]) == 1 : new_word = prefix + [f'{"".join(word[len(prefix):])}?']
                else : new_word = prefix + [f'({"".join(word[len(prefix):])})?']
            else :       
                new_word = prefix + [f'({"".join(word[len(prefix):])}|{"".join(liste[temp][len(prefix):])})'] # doit etre liste est str actuellement
            # print('new_word :',new_word)
            liste.pop(temp)
            liste[0] = new_word
            # print('liste',liste)
        else :
            # print('word',word)
            
            res+= word
            # print('res', res)      
            # liste.pop(temp) 
            liste.pop(0) 
    finished = '^' + ''.join(res) + '$'       
    return finished



# print(end_path(q1.get_good_type(test.auto1,'dataFrame'),'0'))

# print(find_regex_4(test.auto9))
#pour auto 8 le meilleur résultat est ^(a(cba)*bcd)*(abc|aba|acd)$   (on peut un peu plus factoriser mais tres ok)
#auto 9 : (a(cdd)*(bad)*cd)*(cba)*(abc?|abd|acd)
print(refactor2(find_regex_4(test.auto9)))

# print(compile(refactor2(find_regex_4(test.auto9))))         




