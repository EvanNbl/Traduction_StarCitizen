# Importation des modules
import os
import urllib.request
import shutil
import sys
import configparser
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from tkinter import scrolledtext

# Definition des variables
default_path = "C:\\Program Files\\Roberts Space Industries\\StarCitizen\\LIVE\\data"
url = "https://traduction.circuspes.fr/fr/global.ini"

# Definition des fonctions
def get_path():
    # On recupere le chemin du dossier de l'application
    path = filedialog.askdirectory(title="Selectionner le dossier de Star Citizen")
    # On verifie que le chemin est valide
    if path != "":
        # On ecrit le chemin dans le fichier de config
        config.set("path", "path", path)
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        # On affiche le chemin dans le label
        label_path.configure(text=path)
        # On active le bouton de traduction
        button_traduction.configure(state="normal")
    else:
        # On affiche un message d'erreur
        messagebox.showerror("Erreur", "Vous devez selectionner un dossier")

def get_traduction():
    # On recupere le chemin du dossier de l'application
    path = config.get("path", "path")
    # On verifie que le chemin est valide
    if path != "":
        # On recupere le fichier de traduction
        try:
            urllib.request.urlretrieve(url, "global.ini")
        except:
            messagebox.showerror("Erreur", "Impossible de recuperer le fichier de traduction")
        # On verifie que le dossier Localization existe
        if os.path.isdir(path + "/Localization"):
            if os.path.isfile(path + "/Localization/french_(france)"):
                # On copie le fichier de traduction dans le dossier Localization dans le dossier french_(france)
                try:
                    shutil.copy("global.ini", path + "/Localization/french_(france)/global.ini")
                except:
                    # On affiche un message d'erreur
                    messagebox.showerror("Erreur", "Impossible de copier le fichier de traduction")
                # On supprime le fichier de traduction
                try:
                    os.remove("global.ini")
                except:
                    # On affiche un message d'erreur
                    messagebox.showerror("Erreur", "Impossible de supprimer le fichier de traduction")
                # On affiche un message de confirmation
                messagebox.showinfo("Information", "La traduction a bien ete appliquee")
            else:
                try:
                    os.mkdir(path + "/Localization/french_(france)")
                except:
                    # On affiche un message d'erreur
                    messagebox.showerror("Erreur", "Impossible de creer le dossier french_(france)")
        else:
            try:
                os.mkdir(path + "/Localization")
            except:
                # On affiche un message d'erreur
                messagebox.showerror("Erreur", "Impossible de creer le dossier Localization")
    else:
        # On affiche un message d'erreur
        messagebox.showerror("Erreur", "Vous devez selectionner un dossier")

# Definition de la fenetre
fenetre = Tk()
fenetre.title("Traduction Star Citizen")
fenetre.resizable(True, True)

# Definition de la police
font = font.Font(family="Helvetica", size=12)

# Definition du style
style = ttk.Style()
style.configure("TButton", font=font)
style.configure("TLabel", font=font)
style.configure("TEntry", font=font)
style.configure("TCombobox", font=font)

# Definition du fichier de config
config = configparser.ConfigParser()
if os.path.isfile("config.ini"):
    config.read("config.ini")
else:
    config.add_section("path")
    config.set("path", "path", default_path)
    with open("config.ini", "w") as configfile:
        config.write(configfile)

# logo 
fenetre.iconbitmap("logo.ico")

# Definition des widgets
titre = ttk.Label(fenetre, text="Traduction Star Citizen")
# // mettre le sous titre en rouge
sous_titre = ttk.Label(fenetre, text="Attention: Selectionner le dossier data de Star Citizen", foreground="red")
label_path = ttk.Label(fenetre, text=config.get("path", "path"))
button_path = ttk.Button(fenetre, text="Selectionner le dossier", command=get_path)
button_traduction = ttk.Button(fenetre, text="Appliquer la traduction", command=get_traduction, state="disabled")

# Definition de la taille de la fenetre
fenetre.geometry("500x200")


# Placement des widgets
titre.grid(row=0, column=0, columnspan=2, padx=10, pady=10) 
sous_titre.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
label_path.grid(row=2, column=0, padx=10, pady=10)
button_path.grid(row=2, column=1, padx=10, pady=10)
button_traduction.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Lancement de la fenetre
fenetre.mainloop()

# Fin du script
sys.exit(0)