#1. Manipuler un AEF :
import pandas
import json
import warnings
# 
# Désactiver tous les avertissements
warnings.filterwarnings("ignore")
import automaton_q1
# 
#2. Vérifier si un mot est reconnu par un AEF.
import recognize_complete_q2_q3_q4 as q2

automate= {     #automate nonComplet
    'alphabet': ['a','b'],
    'states' : ['0','1'],
    'initial_state' : '0',
    'final_states' : ['1'],
    'transitions': [
        ['0','1','a'],
        ['1','0','b'],
    ]
}

automate_non_emonde = {
    'alphabet': ['a', 'b','c'], 
    'states': ['0', '1', '3'], 
    'initial_state': '0', 
    'final_states': ['3'], 
    'transitions': [
        ['0', '1', 'a'], 
        ['0', '3', 'b'], 
        ['0', '3', 'c']
    ]
}

automateEquivalent = {     #automate nonComplet 
    'alphabet': ['a','b'],
    'states' : ['A','B'],
    'initial_state' : 'A',
    'final_states' : ['B'],
    'transitions': [
        ['A','B','a'],
        ['B','A','b']
    ]
}

automate_non_deterministe= {     #automate nonComplet et nonDetermisite
    'alphabet': ['a','b'],
    'states' : ['0','1'],
    'initial_state' : '0',
    'final_states' : ['1'],
    'transitions': [
        ['0','1','a'],
        ['0','1','b'],
        ['0','0','a']
    ]
}

# 
automate_complet = {
    'alphabet': ['a', 'b'], 
    'states': ['0', '1', 'phi'], 
    'initial_state': '0', 
    'final_states': ['1'], 
    'transitions': [['0', '0', 'a'], ['0', '1', 'b'], ['1', 'phi', 'a'], ['1', 'phi', 'b'], ['phi', 'phi', 'a'], ['phi', 'phi', 'b']]}

automate_deterministe = {
    'alphabet': ['a', 'b'], 
    'states': ['0', '0, 1', '1'], 
    'initial_state': '0', 
    'final_states': ['0, 1', '1'], 
    'transitions': [['0', '0, 1', 'a'], ['0', '1', 'b'], ['0, 1', '0, 1', 'a'], ['0, 1', '1', 'b']]}

if(q2.is_word_recognized(automate, "ab") == True) and (q2.is_word_recognized(automate, "ba") == False):
    print("Question 2 test ok")
else :
    print("Erreur test question 2")
# 
# 
#3. Vérifier si un automate est complet.
if (q2.is_complete(automate_complet) == True) and (q2.is_complete(automate) == False):
    print("Question 3 test ok")
else :
    print("Erreur test question 3")
# 
#4. Rendre un automate complet.
test_question_4 = q2.completing(automate)
if (q2.is_complete(test_question_4) == True):
    print("Question 4 test ok")
else :
    print("Erreur test question 4")
# 
#5. Vérifier si un automate est déterministe.
# 
import determinist as q5
# 
if (q5.is_automaton_deterministic(automate_deterministe)[0] == True) and (q5.is_automaton_deterministic(automate_non_deterministe)[0] == False):
    print("Question 5 test ok")
else :
    print("Erreur test question 5")
    # 
#6. Rendre un AEF déterministe
# 
test_question_6 = q5.to_automaton_deterministic(automate)
if (q5.is_automaton_deterministic(test_question_6)[0] == True):
    print("Question 6 test ok")
else :
    print("Erreur test question 6")
    
#7. Réaliser les opérations suivantes sur les AEFs
import automaton_q7 as q7
import automaton_q1 as q1


    #7. Complément d'un AEF
if ((q7.complem_automaton(automate)))['final_states'] != automate['final_states']:
    print("Question 7 COMPLEMENT test ok")
else :
     print("Erreur test question 7 COMPLEMENT")

        #7. Miroir d'un AEF 
        
miroir = ((q7.miroir_automaton(automate)))
conditionTransition ="ok"
for (transition,transitionMiroir) in zip(automate['transitions'],miroir['transitions']):
    if((transition[0] != transitionMiroir[1]) ==True) or ((transition[1] != transitionMiroir[0]) ==True)  or ((transition[2] != transitionMiroir[2]) ==True) :
        conditionTransition = "nonOK"
if (conditionTransition == "ok") and ([automate['initial_state']] == miroir['final_states']) and (automate['final_states'] == miroir['initial_state']):
    print("Question 7 MIROIR test ok")
else :
     print("Erreur test question 7 MIROIR")

    #7. Produit de deux AEF 
    
if (q7.produit_aefs(automate,automate) == {'alphabet': ['a', 'b'], 'states': ['0,0', '0,1', '1,0', '1,1'], 'initial_state': ['0,0'], 'final_states': ["['1'],['1']"], 'transitions': [['0,0', '1,1', 'a'], ['1,1', '0,0', 'b']]}):
    print("Question 7 PRODUIT test ok")
else :
     print("Erreur test question 7 PRODUIT")
    
    
    #7. Concaténation de deux AEF
    
if (q7.concatAEF(automate,automate) == {'alphabet': ['a', 'b'], 'states': ['0', '1', '0', '1'], 'initial_state': '0', 'final_states': ['1'], 'transitions': [['0', '1', 'a'], ['1', '0', 'b'], ['0', '1', 'a'], ['1', '0', 'b']]}):
    print("Question 7 CONCATENATION test ok")
else :
     print("Erreur test question 7 CONCATENATION")

 
#8.Extraire une expression régulière à partir un automate donné
import regex_q8_q9_q10 as q8

import re
if re.match(r'\^.*\$', q8.find_regex(automate)):
        print("Question 8 test ok")
else :
    print("Erreur test question 8")
    
#9. Trouver le langage reconnu par un automate donné
if re.match(r'\{w.*\$}', q8.find_language(automate)):
        print("Question 9 test ok")
else :
    print("Erreur test question 9")

#10. Vérifier si deux automates sont équivalents, i.e. ils reconnaissent les mêmes
#langages.
if (q8.is_automate_equivalent(automate,automateEquivalent) == True):
        print("Question 10 test ok")
else :
    print("Erreur test question 10")

#11. Rendre un automate émondé.
import minimal_q12 as q12
automatonEmonde = q1.table_to_dict(q12.minimal_automaton(automate_non_emonde))
if (automatonEmonde == {'alphabet': ['b', 'c'], 'states': ['0', '3'], 'initial_state': '0', 'final_states': ['3'], 'transitions': [['0', '3', 'b'], ['0', '3', 'c']]}):
        print("Question 11 test ok")
else :
    print("Erreur test question 11")

#12. Rendre un automate minimal.

if (q8.is_automate_equivalent(automate,q12.minimal_automaton(automate)) == True):
        print("Question 12 test ok")
else :
    print("Erreur test question 12")
