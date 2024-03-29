from tkinter import * 
from tkinter import filedialog
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import json
#local import
import interface as v
import recognize_complete_q2_q3_q4
import automaton_q1
import determinist
import automaton_q7
import regex_q8_q9_q10
import minimal_q12
import excise

#Function
"""
Insert a line on the app-terminal
"""
def insertTerminal(line):
    terminal.insert(tk.END, "> " + line + "\n")
    terminal.see(tk.END)
"""
Check if the json format is correct
@return: Boolean 
"""
def formatVerifBool():

    automate_verif = v.isAutomateString(getTextAreaJSON())

    if automate_verif != 0:
        insertTerminal("ERROR: JSON is not correct")
        return False
    
    return True
"""
Gives the json contained in the text area
@return: String 
"""
def getTextAreaJSON():

    full_text = textArea.get(1.0, tk.END)

    start_comment = '/*'
    end_comment = '*/'

    start_index = full_text.find(start_comment)

    while start_index != -1:

        end_index = full_text.find(end_comment, start_index + len(start_comment))

        if end_index == -1:
            break

        full_text = full_text[:start_index] + full_text[end_index + len(end_comment):]
        start_index = full_text.find(start_comment)

    #print(full_text)

    return full_text
"""
Gives comments contained in textarea
@return: String
"""
def getTextAreaComment():

    full_text = textArea.get(1.0, tk.END)

    start_comment = '/*'
    end_comment = '*/'

    text_inside_comments = []
    start_index = full_text.find(start_comment)

    while start_index != -1:

        end_index = full_text.find(end_comment, start_index + len(start_comment))

        if end_index == -1:
            break

        text_inside_comments.append(full_text[start_index + len(start_comment):end_index])

        start_index = full_text.find(start_comment, end_index + len(end_comment))

    result_text = '\n'.join(text_inside_comments)

    return result_text
"""
Load the json from a string
@return: json
"""
def jsonLoads():
    return json.loads(v.conversion(getTextAreaJSON()))
"""
Load 2 json from a string
@return: [json]
"""
def  json2loadsAndVerif():

    text = getTextAreaJSON()
    i = text.find('}\n{')

    if  i != -1:

        json1 = text[:i+1]
        json2 = text[i+2:]

        if v.isAutomateString(json1) != 0:
            insertTerminal("ERROR: 1st JSON is not correct")
            json1 = ""
            
        if v.isAutomateString(json2) != 0:
            insertTerminal("ERROR: 2nd JSON is not correct")   
            json2 = ""
        
        return [json1,json2]

    else:
        insertTerminal("ERREUR: Les deux JSON doivent être separé par un retour à la ligne")
        return ['','']
"""
Create an insert pop up
@param: String text to write on the pop up
@return: String the user input
"""
def insertPopUp(text):
    # Créer une fenêtre principale
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # Afficher la boîte de dialogue pour la saisie de l'utilisateur
    user_input = tk.simpledialog.askstring("Entrée", text)

    return user_input
"""
Convert automaton to string and put it in text area with comment
@param: json automate
"""
def addJsonOnTextArea(automate):
  
    automate = automaton_q1.get_good_type(automate, "dict")
   
    automate = json.dumps(automate)

    automate = automate.replace('{','{\n').replace('}','\n}')
    automate = automate.replace('],','],\n')
    automate = automate.replace('[[','[\n [').replace(']]',']\n ]')
    automate = automate.replace(', "final_states"',',\n "final_states"')
    automate = automate.replace(', "transitions"',',\n "transitions"')
    
    comment = getTextAreaComment()
    if comment != "":
        automate += "\n/*" + comment + "*/"

    textArea.delete(1.0, tk.END)
    textArea.insert(tk.END, automate)
#FILE AND DRAW
"""
Open a file and load the content on the text area
"""
def openFile():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            textArea.delete(1.0, tk.END)
            textArea.insert(tk.END, content)
