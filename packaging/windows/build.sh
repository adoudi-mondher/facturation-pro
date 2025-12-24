#!/bin/bash
# ===============================================
# Easy Facture - Script de build Windows (Git Bash)
# Par Mondher ADOUDI - Sidr Valley AI
# Version 1.6.0
# ===============================================

set -e  # Arrêter en cas d'erreur

echo ""
echo "================================================"
echo "   EASY FACTURE - BUILD WINDOWS .EXE"
echo "   Version 1.6.0"
echo "================================================"
echo ""

# Se placer à la racine du projet
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/../.." || exit 1
PROJECT_ROOT=$(pwd)

echo "[1/6] Vérification de Python..."

# Vérifier py (Python Launcher)
if ! cmd //c "py --version" 2>&1 | grep -q "Python"; then
    echo "ERROR: Python non trouvé"
    echo "Veuillez installer Python depuis python.org"
    exit 1
fi

PYTHON_VERSION=$(cmd //c "py --version" 2>&1 | head -1)
echo "     $PYTHON_VERSION détecté"
echo ""

# Créer/Vérifier un venv local si nécessaire
echo "[2/6] Préparation de l'environnement virtuel..."
if [ ! -d "venv_build" ]; then
    echo "     Création d'un nouvel environnement virtuel..."
    cmd //c "py -m venv venv_build"
    echo "     Environnement créé: venv_build/"
else
    echo "     Environnement existant: venv_build/"
fi
echo ""

# Installer les dépendances dans le venv de build
echo "[3/6] Installation des dépendances..."
echo "     Installation de PyInstaller..."
cmd //c "venv_build\\Scripts\\python.exe -m pip install --quiet --upgrade pip"
cmd //c "venv_build\\Scripts\\python.exe -m pip install --quiet pyinstaller"

if [ -f "requirements.txt" ]; then
    echo "     Installation des requirements du projet..."
    cmd //c "venv_build\\Scripts\\python.exe -m pip install --quiet -r requirements.txt"
fi
echo "     Dépendances installées: OK"
echo ""

# Nettoyer les builds précédents (MAIS PAS le .spec ni les données personnelles !)
echo "[4/6] Nettoyage des builds précédents..."
cd packaging/windows || exit 1

# Sauvegarder les données personnelles si elles existent
BACKUP_NEEDED=false
if [ -d "dist/EasyFacture/data" ]; then
    echo "     ⚠️  Sauvegarde des données personnelles détectée..."
    mkdir -p .backup_personal_data
    cp -r dist/EasyFacture/data .backup_personal_data/ 2>/dev/null && BACKUP_NEEDED=true
    echo "     ✓ Données sauvegardées temporairement"
fi

# Nettoyer
[ -d "build" ] && rm -rf build && echo "     - build/ supprimé"
[ -d "dist" ] && rm -rf dist && echo "     - dist/ supprimé"
echo "     Nettoyage: OK"
echo "     (EasyFacture.spec et données personnelles conservés)"
echo ""

# Build avec PyInstaller
echo "[5/6] Build de l'exécutable..."
SPEC_FILE="$(pwd)/EasyFacture.spec"
echo "     Fichier spec: $SPEC_FILE"
echo "     Ceci peut prendre 2-5 minutes, veuillez patienter..."
echo ""

# Vérifier que le .spec existe
if [ ! -f "EasyFacture.spec" ]; then
    echo "ERROR: EasyFacture.spec introuvable dans $(pwd)"
    exit 1
fi

# Utiliser le Python du venv_build avec chemin Windows
cd "$PROJECT_ROOT/packaging/windows"
cmd //c "..\\..\\venv_build\\Scripts\\python.exe -m PyInstaller EasyFacture.spec --clean --noconfirm"

BUILD_EXIT=$?

if [ $BUILD_EXIT -ne 0 ]; then
    echo ""
    echo "ERROR: Le build a échoué (code: $BUILD_EXIT)"
    echo "Vérifiez les erreurs ci-dessus"
    exit 1
fi

# Vérifier le résultat
echo ""
echo "[6/6] Vérification du résultat..."
if [ -f "dist/EasyFacture/EasyFacture.exe" ]; then
    EXE_SIZE=$(du -h "dist/EasyFacture/EasyFacture.exe" | cut -f1)
    echo "     ✓ EasyFacture.exe créé ($EXE_SIZE)"

    # Restaurer les données personnelles si elles ont été sauvegardées
    if [ "$BACKUP_NEEDED" = true ] && [ -d ".backup_personal_data/data" ]; then
        echo "     🔄 Restauration des données personnelles..."
        cp -r .backup_personal_data/data dist/EasyFacture/
        rm -rf .backup_personal_data
        echo "     ✓ Données personnelles restaurées"
    fi

    FILE_COUNT=$(find dist/EasyFacture -type f | wc -l)
    FOLDER_SIZE=$(du -sh dist/EasyFacture | cut -f1)
    echo "     ✓ $FILE_COUNT fichiers dans le package"
    echo "     ✓ Taille totale: $FOLDER_SIZE"
else
    echo "     ✗ ERREUR: EasyFacture.exe non trouvé dans dist/EasyFacture/"
    echo ""
    echo "Contenu de dist/ :"
    ls -la dist/ 2>/dev/null || echo "Le dossier dist/ n'existe pas"

    # Restaurer les données quand même en cas d'échec
    if [ "$BACKUP_NEEDED" = true ] && [ -d ".backup_personal_data" ]; then
        echo "     🔄 Tentative de restauration des données..."
        mkdir -p dist/EasyFacture
        cp -r .backup_personal_data/data dist/EasyFacture/ 2>/dev/null
        rm -rf .backup_personal_data
    fi

    exit 1
fi

echo ""
echo "================================================"
echo "   BUILD TERMINÉ AVEC SUCCÈS !"
echo "================================================"
echo ""
echo "📦 Exécutable: packaging/windows/dist/EasyFacture/EasyFacture.exe"
echo "📏 Taille: $FOLDER_SIZE"
echo ""
echo "🧪 Pour tester:"
echo "   cd packaging/windows/dist/EasyFacture"
echo "   ./EasyFacture.exe"
echo ""
echo "📮 Pour distribuer:"
echo "   Compressez le dossier 'dist/EasyFacture' en ZIP"
echo "   Envoyez le fichier ZIP aux utilisateurs"
echo ""
echo "✨ Bon déploiement !"
echo ""
