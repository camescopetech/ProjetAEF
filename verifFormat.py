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

import tkinter as tk
import math

def regrouper_transitions(automate):
    transitions_regroupees = {}

    for transition in automate["transitions"]:
        etat_depart, etat_arrivee, symbole = transition

        # Créer une clé triée pour chaque paire d'états
        cle = tuple(sorted([etat_depart, etat_arrivee]))

        # Vérifier si la clé existe déjà dans le dictionnaire
        if cle in transitions_regroupees:
            transitions_regroupees[cle].append([etat_depart, etat_arrivee, symbole])
        else:
            transitions_regroupees[cle] = [[etat_depart, etat_arrivee, symbole]]

    # Convertir le résultat en une liste de listes de transitions
    resultat = [transitions for transitions in transitions_regroupees.values()]

    return resultat

def afficher_automate(automate):
    fenetre = tk.Tk()
    fenetre.title("Automate Visuel")

    canevas = tk.Canvas(fenetre, width=500, height=300, bg="white")
    canevas.pack()

    # Calculer le centre du cercle
    centre_x = 250
    centre_y = 150

    # Inverser l'ordre des états pour commencer à droite
    etats_reverse = list(reversed(automate['states']))

    # Dessiner les états en cercle
    etats_circles = {}  # Dictionnaire pour stocker les cercles des états
    nombre_etats = len(etats_reverse)
    rayon = 80

    for i, state in enumerate(etats_reverse):
        angle = (3 * math.pi / 2) + (2 * math.pi * i) / nombre_etats
        x = centre_x + int(rayon * math.cos(angle))
        y = centre_y + int(rayon * math.sin(angle))

        est_etat_initial = state == automate['initial_state']
        est_etat_final = state in automate['final_states']

        # Dessiner cercle pour l'état
        cercle = canevas.create_oval(x - 20, y - 20, x + 20, y + 20, outline="black", fill="white")

        # Ajouter indicateur pour l'état initial (triangle)
        if est_etat_initial:
            # Ajuster les coordonnées pour placer le triangle à droite du cercle
            canevas.create_polygon(x - 20, y, x - 30, y + 10, x - 30, y - 10, fill="black")

        # Ajouter indicateur pour l'état final (cercle)
        if est_etat_final:
            canevas.create_oval(x - 15, y - 15, x + 15, y + 15, outline="black")

        # Ajouter texte pour l'état
        canevas.create_text(x, y, text=state)

        etats_circles[state] = (x, y)  # Stocker les coordonnées du cercle dans le dictionnaire

    # Dessiner les transitions
    
    rayon = 20
    transGroupList = regrouper_transitions(automate)

    for transGroup in transGroupList:

        
        # Si la transition pointe vers le même état, dessiner une boucle
        if transGroup[0][0] == transGroup[0][1]:

            transition = transGroup[0]

            start_state, end_state, symbol = transition
            x1, y1 = etats_circles[start_state]
            x2, y2 = etats_circles[end_state]

            arrow_length = 30  # Ajustez cette valeur pour définir la longueur de la boucle
            arrow_x = x2 + arrow_length * math.cos(math.pi / 4)  # Ajustez l'angle de la boucle selon votre préférence
            arrow_y = y2 + arrow_length * math.sin(math.pi / 4)

            # Dessiner une boucle avec une flèche à l'extrémité
            canevas.create_line(x2, y2, arrow_x, arrow_y, smooth=tk.TRUE, arrow=tk.LAST)
            canevas.create_text((x2 + arrow_x) / 2, (y2 + arrow_y) / 2 - 10, text=symbol, fill='blue')   
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

                canevas.create_line(start_x_adjusted, start_y_adjusted, end_x_adjusted, end_y_adjusted, arrow=tk.LAST)  # Flèche entre les cercles
                canevas.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 10, text=symbol, fill='blue')

                transGroup = transGroup[1:]

            decalage = 30
            clock = 0
            for transition in transGroup:

                start_state, end_state, symbol = transition
                x1, y1 = etats_circles[start_state]
                x2, y2 = etats_circles[end_state]
        
                # Dessiner une flèche du cercle du premier état vers le cercle du deuxième état
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

                # Ajuster la position de départ et d'arrêt pour que les flèches démarrent et finissent au niveau du cercle
               
                start_x_adjusted = x1 + rayon * math.cos(math.atan2(control_y - y1, control_x - x1))
                start_y_adjusted = y1 + rayon * math.sin(math.atan2(control_y - y1, control_x - x1))
                end_x_adjusted = x2 - rayon * math.cos(math.atan2(y2 - control_y, x2 - control_x))
                end_y_adjusted = y2 - rayon * math.sin(math.atan2(y2 - control_y, x2 - control_x))

                canevas.create_line(start_x_adjusted, start_y_adjusted, control_x, control_y, end_x_adjusted, end_y_adjusted, smooth=tk.TRUE, arrow=tk.LAST)



    fenetre.mainloop()