"""
Open a file and add the content on the text area
"""
def addFile():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            content = '\n' + file.read()
            textArea.insert(tk.END, content)
"""
Save the text area on a new file
"""
def saveFileAs():
    global current_file_path

    content = textArea.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path: 
        with open(file_path, 'w') as file:
            file.write(content)
        current_file_path = file_path
"""
Save the file and create a file if it does not exist yet
"""
def saveFile():
    global current_file_path
    
    if current_file_path:
        content = textArea.get(1.0, tk.END)

        with open(current_file_path, 'w') as file:
            file.write(content)

    else:
        saveFileAs()
"""
Check if the json format is correct
"""
def drawAutomate():

    #if formatVerifBool():
    v.drawAutomate(jsonLoads())

#Verification
"""
Check if the json format is correct
"""
def formatVerif():

    automate_verif = v.isAutomateString(getTextAreaJSON())

    listError = [
        "OK",
        "Ce n'est pas du JSON",
        "Les clés sont incorrectes",
        "La transition doit avoir trois éléments",
        "L'état initial doit avoir un élément",
        "Les éléments dans 'alphabet', 'states' et 'final_states' doivent avoir au moins une occurrence",
        "L'alphabet n'est pas correct",
        "Les états ne sont pas corrects",
        "Les états doivent contenir initial_state ET initial_state doit avoir un élément",
        "Les états doivent contenir final_states"
    ]

    if automate_verif == 0:
        line = listError[0]
    else:
        line =  "ERREUR" + str(automate_verif) + ": " + listError[automate_verif]
    
    insertTerminal(line)
    terminal.yview(tk.END)

#QUESTION
"""
Function which links the function of the question 2 to the HMI
"""
def question2():

    if formatVerifBool():
       
        word = insertPopUp("Entrez un mot:")

        if recognize_complete_q2_q3_q4.is_word_recognized(jsonLoads(),word):
            insertTerminal(word + " est reconnu par l'AEF")
        else:
            insertTerminal(word + " n'est reconnu par l'AEF")
"""
Function which links the function of the question 3 to the HMI
"""       
def question3():

    if formatVerifBool():

        if recognize_complete_q2_q3_q4.is_complete(jsonLoads()):
            insertTerminal("L'automate est complet")
        else:
            insertTerminal("L'automate n'est pas complet")
"""
Function which links the function of the question 4 to the HMI
"""
def question4():
    
    if formatVerifBool():

        automate = recognize_complete_q2_q3_q4.completing(jsonLoads())

        addJsonOnTextArea(automate)
        insertTerminal("Automate completé")
"""
Function which links the function of the question 5 to the HMI
"""
def question5():
    
    if formatVerifBool():

        test = determinist.is_automaton_deterministic(jsonLoads())

        if test[0]:
            insertTerminal("L'automate est deterministe")
        else:
            insertTerminal(test[1])
"""
Function which links the function of the question 6 to the HMI
"""
def question6():
    
    if formatVerifBool():

        #automate = automaton_q1.get_good_type(jsonLoads, "dataFrame")
        automate = determinist.to_automaton_deterministic(jsonLoads())      
        
        addJsonOnTextArea(automate)     
        insertTerminal("Automate à été rendu deterministe")
       
"""
Function which links the function of the question 7.1 to the HMI
"""
def question71():
    
    if formatVerifBool():

        automate = automaton_q7.complem_automaton(jsonLoads())

        addJsonOnTextArea(automate)
        insertTerminal("Automate complementé")
"""
Function which links the function of the question 7.2 to the HMI
"""
def question72():

    if formatVerifBool():
        
        automate = automaton_q7.miroir_automaton(jsonLoads())

        addJsonOnTextArea(automate)
        insertTerminal("Automate rendu miroir")
