import automaton_q1 as q1
import pandas as pd
import automatons_tests as test
import os

def find_regex(automaton) :
    # Il faut verifier que les cycles imbriquées ne soit pas empruntés plusieurs fois. Ensuite on fait juste les chemins qui mènent au finals states
    
    # on cherche les chemins sans loop qui mènent à un état final dans le but d'obtenir une liste qui va droit à l'état final. 
    # Ensuite, on passe dans les etats et on rajoute des les lettres des loops avec *.
    # En cas de loop imbriqué,
    # Regarder si la loop ne démare pas comme le path fini.
    # A chaque état dans la loop, on vérifie si l'état n'est pas membre d'une autre loop


    # Large apres pavé au dessus
    # On cherche les loops, on cherche les chemins qui finissent depuis les etats, on bricole
    # schéma : si des loops démarre au meme endroit : (1?2?)*, si loop démarre dans un état d'une loop : (1a 2* 1b)*
    #Pour le moment on peut mettre des parenthese a chaque loop ajouté

    df = q1.get_good_type(automaton, 'dataFrame')
    cycles = find_cycle(df) # sort les loops dans le df

    ini_state = df[df.initial_state == True].index[0]
    paths = end_path(df,ini_state)
    res = []
    for path in paths :

        current_natural_path_index = 0
        word = []
        current_cycles = []

        states_full = path[0]
        letters_full = path[1]

        #parlons de gestion des cycles : dès qu'on en trouve un, il faut regarder si il en entraine un autre, qu'il faut imbriquer dedans, et ainsi de suite. 
        # Une fois un cycle emprunté, il ne faut plus le prendre en compte.
        # Il faut écrire (1a (2a3(...)*2b)* 1b)*
        # Potentiel introduction du ? pour des cycles démarrant du même état
        # On met au début de la liste à chaque fois qu'on trouve une loop, qu'on ajoute en entiers directement pour conserver l'ordre 
        stack = [(ini_state,'start',False)]
        for i in range(len(states_full)) :
            stack.append((states_full[i],letters_full[i],True))
        #maitenant : il faut réinitialiser les cycles pour qu'il puissent être pris à chaque étape de l'avancement vers le mots final non bouclé    
        # DERNIER TRUC A FAIRE : ON RENTRE PAS DANS UN CYCLE SI L'ETAT SUIVANT EST CELUI DU PATH NON loop
        while stack :

            letter = stack[0][1]
            current_state = stack[0][0]
            next_default_state = stack[0][1]
            is_default_path = stack[0][2]
            if is_default_path :
                current_cycles = []

            if is_default_path :
                current_natural_path_index += 1
            

            stack.pop(0)

            if current_state :
                for cycle in cycles :

                    if current_state in cycle[0] and cycle not in current_cycles : #nouveau cycle trouvé
                      # ICI METTRE IF AVEC PROCHAIN ETAT PAS DANS LECELUI DU PATH
                    
                        current_cycles.append(cycle)
                        # temp_word = []
                        debut_cycle = cycle[0].index(current_state)
                        # on ne prend pas le cycle si pas prochain. On prend si dernier etat ou cycle demarre pas par suite path
                        if (current_natural_path_index+1 >= len(states_full)) or cycle[0][(debut_cycle+1)%len(cycle[0])] != path[0][(current_natural_path_index+1)]:



                            for i in range(len(cycle[0])):

                                stack.insert(i,(cycle[0][(debut_cycle+i)%len(cycle[0])],cycle[1][(debut_cycle+i)%len(cycle[0])],False))


                        #idée : a la fin de la loop for, ajoute * + taille de la loop + 1e, 2e, 3e... loop. A la restitution, on regarde si * dans les taille de loop caracteres precedant. Si oui loop imbriqué
                        # Il faut impérativement traité la loop la plus imbriquée en premier

                            stack.insert(len(cycle[0]),('False',['*',len(cycle[0]) ,len(current_cycles)], False))

            word.append(letter) 

        res.append(word)

    return optimize(refactor(star(res)))    



def find_cycle(automaton) :
    # pour chaque état, dresser la liste des transitions possibles
    # si l'on arrive à un état précédemment croisé,ajouté dans une liste des loops une liste contenant les etats de la loop (et mots ? )   
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
    #utiliser commonprefix.Passer dans la liste et trouver le mots avec le plus grand prefixe commun.
    # Dépiler le mot des mots à comprimer
    # Le mot à ajouter est la liste commune + [(fin_mot1|fin_mot2)]
    # On garde le nouveau pour le comparer à tous ceux qui commencent pareil. 
    # On l'ajoute à une liste finale seulement quand commonprefix retourne [] avec tous les mots restants.
    liste = results.copy()
    res = []
    while liste :
        word = liste[0]
        prefix = []
        new_word = []
        temp = 0
        for other_word in liste[1:] :
        
            if len(os.path.commonprefix([word,other_word])) > len(prefix) :
                prefix = os.path.commonprefix([word,other_word])
                temp = liste.index(other_word)      
        if prefix :
            if not word[len(prefix):] : 
                if len(liste[temp][len(prefix):]) == 1 : new_word = prefix+ [f'{"".join(liste[temp][len(prefix):])}?']
                else :new_word = prefix+ [f'({"".join(liste[temp][len(prefix):])})?']
            elif not liste[temp][len(prefix):] : 
                if len(word[len(prefix):]) == 1 : new_word = prefix + [f'{"".join(word[len(prefix):])}?']
                else : new_word = prefix + [f'({"".join(word[len(prefix):])})?']
            else :       
                new_word = prefix + [f'({"".join(word[len(prefix):])}|{"".join(liste[temp][len(prefix):])})'] # doit etre liste est str actuellement
            liste.pop(temp)
            liste[0] = new_word
        else :
            res+= word + ['|']
            liste.pop(0) 

    finished =  res[:-1]   
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

def find_language(automaton) :
    # just return the regex into a mathematically correct language
    auto = q1.get_good_type(automaton,'dict')
    return f'{{w ∈ {{{", ".join(auto["alphabet"])}}}| w satisfait {find_regex(auto)}}}'


# 2 petis print pour les 2 questions :

# print(find_language(test.auto8))
 
# print(find_regex(test.auto8))
