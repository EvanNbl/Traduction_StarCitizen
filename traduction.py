import os
import urllib.request
import shutil
import sys
import configparser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font

# Définition des constantes
DEFAULT_PATH = "C:\\Program Files\\Roberts Space Industries\\StarCitizen\\LIVE\\data"
URL = "https://traduction.circuspes.fr/fr/global.ini"

# Définition des fonctions
def get_path():
    path = filedialog.askdirectory(title="Sélectionner le dossier de Star Citizen")
    if path:
        config.set("path", "path", path)
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        label_path.configure(text=path)
        button_traduction.configure(state="normal")
    else:
        messagebox.showerror("Erreur", "Vous devez sélectionner un dossier")

def get_translation():
    path = config.get("path", "path")
    path = path[:-5]
    try:
        with open(os.path.join(path, "user.cfg"), "w") as userfile:
            userfile.write("g_language = french_(france)")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de créer le fichier user.cfg : {str(e)}")

    path = config.get("path", "path")
    if path:
        try:
            urllib.request.urlretrieve(URL, "global.ini")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer le fichier de traduction : {str(e)}")

        localization_dir = os.path.join(path, "Localization")
        if os.path.isdir(localization_dir):
            french_dir = os.path.join(localization_dir, "french_(france)")
            if os.path.isfile(french_dir):
                try:
                    shutil.copy("global.ini", french_dir)
                    os.remove("global.ini")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de copier le fichier de traduction : {str(e)}")
            else:
                try:
                    os.mkdir(french_dir)
                    shutil.copy("global.ini", french_dir)
                    os.remove("global.ini")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de créer le dossier french_(france) : {str(e)}")
        else:
            try:
                os.mkdir(localization_dir)
                french_dir = os.path.join(localization_dir, "french_(france)")
                os.mkdir(french_dir)
                shutil.copy("global.ini", french_dir)
                os.remove("global.ini")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de créer le dossier Localization : {str(e)}")
    else:
        messagebox.showerror("Erreur", "Vous devez sélectionner un dossier")

# Définition de la fenêtre
fenetre = tk.Tk()
fenetre.title("Traduction Star Citizen")
fenetre.resizable(True, True)

# Définition de la police
font_style = font.nametofont("TkDefaultFont")
font_style.configure(size=12)

# Définition du style
style = ttk.Style()
style.configure("TButton", font=font_style)
style.configure("TLabel", font=font_style)
style.configure("TEntry", font=font_style)
style.configure("TCombobox", font=font_style)

# Définition du fichier de configuration
config = configparser.ConfigParser()
if os.path.isfile("config.ini"):
    config.read("config.ini")
else:
    config.add_section("path")
    config.set("path", "path", DEFAULT_PATH)
    with open("config.ini", "w") as configfile:
        config.write(configfile)

# Logo
fenetre.iconbitmap("logo.ico")

# Définition des widgets
titre = ttk.Label(fenetre, text="Traduction Star Citizen")
sous_titre = ttk.Label(fenetre, text="Attention: Sélectionner le dossier data de Star Citizen", foreground="red")
label_path = ttk.Label(fenetre, text=config.get("path", "path"))
button_path = ttk.Button(fenetre, text="Sélectionner le dossier", command=get_path)
button_traduction = ttk.Button(fenetre, text="Appliquer la traduction", command=get_translation, state="disabled")

# Définition de la taille de la fenêtre
fenetre.geometry("650x200")

# Placement des widgets
titre.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
sous_titre.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
label_path.grid(row=2, column=0, padx=10, pady=10)
button_path.grid(row=2, column=1, padx=10, pady=10)
button_traduction.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Lancement de la fenêtre
fenetre.mainloop()

# Fin du script
sys.exit(0)
