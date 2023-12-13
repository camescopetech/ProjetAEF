# ecrire plein d'automates avec leur caractéristiques testant des randoms trucs
import automaton_q1 as q1
import pandas as pd


#deterministe, simple
auto1 = {
    'alphabet': ['a','b'],
    'states' : ['0','1','2','3'],
    'initial_state' : '0',
    'final_states' : ['2','3'],
    'transitions': [
        ['0','3','a'],
        ['0','1','b'],

        ['1','2','b'],
        ['1','1','a'],

        ['3','3','a']
    ]
}

#déterministe, tableau equivalent a auto1
auto2 = pd.DataFrame(index = ['0','1','2','3'], data = {
    'a': ['3','1',q1.null_transition,'3'],
    'b' : ['1','2',q1.null_transition,q1.null_transition],
    'initial_state': [True,False,False,False],
    'final_states':[False,False,True,True]
})

# Non deterministe, 2 fois la meme transi
auto3 = {
    'alphabet': ['a','b'],
    'states' : ['0','1','2','3'],
    'initial_state' : '0',
    'final_states' : ['2','3'],
    'transitions': [
        ['0','0','b'],
        ['0','1','a'],
        ['0','3','a'],
        ['0','3','a'],

        ['1','1','b'],
        ['1','2','a'],
        ['1','2','b'],

        ['2','2','a'],
        ['2','2','b'],

        ['3','3','a']
    ]
}
# equivalent a auto3 sous forme de dataFrame
auto4 = pd.DataFrame(index = ['0','1','2','3'], data = {
    'a': ['1, 3','2','2','3'],
    'b' : ['0','1, 2','2',q1.null_transition],
    'initial_state': [True,False,False,False],
    'final_states':[False,False,True,True]
})


# très complexe, non deterministe, complet
auto5 = {
    'alphabet': ['a', 'b', 'c', 'd'],
    'states': ['A', 'B', 'C', 'D', 'E'],
    'initial_state': 'A',
    'final_states': ['D', 'E'],
    'transitions': [
        ['A', 'B', 'a'],
        ['A', 'C', 'b'],
        ['A', 'D', 'c'],
        ['A', 'E', 'd'],

        ['B', 'A', 'b'],
        ['B', 'C', 'c'],
        ['B', 'D', 'd'],
        ['B', 'E', 'a'],

        ['C', 'A', 'c'],
        ['C', 'B', 'a'],
        ['C', 'C', 'd'],
        ['C', 'D', 'b'],
        ['C', 'E', 'a'],

        ['D', 'A', 'd'],
        ['D', 'B', 'b'],
        ['D', 'C', 'a'],
        ['D', 'D', 'c'],
        ['D', 'E', 'a'],

        ['E', 'A', 'a'],
        ['E', 'B', 'c'],
        ['E', 'C', 'b'],
        ['E', 'D', 'a'],
        ['E', 'E', 'd']
    ]
}
# =auto 5 deterministe
auto6 = {
    'alphabet': ['a', 'b', 'c', 'd'],
    'states': ['A', 'B', 'C', 'D', 'E'],
    'initial_state': 'A',
    'final_states': ['D', 'E'],
    'transitions': [
        ['A', 'B', 'a'],
        ['A', 'C', 'b'],
        ['A', 'D', 'c'],
        ['A', 'E', 'd'],

        ['B', 'A', 'b'],
        ['B', 'C', 'c'],
        ['B', 'D', 'd'],
        ['B', 'E', 'a'],

        ['C', 'A', 'c'],
        ['C', 'B', 'a'],
        ['C', 'C', 'd'],
        ['C', 'D', 'b'],

        ['D', 'A', 'd'],
        ['D', 'B', 'b'],
        ['D', 'C', 'a'],
        ['D', 'D', 'c'],

        ['E', 'A', 'a'],
        ['E', 'B', 'c'],
        ['E', 'C', 'b'],
        ['E', 'E', 'd']
    ]
}
#automate émondé
auto7 = {
    'alphabet': ['a', 'b'],
    'states': ['q0', 'q1', 'q2'],
    'initial_state': 'q0',
    'final_states': ['q2'],
    'transitions': [
        ['q0', 'q1', 'a'],
        ['q1', 'q2', 'b'],
        ['q2', 'q2', 'a']
    ]
}
#complexe, boucle
auto8 = {
    'alphabet': ['a', 'b','c','d'],
    'states': [ 'q1', 'q2','q3','q4','q5','q6'],
    'initial_state': 'q1',
    'final_states': ['q3','q4','q6'],
    'transitions': [
        ['q1', 'q2', 'a'],
        ['q2', 'q3', 'b'],
        ['q3', 'q4', 'c'],
        ['q4', 'q1', 'd'],
        ['q2', 'q5', 'c'],
        ['q5', 'q1', 'b'],
        ['q5', 'q6', 'd'],
        ['q3', 'q6', 'a'],
    ]
}

#auto8 avec une transition de plus
auto9 = {
    'alphabet': ['a', 'b','c','d'],
    'states': [ 'q1', 'q2','q3','q4','q5','q6'],
    'initial_state': 'q1',
    'final_states': ['q3','q4','q6'],
    'transitions': [
        ['q1', 'q2', 'a'],
        ['q2', 'q3', 'b'],
        ['q3', 'q4', 'c'],
        ['q4', 'q1', 'd'],
        ['q2', 'q5', 'c'],
        ['q5', 'q1', 'b'],
        ['q5', 'q6', 'd'],
        ['q3', 'q6', 'a'],
        ['q6', 'q2', 'd']
    ]
}


