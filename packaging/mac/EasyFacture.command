#!/bin/bash
# ===============================================
# Easy Facture - Lanceur Mac
# Par Mondher ADOUDI - Sidr Valley AI
# Version 1.5.0
# ===============================================

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Bannière
clear
echo "============================================================"
echo "   🚀 EASY FACTURE v1.5.0"
echo "   Par Mondher ADOUDI - Sidr Valley AI"
echo "============================================================"
echo ""

# Aller dans le répertoire du script
cd "$(dirname "$0")"

# Vérifier Python
echo -e "${BLUE}[1/4]${NC} Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    echo ""
    echo "Installation de Python 3 :"
    echo "1. Aller sur https://www.python.org/downloads/mac-osx/"
    echo "2. Télécharger Python 3.10+"
    echo "3. Installer et relancer ce script"
    echo ""
    read -p "Appuyez sur Entrée pour quitter..."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"
echo ""

# Vérifier/Créer environnement virtuel
echo -e "${BLUE}[2/4]${NC} Configuration de l'environnement..."
if [ ! -d "venv" ]; then
    echo "   Création de l'environnement virtuel..."
    python3 -m venv venv
    echo -e "${GREEN}   ✅ Environnement créé${NC}"
else
    echo -e "${GREEN}   ✅ Environnement existant${NC}"
fi

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
echo ""
echo -e "${BLUE}[3/4]${NC} Installation des dépendances..."
if [ ! -f ".deps_installed" ]; then
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    touch .deps_installed
    echo -e "${GREEN}   ✅ Dépendances installées${NC}"
else
    echo -e "${GREEN}   ✅ Dépendances déjà installées${NC}"
fi

# Trouver un port libre
echo ""
echo -e "${BLUE}[4/4]${NC} Démarrage du serveur..."
PORT=5000
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; do
    echo "   Port $PORT occupé, essai du suivant..."
    PORT=$((PORT + 1))
done

echo -e "${GREEN}   ✅ Port trouvé : $PORT${NC}"
echo ""

# Créer la base de données si nécessaire
if [ ! -f "data/facturation.db" ]; then
    mkdir -p data
    echo "   Initialisation de la base de données..."
    python3 -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
fi

# Lancer l'application
echo "============================================================"
echo -e "${GREEN}✅ Easy Facture est prêt !${NC}"
echo -e "${BLUE}🌐 URL : http://localhost:$PORT${NC}"
echo ""
echo "💡 Le navigateur va s'ouvrir automatiquement..."
echo "⚠️  NE PAS FERMER CETTE FENÊTRE"
echo "============================================================"
echo ""

# Ouvrir le navigateur après 2 secondes
(sleep 2 && open "http://localhost:$PORT") &

# Lancer Flask
export FLASK_APP=run.py
export FLASK_ENV=production
python3 run.py --host=127.0.0.1 --port=$PORT

# Nettoyage à la fermeture
echo ""
echo "⏹️  Arrêt du serveur..."
echo "👋 Au revoir !"
