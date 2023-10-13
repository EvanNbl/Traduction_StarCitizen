import os
import urllib.request
import shutil
import sys
import configparser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import zipfile

# Définition des constantes
DEFAULT_PATH = "C:\\Program Files\\Roberts Space Industries\\StarCitizen\\LIVE\\data"
CONFIG_FILE = "config.ini"

# Fonction pour mettre à jour la source de traduction
def update_translation_source(event):
    source = translation_source_var.get()
    config.set("translation_source", "source", source)
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

# Fonction pour sélectionner le dossier de Star Citizen
def get_path():
    path = filedialog.askdirectory(title="Sélectionner le dossier de Star Citizen")
    if path:
        config.set("path", "path", path)
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
        label_path.configure(text=path)
        button_traduction.configure(state="normal")
    else:
        messagebox.showerror("Erreur", "Vous devez sélectionner un dossier")

# Fonction pour appliquer la traduction
def get_translation():
    source = config.get("translation_source", "source")
    path = config.get("path", "path")
    path = path[:-5]

    try:
        with open(os.path.join(path, "user.cfg"), "w") as userfile:
            userfile.write("g_language = french_(france)")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de créer le fichier user.cfg : {str(e)}")

    path = os.path.join(path, "data")
    if source == "Traduction FR Cirque Lisoir & Co":
        url = "https://traduction.circuspes.fr/fr/global.ini"
        try:
            urllib.request.urlretrieve(url, "global.ini")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer le fichier de traduction : {str(e)}")
    elif source == "Traduction FR de SPEED0U":
        zip_url = "https://github.com/SPEED0U/StarCitizenTranslations/archive/master.zip"
        try:
            urllib.request.urlretrieve(zip_url, "translations.zip")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de télécharger le fichier de traduction : {str(e)}")

        with zipfile.ZipFile("translations.zip", "r") as zip_ref:
            zip_ref.extract("StarCitizenTranslations-main/french_(france)/global.ini")
            shutil.copy("StarCitizenTranslations-main/french_(france)/global.ini", "global.ini")

        os.remove("translations.zip")
        os.remove("StarCitizenTranslations-main/french_(france)/global.ini")
        os.rmdir("StarCitizenTranslations-main/french_(france)")
        os.rmdir("StarCitizenTranslations-main")
    else:
        messagebox.showerror("Erreur", "Source de traduction inconnue.")
        return

    localization_dir = os.path.join(path, "Localization")
    if os.path.isdir(localization_dir):
        french_dir = os.path.join(localization_dir, "french_(france)")
        if os.path.isfile(french_dir):
            try:
                shutil.copy("global.ini", french_dir)
                os.remove("global.ini")
                messagebox.showinfo("Succès", "La traduction a été appliquée avec succès !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de copier le fichier de traduction : {str(e)}")
        else:
            try:
                os.mkdir(french_dir)
                shutil.copy("global.ini", french_dir)
                os.remove("global.ini")
                messagebox.showinfo("Succès", "La traduction a été appliquée avec succès !")
            except Exception as e:
                os.remove("global.ini")
    else:
        try:
            os.mkdir(localization_dir)
            french_dir = os.path.join(localization_dir, "french_(france)")
            os.mkdir(french_dir)
            shutil.copy("global.ini", french_dir)
            os.remove("global.ini")
            messagebox.showinfo("Succès", "La traduction a été appliquée avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier Localization : {str(e)}")

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
if os.path.isfile(CONFIG_FILE):
    config.read(CONFIG_FILE)
else:
    config.add_section("path")
    config.set("path", "path", DEFAULT_PATH)

if not config.has_section("translation_source"):
    config.add_section("translation_source")
    config.set("translation_source", "source", "Traduction Cirque Lisoir & Communauté FR")

with open(CONFIG_FILE, "w") as configfile:
    config.write(configfile)

# Logo
fenetre.iconbitmap("logo.ico")

# Définition des widgets
titre = ttk.Label(fenetre, text="Traduction Star Citizen")
sous_titre = ttk.Label(fenetre, text="Attention: Sélectionner le dossier 'data' de Star Citizen", foreground="red")
label_path = ttk.Label(fenetre, text=config.get("path", "path"))
button_path = ttk.Button(fenetre, text="Sélectionner le dossier", command=get_path)
button_traduction = ttk.Button(fenetre, text="Appliquer la traduction", command=get_translation, state="disabled")

# Créez le sélecteur
translation_source_label = ttk.Label(fenetre, text="Source de traduction :")
translation_source_var = tk.StringVar()
translation_source_combobox = ttk.Combobox(fenetre, textvariable=translation_source_var, values=["Traduction Cirque Lisoir & Communauté FR", "Traduction FR de SPEED0U"])
translation_source_combobox.set(config.get("translation_source", "source"))
translation_source_combobox["width"] = 30

# Placement des widgets
titre.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
translation_source_combobox.grid(row=0, column=1, padx=10, pady=10)
sous_titre.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
label_path.grid(row=3, column=0, padx=10, pady=10)
button_path.grid(row=3, column=1, padx=10, pady=10)
button_traduction.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Associez la fonction à l'événement de changement d'option dans le sélecteur
translation_source_combobox.bind("<<ComboboxSelected>>", update_translation_source)

# Lancement de la fenêtre
fenetre.geometry("700x200")  # Augmentez la hauteur pour faire de la place pour le sélecteur
fenetre.mainloop()

# Fin du script
sys.exit(0)
