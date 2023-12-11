from tkinter import * 
from tkinter import filedialog
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import json
#local import
import verifFormat as v
import automaton_q2_q3
import automaton_q1

#Function
def insertTerminal(line):
    terminal.insert(tk.END, "> " + line + "\n")

def formatVerifBool():

    automate_verif = v.isAutomateString(textArea.get(1.0, tk.END))

    if automate_verif != 0:
        insertTerminal("ERROR: JSON is not correct")
        return False
    
    return True

def jsonLoads():
    return json.loads(v.conversion(textArea.get(1.0, tk.END)))

def insertPopUp(text):
    # Créer une fenêtre principale
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # Afficher la boîte de dialogue pour la saisie de l'utilisateur
    user_input = tk.simpledialog.askstring("Entrée", text)

    return user_input

#FILE AND DRAW
def openFile():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            textArea.delete(1.0, tk.END)
            textArea.insert(tk.END, content)

def saveFileAs():
    global current_file_path

    content = textArea.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path: 
        with open(file_path, 'w') as file:
            file.write(content)
        current_file_path = file_path

def saveFile():
    global current_file_path
    
    if current_file_path:
        content = textArea.get(1.0, tk.END)

        with open(current_file_path, 'w') as file:
            file.write(content)

    else:
        saveFileAs()

def drawAutomate():

    v.afficher_automate(jsonLoads())
    insertTerminal("En dev")

#Verification
def formatVerif():

    automate_verif = v.isAutomateString(textArea.get(1.0, tk.END))

    listError = [
        "OK",
        "Not a json",
        "The keys are false",
        "Transition must have three elements",
        "Initial_state' must have one element",
        "Element in 'alphabet', 'states' and 'final_states' must have any occurrence",
        "Alphabet is not correct",
        "States is not correct",
        "States must contain initial_state",
        "States must contain final_states"
    ]

    if automate_verif == 0:
        line = listError[0]
    else:
        line =  "ERROR" + str(automate_verif) + ": " + listError[automate_verif]
    
    insertTerminal(line)
    terminal.yview(tk.END)

#QUESTION
def question2():

    if formatVerifBool():
       
        word = insertPopUp("Entrez un mot:")

        if automaton_q2_q3.is_word_recognized(jsonLoads(),word):
            insertTerminal(word + " est reconnu par l'AEF")
        else:
            insertTerminal(word + " n'est reconnu par l'AEF")
        
def question3():

    if formatVerifBool():

        if automaton_q2_q3.is_complete(jsonLoads()):
            insertTerminal("L'automate est complet")
        else:
            insertTerminal("L'automate n'est pas complet")

def question4():
    
    if formatVerifBool():

        complet_automate = automaton_q2_q3.completing(jsonLoads())

        complet_automate = automaton_q1.get_good_type(complet_automate, "dict")

        complet_automate = json.dumps(complet_automate)#, indent=2)
        insertTerminal("Automate completé")
        complet_automate = complet_automate.replace('{','{\n').replace('}','\n}')
        complet_automate = complet_automate.replace('],','],\n')
        complet_automate = complet_automate.replace('[[','[\n [').replace(']]',']\n ]')

        textArea.delete(1.0, tk.END)
        textArea.insert(tk.END, complet_automate)

def question5():
    insertTerminal("q5 en travaux")  

def question6():
    insertTerminal("q6 en travaux") 

#---Main
projectName = "projet Python"
print(projectName)

root = Tk()
#root.geometry(800x800)
root.title(projectName)
root.resizable(height=False,width=False)

current_file_path = None

#TextArea
textArea = ScrolledText(root, width="100", height=30)
textArea.grid(row=0, column=0)
#Terminal
terminal = ScrolledText(root, width="100", height=10, bg="black", fg="white")
terminal.grid(row=1, column=0)

#Menu
menu = Menu(root)
menu_file = Menu(menu, tearoff=0)
menu_function = Menu(menu, tearoff=0)

#Menu file
menu_file.add_command(label="Ouvrir", command=openFile)
menu_file.add_command(label="Enregistrer", command=saveFileAs)
menu_file.add_command(label="Sauvegarder", command=saveFile)
menu.add_cascade(label="Fichier", menu=menu_file)

#Menu projet
menu_function.add_command(label="Reconnaissance", command=question2)
menu_function.add_command(label="Est complet", command=question3)
menu_function.add_command(label="Rendre complet", command=question4)
menu_function.add_command(label="Est déterministe", command=question5)
menu_function.add_command(label="Rendre déterministe", command=question6)
menu.add_cascade(label="Fonction", menu=menu_function)

#MenuFunction
menu.add_command(label="Verification", command=formatVerif)
menu.add_command(label="Shema", command=drawAutomate)

#mainloop
root.config(menu=menu)
root.mainloop()
