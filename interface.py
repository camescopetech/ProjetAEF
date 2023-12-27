import json
import ast
import tkinter as tk
import math

"""
Convert the automate into a string
@param: json automate
@return: String
"""
def conversion(automate):
    try:

        structure_python = ast.literal_eval(automate)
        chaine_json = json.dumps(structure_python)
        
        return chaine_json
    except (SyntaxError, ValueError) as e:
        #print(f"Erreur lors de la conversion : {e}")
        return None
"""
Check if there are any occurrences in the list of the automate
@param: json automate, String key
@return: Boolean
"""   
def isNoneOccurenceList(automate,key):

    list = automate.get(key, [])

    return len(list) == len(set(list))
"""
Checks if the automaton in string has the right format
@param: json automate
@return: int Corresponds to the success or error of the automaton in the form of a string
"""
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
    #if not initial_state:
    #    return 4

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
    if initial_state not in states:
        return 8
    
    #ERROR9: states must contain final_states
    for final_state in final_states:
        if final_state not in states:
            return 9

    return 0
"""
Groups the transitions
@param: json automate
@result: list of the transition
"""
def regrouper_transitions(automate):
    transitions_regroupees = {}

    for transition in automate["transitions"]:
        etat_depart, etat_arrivee, symbole = transition

        #Créer une clé triée pour chaque paire d'états
        cle = tuple(sorted([etat_depart, etat_arrivee]))

        #Vérifier si la clé existe déjà dans le dictionnaire
        if cle in transitions_regroupees:
            transitions_regroupees[cle].append([etat_depart, etat_arrivee, symbole])
        else:
            transitions_regroupees[cle] = [[etat_depart, etat_arrivee, symbole]]

    #Convertir le résultat en une liste de listes de transitions
    resultat = [transitions for transitions in transitions_regroupees.values()]

    return resultat
"""
Draw the automate into another window
@param: json automate
"""
def drawAutomate(automate):
    fenetre = tk.Tk()
    fenetre.title("Automate Visuel")

    canevas = tk.Canvas(fenetre, width=500, height=300, bg="white")
    canevas.pack()

    #Center of window 
    centre_x = 250
    centre_y = 150

    #Reverse the order of states to start on the right 
    etats_reverse = list(reversed(automate['states']))

    #Draw the states in a circle 
    etats_circles = {}  
    nombre_etats = len(etats_reverse)
    rayon = 80

    for i, state in enumerate(etats_reverse):
        angle = (3 * math.pi / 2) + (2 * math.pi * i) / nombre_etats
        x = centre_x + int(rayon * math.cos(angle))
        y = centre_y + int(rayon * math.sin(angle))

        est_etat_initial = state == automate['initial_state']
        est_etat_final = state in automate['final_states']

        #Draw circle for state
        canevas.create_oval(x - 20, y - 20, x + 20, y + 20, outline="black", fill="white")

        #Adds indicator for initial state (triangle) 
        if est_etat_initial:
            #Adjust the coordinates to place the triangle to the right of the circle
            canevas.create_polygon(x - 20, y, x - 30, y + 10, x - 30, y - 10, fill="black")

        #Add indicator for final state (circle)
        if est_etat_final:
            canevas.create_oval(x - 15, y - 15, x + 15, y + 15, outline="black")

        #Add text for status 
        canevas.create_text(x, y, text=state)

        #Stores circle coordinates in dictionary 
        etats_circles[state] = (x, y)  

    #Draw the transitions 
    rayon = 20
    transGroupList = regrouper_transitions(automate)

    for transGroup in transGroupList:

        
        #If the transition points to the same state, draw a loop 
        if transGroup[0][0] == transGroup[0][1]:

            transition = transGroup[0]

            start_state, end_state, symbol = transition
            x, y = etats_circles[start_state]

            rayonArrow = 10
            xPointeArrow = x + 2*(rayon - rayonArrow)
            canevas.create_text(x + 2*rayon + 10 , y , text=symbol, fill='blue')
            canevas.create_oval(xPointeArrow, y - rayonArrow, x + 2*rayon, y + rayonArrow, outline="black")
            canevas.create_polygon(xPointeArrow, y, xPointeArrow - 5, y + 5, xPointeArrow + 5, y + 5, fill="black")

        else:

            lenGroup = len(transGroup)

            if lenGroup % 2 == 1:

                transition = transGroup[0]

                start_state, end_state, symbol = transition
                x1, y1 = etats_circles[start_state]
                x2, y2 = etats_circles[end_state]

                control_x = (x1 + x2) / 2
                control_y = (y1 + y2) / 2 

                start_x_adjusted = x1 + rayon * math.cos(math.atan2(control_y - y1, control_x - x1))
                start_y_adjusted = y1 + rayon * math.sin(math.atan2(control_y - y1, control_x - x1))
                end_x_adjusted = x2 - rayon * math.cos(math.atan2(y2 - control_y, x2 - control_x))
                end_y_adjusted = y2 - rayon * math.sin(math.atan2(y2 - control_y, x2 - control_x))

                #Arrow between circles
                canevas.create_line(start_x_adjusted, start_y_adjusted, end_x_adjusted, end_y_adjusted, arrow=tk.LAST) 
                canevas.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 10, text=symbol, fill='blue')

                transGroup = transGroup[1:]

            decalage = 30
            clock = 0
            for transition in transGroup:

                start_state, end_state, symbol = transition
                x1, y1 = etats_circles[start_state]
                x2, y2 = etats_circles[end_state]
        
                #Draw an arrow from the circle of the first state to the circle of the second state
                if clock == 0:
                    
                    control_x = (x1 + x2) / 2
                    control_y = (y1 + y2) / 2

                    if x1 == x2:
                        control_x -= decalage
                    else:
                        control_y -= decalage
                
                    canevas.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 10, text=symbol,fill='blue')

                    clock = 1
                else:
                    control_x = (x1 + x2) / 2
                    control_y = (y1 + y2) / 2

                    if x1 == x2:
                        control_x += decalage
                    else:
                        control_y += decalage

                    canevas.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 10, text=symbol,fill='blue')

                    clock = 0
                    decalage += 20

                #Adjust the start and stop position so that the arrows start and end at the circle 
               
                start_x_adjusted = x1 + rayon * math.cos(math.atan2(control_y - y1, control_x - x1))
                start_y_adjusted = y1 + rayon * math.sin(math.atan2(control_y - y1, control_x - x1))
                end_x_adjusted = x2 - rayon * math.cos(math.atan2(y2 - control_y, x2 - control_x))
                end_y_adjusted = y2 - rayon * math.sin(math.atan2(y2 - control_y, x2 - control_x))

                canevas.create_line(start_x_adjusted, start_y_adjusted, control_x, control_y, end_x_adjusted, end_y_adjusted, smooth=tk.TRUE, arrow=tk.LAST)

    fenetre.mainloop()
