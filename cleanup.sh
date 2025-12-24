#!/bin/bash
# Script de nettoyage du projet avant commit
# Par Mondher ADOUDI - Sidr Valley AI

echo "🧹 NETTOYAGE DU PROJET FACTURATION-APP"
echo "======================================"
echo ""

# Compteur d'espace libéré
FREED_SPACE=0

echo "🔴 ÉTAPE 1 : Suppression des fichiers temporaires volumineux"
echo "------------------------------------------------------------"

# Environnements virtuels
if [ -d "venv" ]; then
    SIZE=$(du -sm venv | cut -f1)
    rm -rf venv
    echo "  ✓ venv/ supprimé (${SIZE} MB)"
    FREED_SPACE=$((FREED_SPACE + SIZE))
fi

if [ -d "venv_build" ]; then
    SIZE=$(du -sm venv_build | cut -f1)
    rm -rf venv_build
    echo "  ✓ venv_build/ supprimé (${SIZE} MB)"
    FREED_SPACE=$((FREED_SPACE + SIZE))
fi

# Artefacts de build
if [ -d "build" ]; then
    SIZE=$(du -sm build 2>/dev/null | cut -f1)
    rm -rf build
    echo "  ✓ build/ supprimé (${SIZE} MB)"
    FREED_SPACE=$((FREED_SPACE + SIZE))
fi

if [ -d "dist" ]; then
    SIZE=$(du -sm dist 2>/dev/null | cut -f1)
    rm -rf dist
    echo "  ✓ dist/ supprimé (${SIZE} MB)"
    FREED_SPACE=$((FREED_SPACE + SIZE))
fi

if [ -d "packaging/windows/build" ]; then
    SIZE=$(du -sm packaging/windows/build 2>/dev/null | cut -f1)
    rm -rf packaging/windows/build
    echo "  ✓ packaging/windows/build/ supprimé (${SIZE} MB)"
    FREED_SPACE=$((FREED_SPACE + SIZE))
fi

if [ -d "packaging/windows/dist" ]; then
    SIZE=$(du -sm packaging/windows/dist 2>/dev/null | cut -f1)
    rm -rf packaging/windows/dist
    echo "  ✓ packaging/windows/dist/ supprimé (${SIZE} MB)"
    FREED_SPACE=$((FREED_SPACE + SIZE))
fi

# Cache de tests
if [ -d ".pytest_cache" ]; then
    rm -rf .pytest_cache
    echo "  ✓ .pytest_cache/ supprimé"
fi

if [ -d "htmlcov" ]; then
    SIZE=$(du -sm htmlcov 2>/dev/null | cut -f1)
    rm -rf htmlcov
    echo "  ✓ htmlcov/ supprimé (${SIZE} MB)"
    FREED_SPACE=$((FREED_SPACE + SIZE))
fi

# Cache Python
echo "  🔍 Recherche de __pycache__..."
PYCACHE_COUNT=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l)
if [ $PYCACHE_COUNT -gt 0 ]; then
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
    echo "  ✓ $PYCACHE_COUNT dossiers __pycache__/ supprimés"
fi

echo ""
echo "🟠 ÉTAPE 2 : Suppression des backups manuels"
echo "--------------------------------------------"

if [ -f "config.py.backup" ]; then
    rm config.py.backup
    echo "  ✓ config.py.backup supprimé"
fi

if [ -f "run.py.backup" ]; then
    rm run.py.backup
    echo "  ✓ run.py.backup supprimé"
fi

echo ""
echo "🟡 ÉTAPE 3 : Archivage de la documentation obsolète"
echo "----------------------------------------------------"

mkdir -p docs/archive

if [ -f "CORRECTIONS-BUILD-WINDOWS.md" ]; then
    mv CORRECTIONS-BUILD-WINDOWS.md docs/archive/
    echo "  ✓ CORRECTIONS-BUILD-WINDOWS.md → docs/archive/"
fi

echo ""
echo "📊 RÉSUMÉ DU NETTOYAGE"
echo "======================"
echo ""
echo "  Espace libéré : ~${FREED_SPACE} MB"
echo ""
echo "✅ Fichiers conservés :"
echo "  • Votre licence : .personal_backup/license_adoudi_at_mondher.ch_20251207.txt"
echo "  • Documentation : BUILD-PERSONNEL-VS-CLIENT.md, GUIDE-DEPLOIEMENT-DISTANT.md"
echo "  • Code source : app/, tests/, static/, etc."
echo "  • Scripts : build.sh, build_for_client.sh, generate_customer_license.py"
echo ""
echo "⚠️  Fichiers .gitignore mis à jour :"
echo "  • Ajouté : license_*.txt"
echo "  • Ajouté : .personal_backup/"
echo ""
echo "🎯 PROCHAINES ÉTAPES :"
echo "  1. Vérifier que tout fonctionne : git status"
echo "  2. Recréer venv si besoin : py -m venv venv"
echo "  3. Installer dépendances : pip install -r requirements.txt"
echo "  4. Commit des changements : git add . && git commit -m 'chore: cleanup project'"
echo ""
