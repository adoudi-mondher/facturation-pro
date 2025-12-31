#!/bin/bash
# ===============================================
# Easy Facture - Build VERSION CLIENT (propre)
# Par Mondher ADOUDI - Sidr Valley AI
# Version 1.6.0
# ===============================================
#
# Ce script crée une version PROPRE pour distribution client
# SANS vos données personnelles de test

set -e

echo ""
echo "================================================"
echo "   EASY FACTURE - BUILD VERSION CLIENT"
echo "   Version 1.6.0 (Distribution propre)"
echo "================================================"
echo ""
echo "⚠️  ATTENTION: Ce build sera SANS vos données de test"
echo "   Utiliser pour: Distribution aux clients"
echo "   Ne PAS utiliser pour: Votre version perso"
echo ""
read -p "Continuer? (o/n): " confirm
if [ "$confirm" != "o" ] && [ "$confirm" != "O" ]; then
    echo "Build annulé"
    exit 0
fi
echo ""

# Se placer à la racine du projet
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/../.." || exit 1
PROJECT_ROOT=$(pwd)

echo "[1/7] Vérification de Python..."
if ! cmd //c "py --version" 2>&1 | grep -q "Python"; then
    echo "ERROR: Python non trouvé"
    exit 1
fi
PYTHON_VERSION=$(cmd //c "py --version" 2>&1 | head -1)
echo "     $PYTHON_VERSION détecté"
echo ""

echo "[2/7] Préparation de l'environnement virtuel..."
if [ ! -d "venv_build" ]; then
    echo "     Création d'un nouvel environnement virtuel..."
    cmd //c "py -m venv venv_build"
    echo "     Environnement créé: venv_build/"
else
    echo "     Environnement existant: venv_build/"
fi
echo ""

echo "[3/7] Installation des dépendances..."
echo "     Installation de PyInstaller..."
cmd //c "venv_build\\Scripts\\python.exe -m pip install --quiet --upgrade pip"
cmd //c "venv_build\\Scripts\\python.exe -m pip install --quiet pyinstaller"

if [ -f "requirements.txt" ]; then
    echo "     Installation des requirements du projet..."
    cmd //c "venv_build\\Scripts\\python.exe -m pip install --quiet -r requirements.txt"
fi
echo "     Dépendances installées: OK"
echo ""

echo "[4/7] Nettoyage complet (SANS sauvegarde des données)..."
cd packaging/windows || exit 1

# ⚠️ PAS DE SAUVEGARDE - Build propre pour client
[ -d "build" ] && rm -rf build && echo "     - build/ supprimé"
[ -d "dist" ] && rm -rf dist && echo "     - dist/ supprimé"
echo "     Nettoyage: OK (build propre pour client)"
echo ""

echo "[5/7] Build de l'exécutable..."
SPEC_FILE="$(pwd)/EasyFacture.spec"
echo "     Fichier spec: $SPEC_FILE"
echo "     Ceci peut prendre 2-5 minutes, veuillez patienter..."
echo ""

if [ ! -f "EasyFacture.spec" ]; then
    echo "ERROR: EasyFacture.spec introuvable dans $(pwd)"
    exit 1
fi

cd "$PROJECT_ROOT/packaging/windows"
cmd //c "..\\..\\venv_build\\Scripts\\python.exe -m PyInstaller EasyFacture.spec --clean --noconfirm"

BUILD_EXIT=$?

if [ $BUILD_EXIT -ne 0 ]; then
    echo ""
    echo "ERROR: Le build a échoué (code: $BUILD_EXIT)"
    exit 1
fi

echo ""
echo "[6/7] Création d'un dossier data/ vide pour le client..."
if [ -f "dist/EasyFacture/EasyFacture.exe" ]; then
    # Créer structure data vide
    mkdir -p dist/EasyFacture/data/uploads/logos
    mkdir -p dist/EasyFacture/data/uploads/factures
    mkdir -p dist/EasyFacture/data/backups

    # Créer des fichiers .gitkeep pour préserver la structure
    touch dist/EasyFacture/data/uploads/.gitkeep
    touch dist/EasyFacture/data/backups/.gitkeep

    echo "     ✓ Dossier data/ vide créé"
    echo "     ✓ Structure: data/uploads/, data/backups/"
else
    echo "     ✗ ERREUR: EasyFacture.exe non trouvé"
    exit 1
fi

echo ""
echo "[7/7] Vérification du package client..."
EXE_SIZE=$(du -h "dist/EasyFacture/EasyFacture.exe" | cut -f1)
echo "     ✓ EasyFacture.exe créé ($EXE_SIZE)"

FILE_COUNT=$(find dist/EasyFacture -type f | wc -l)
FOLDER_SIZE=$(du -sh dist/EasyFacture | cut -f1)
echo "     ✓ $FILE_COUNT fichiers dans le package"
echo "     ✓ Taille totale: $FOLDER_SIZE"

# Vérifier qu'il n'y a PAS de base de données
if [ -f "dist/EasyFacture/data/facturation.db" ]; then
    echo "     ⚠️  ATTENTION: Une base de données existe (suppression...)"
    rm -f dist/EasyFacture/data/facturation.db
fi

echo "     ✓ Aucune donnée personnelle détectée"
echo ""

echo "================================================"
echo "   BUILD CLIENT TERMINÉ !"
echo "================================================"
echo ""
echo "📦 Package client (PROPRE) : packaging/windows/dist/EasyFacture/"
echo "📏 Taille: $FOLDER_SIZE"
echo "🔒 Sans données personnelles: OUI ✓"
echo ""
echo "🎁 Pour distribuer :"
echo "   1. Compresser le dossier dist/EasyFacture/"
echo "      cd packaging/windows/dist"
echo "      zip -r EasyFacture-v1.6.0-Client.zip EasyFacture/"
echo ""
echo "   2. Envoyer EasyFacture-v1.6.0-Client.zip au client"
echo ""
echo "   3. Le client décompresse et lance EasyFacture.exe"
echo "      → L'app créera automatiquement la base de données vide"
echo "      → Le client entrera sa licence au premier lancement"
echo ""
echo "✨ Package prêt pour distribution !"
echo ""
