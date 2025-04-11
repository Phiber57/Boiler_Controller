#!/bin/bash

# Définir les variables
REPO_URL="https://github.com/Phiber57/Boiler_Controller.git"
REPO_NAME=$(basename $REPO_URL .git)
SCRIPT_NAME="run.sh"
WORK_DIR="boiler"
SRC_DIR="Software"
VERSION_FILE="$WORK_DIR/last_version"

# Créer le dossier de travail s'il n'existe pas
mkdir -p $WORK_DIR
cd $WORK_DIR

# Vérifier la dernière version du dépôt
git ls-remote $REPO_URL HEAD | awk '{print $1}' > current_version


# Comparer avec la version précédente
if [ ! -f "$VERSION_FILE" ] || ! diff -q current_version "$VERSION_FILE" > /dev/null 2>&1; then
    echo "Nouvelle version détectée. Mise à jour et exécution du script..."
    
    # Supprimer l'ancien dépôt s'il existe
    rm -rf $REPO_NAME
    
    # Cloner le dépôt
    git clone $REPO_URL
    
    # Entrer dans le dossier du dépôt
    cd $REPO_NAME/$SRC_DIR

    # Rendre le script exécutable
    chmod +x ./run/$SCRIPT_NAME
    
    # Exécuter le script
    ./run/$SCRIPT_NAME
    
    # Mettre à jour le fichier de version
    mv current_version "$VERSION_FILE"
    
    # Nettoyer
    cd ..
    rm -rf $REPO_NAME
else
    echo "Aucune nouvelle version détectée. Le script ne sera pas exécuté."
fi

# Supprimer le fichier temporaire
rm -f current_version