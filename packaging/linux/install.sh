#!/bin/bash
# ===============================================
# Easy Facture - Installation Linux/Raspberry Pi
# Par Mondher ADOUDI - Sidr Valley AI
# Version 1.5.0
# ===============================================

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear
echo "============================================================"
echo "   📦 EASY FACTURE - INSTALLATION LINUX"
echo "   Version 1.5.0 - Par Mondher ADOUDI"
echo "============================================================"
echo ""

# Vérifier root pour installations système
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⚠️  Ce script nécessite les droits sudo${NC}"
    echo "   Relancez avec : sudo ./install.sh"
    exit 1
fi

# Détecter l'OS
echo -e "${BLUE}[1/7]${NC} Détection du système..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
fi
echo -e "${GREEN}   ✅ Système : $OS $VER${NC}"
echo ""

# Mise à jour des paquets
echo -e "${BLUE}[2/7]${NC} Mise à jour du système..."
apt-get update -qq
echo -e "${GREEN}   ✅ Système à jour${NC}"
echo ""

# Installer Python 3
echo -e "${BLUE}[3/7]${NC} Installation de Python 3..."
if ! command -v python3 &> /dev/null; then
    apt-get install -y python3 python3-pip python3-venv
    echo -e "${GREEN}   ✅ Python 3 installé${NC}"
else
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}   ✅ $PYTHON_VERSION déjà installé${NC}"
fi
echo ""

# Installer SQLite3
echo -e "${BLUE}[4/7]${NC} Installation de SQLite3..."
if ! command -v sqlite3 &> /dev/null; then
    apt-get install -y sqlite3 libsqlite3-dev
    echo -e "${GREEN}   ✅ SQLite3 installé${NC}"
else
    echo -e "${GREEN}   ✅ SQLite3 déjà installé${NC}"
fi
echo ""

# Créer l'environnement virtuel
echo -e "${BLUE}[5/7]${NC} Configuration de l'environnement Python..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}   ✅ Environnement configuré${NC}"
echo ""

# Créer la base de données
echo -e "${BLUE}[6/7]${NC} Initialisation de la base de données..."
mkdir -p data
if [ ! -f "data/facturation.db" ]; then
    python3 -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
    echo -e "${GREEN}   ✅ Base de données créée${NC}"
else
    echo -e "${GREEN}   ✅ Base de données existante${NC}"
fi
echo ""

# Créer le lanceur
echo -e "${BLUE}[7/7]${NC} Création du lanceur..."
cat > /usr/local/bin/easy-facture << 'EOF'
#!/bin/bash
cd /opt/easy-facture
source venv/bin/activate
python3 run.py
EOF

chmod +x /usr/local/bin/easy-facture

# Créer le fichier .desktop pour le menu
cat > /usr/share/applications/easy-facture.desktop << EOF
[Desktop Entry]
Type=Application
Name=Easy Facture
Comment=Logiciel de facturation
Icon=/opt/easy-facture/icon.png
Exec=/usr/local/bin/easy-facture
Terminal=true
Categories=Office;Finance;
EOF

echo -e "${GREEN}   ✅ Lanceur créé${NC}"
echo ""

# Résumé
echo "============================================================"
echo -e "${GREEN}✅ INSTALLATION TERMINÉE !${NC}"
echo "============================================================"
echo ""
echo "Pour lancer Easy Facture :"
echo "  • Depuis le menu : Applications → Easy Facture"
echo "  • Depuis le terminal : easy-facture"
echo "  • Depuis le navigateur : http://localhost:5000"
echo ""
echo "Données : /opt/easy-facture/data/"
echo "Logs : /opt/easy-facture/logs/"
echo ""
echo "Support : adoudi@mondher.ch"
echo ""
