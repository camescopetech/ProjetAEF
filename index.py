from tkinter import * 
from tkinter import filedialog
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import json
#local import
import verifFormat as v

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

def formatTerminal(line):
    return "> " + line + "\n"

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
    
    terminal.insert(tk.END, formatTerminal(line))
    terminal.yview(tk.END)

def drawAutomate():

    v.afficher_automate(json.loads(v.conversion(textArea.get(1.0, tk.END))))

#QUESTION
#2
def question2():
    print("hello")


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
menu.add_cascade(label="Fonction", menu=menu_function)

#MenuFunction
menu.add_command(label="Verification", command=formatVerif)
menu.add_command(label="Shema", command=drawAutomate)

#mainloop
root.config(menu=menu)
root.mainloop()