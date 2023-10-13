@echo off

:: Vérifier si Python 3 est déjà installé
python --version 2>NUL
if %errorlevel% equ 0 (
    echo Lancement du script Python...
    :: Exécuter le script Python
    python3 traduction.py
    exit
) else (
    echo Installation de Python 3...
    :: Télécharger le programme d'installation de Python 3
    curl https://www.python.org/ftp/python/3.9.4/python-3.9.4-amd64.exe --output python-installer.exe
    :: Installer Python 3
    python-installer.exe /quiet
    :: Supprimer le programme d'installation
    del python-installer.exe
    echo Installation de Python 3 terminée.
    echo Lancement du script Python...
    :: Exécuter le script Python
    python3 traduction.py
    exit
)