"""
Function which links the function of the question 7.3 to the HMI
"""
def question73():

    jsonTab = json2loadsAndVerif()
    json1 = jsonTab[0]
    json2 = jsonTab[1]

    if json1 != '' and json2 != '':
        json1 = json.loads(v.conversion(json1))
        json2 = json.loads(v.conversion(json2))

        automate = automaton_q7.produit_aefs(json1,json2)

        addJsonOnTextArea(automate)
        insertTerminal("Produits effectué")

"""
Function which links the function of the question 7.4 to the HMI
"""
def question74():

    jsonTab = json2loadsAndVerif()
    json1 = jsonTab[0]
    json2 = jsonTab[1]

    if json1 != '' and json2 != '':
        json1 = json.loads(v.conversion(json1))
        json2 = json.loads(v.conversion(json2))

        automate = automaton_q7.concatAEF(json1,json2)

        addJsonOnTextArea(automate)
        insertTerminal("Produits effectué")
"""
Function which links the function of the question 8 to the HMI
"""
def question8():

    if formatVerifBool():
        insertTerminal("Expression reguliere: " + regex_q8_q9_q10.find_regex(jsonLoads()))  
"""
Function which links the function of the question 9 to the HMI
"""
def question9():

    if formatVerifBool():
        insertTerminal("Langage: " + regex_q8_q9_q10.find_language(jsonLoads()))  
"""
Function which links the function of the question 10 to the HMI
"""
def question10():

    jsonTab = json2loadsAndVerif()
    json1 = jsonTab[0]
    json2 = jsonTab[1]

    if json1 != '' and json2 != '':
        json1 = json.loads(v.conversion(json1))
        json2 = json.loads(v.conversion(json2))

        isEqui = regex_q8_q9_q10.is_automate_equivalent(json1,json2)

        if isEqui:
            insertTerminal("Les deux automates sont equivalents")
        else: 
            insertTerminal("Les deux automates ne sont pas equivalents")

"""
Function which links the function of the question 11 to the HMI
"""
def question11():

    if formatVerifBool():
        
        automate = jsonLoads()
        automate = minimal_q12.minimal_automaton(automate)

        addJsonOnTextArea(automate)
        insertTerminal("Automate éondé")


"""
Function which links the function of the question 12 to the HMI
"""
def question12():

    if formatVerifBool():

        automate = jsonLoads()

        
        if not determinist.is_automaton_deterministic(automate)[0] :
            automate = determinist.to_automaton_deterministic(automate)
            insertTerminal("Warning : Only deterministic automaton can be minimal. The automaton is now deterministic")
        automate = minimal_q12.minimal_automaton(jsonLoads())

        addJsonOnTextArea(automate)
        insertTerminal("Automate minimisé")
        

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
menu_file.add_command(label="Ajouter", command=addFile)
menu_file.add_command(label="Enregistrer", command=saveFileAs)
menu_file.add_command(label="Sauvegarder", command=saveFile)
menu.add_cascade(label="Fichier", menu=menu_file)

#Menu projet
menu_function.add_command(label="Reconnaissance", command=question2)
menu_function.add_command(label="Est complet", command=question3)
menu_function.add_command(label="Rendre complet", command=question4)
menu_function.add_command(label="Est déterministe", command=question5)
menu_function.add_command(label="Rendre déterministe", command=question6)
menu_function.add_command(label="Complement", command=question71)
menu_function.add_command(label="Miroir", command=question72)
menu_function.add_command(label="Produit", command=question73)
menu_function.add_command(label="Concatenation", command=question74)
menu_function.add_command(label="Expression regulière", command=question8)
menu_function.add_command(label="Langage Reconnu", command=question9)
menu_function.add_command(label="Equivalent", command=question10)
menu_function.add_command(label="Rendre emondé", command=question11)
menu_function.add_command(label="Rendre minimal", command=question12)
menu.add_cascade(label="Fonction", menu=menu_function)

#MenuFunction
menu.add_command(label="Verification", command=formatVerif)
menu.add_command(label="Schema", command=drawAutomate)

#mainloop
root.config(menu=menu)
root.mainloop()
