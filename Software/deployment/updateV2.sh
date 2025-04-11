#!/bin/bash

# Vérifier si l'URL du repo est fournie
if [ $# -eq 0 ]; then
    echo "Usage: ./clone_project.sh <URL_DU_REPO>"
    exit 1
fi

REPO_URL=$1
PROJECT_DIR="project"

# Sauvegarder les credentials s'ils existent
CREDENTIAL_BACKUP="/tmp/credential_backup"
if [ -d "$PROJECT_DIR/credential" ]; then
    echo "Sauvegarde des credentials..."
    mkdir -p "$CREDENTIAL_BACKUP"
    cp -r "$PROJECT_DIR/credential/"* "$CREDENTIAL_BACKUP/"
fi

# Vérifier si le projet existe déjà
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Premier lancement - Clonage du projet depuis $REPO_URL..."
    git clone "$REPO_URL" "$PROJECT_DIR"
    
    if [ $? -ne 0 ]; then
        echo "Erreur lors du clonage du projet"
        rm -rf "$PROJECT_DIR"
        exit 1
    fi
else
    echo "Projet existant - Mise à jour..."
    cd "$PROJECT_DIR"
    git fetch origin
    git pull origin main || git pull origin master
    cd ..
fi

# Se déplacer dans le dossier du projet
cd "$PROJECT_DIR"

# Restaurer les credentials
if [ -d "$CREDENTIAL_BACKUP" ]; then
    echo "Restauration des credentials..."
    mkdir -p credential
    cp -r "$CREDENTIAL_BACKUP/"* credential/
    rm -rf "$CREDENTIAL_BACKUP"
fi

# Installer les dépendances Python si requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "Installation des dépendances Python..."
    pip install -r requirements.txt
fi

# Exécuter le script Python s'il existe
if [ -f "server.py" ]; then
    echo "Démarrage du serveur Python..."
    python3 server.py
else
    echo "Erreur: server.py non trouvé"
    exit 1
fi
