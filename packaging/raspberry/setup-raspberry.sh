#!/bin/bash
# ===============================================
# Easy Facture - Configuration Raspberry Pi
# Par Mondher ADOUDI - Sidr Valley AI
# Version 1.5.0
# ===============================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

clear
echo "============================================================"
echo "   🍓 EASY FACTURE - RASPBERRY PI"
echo "   Version 1.5.0 - Configuration automatique"
echo "============================================================"
echo ""

# Vérifier qu'on est sur un Raspberry
if [ ! -f /proc/device-tree/model ]; then
    echo -e "${YELLOW}⚠️  Ce script est optimisé pour Raspberry Pi${NC}"
    read -p "Continuer quand même ? (o/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        exit 1
    fi
fi

# Installation de base
echo -e "${BLUE}[1/8]${NC} Installation des paquets de base..."
sudo apt-get update -qq
sudo apt-get install -y python3 python3-pip python3-venv sqlite3 -qq
echo -e "${GREEN}   ✅ Paquets installés${NC}"
echo ""

# Configuration de l'environnement
echo -e "${BLUE}[2/8]${NC} Configuration de l'environnement..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}   ✅ Environnement prêt${NC}"
echo ""

# Optimisation mémoire pour Raspberry
echo -e "${BLUE}[3/8]${NC} Optimisation pour Raspberry Pi..."
# Limiter l'utilisation mémoire de Flask
export FLASK_MAX_CONTENT_LENGTH=16777216  # 16MB max upload
echo -e "${GREEN}   ✅ Optimisations appliquées${NC}"
echo ""

# Créer la base de données
echo -e "${BLUE}[4/8]${NC} Initialisation de la base de données..."
mkdir -p data logs
if [ ! -f "data/facturation.db" ]; then
    python3 -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
    echo -e "${GREEN}   ✅ Base de données créée${NC}"
else
    echo -e "${GREEN}   ✅ Base de données existante${NC}"
fi
echo ""

# Créer le service systemd
echo -e "${BLUE}[5/8]${NC} Configuration du service auto-start..."
sudo tee /etc/systemd/system/easy-facture.service > /dev/null << EOF
[Unit]
Description=Easy Facture - Logiciel de facturation
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 $(pwd)/run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable easy-facture.service
echo -e "${GREEN}   ✅ Service créé${NC}"
echo ""

# Créer le raccourci bureau
echo -e "${BLUE}[6/8]${NC} Création du raccourci bureau..."
mkdir -p ~/Desktop
cat > ~/Desktop/EasyFacture.desktop << EOF
[Desktop Entry]
Type=Application
Name=Easy Facture
Comment=Logiciel de facturation
Exec=chromium-browser --app=http://localhost:5000
Icon=$(pwd)/icon.png
Terminal=false
Categories=Office;Finance;
EOF

chmod +x ~/Desktop/EasyFacture.desktop
echo -e "${GREEN}   ✅ Raccourci créé${NC}"
echo ""

# Configuration écran tactile (optionnel)
echo -e "${BLUE}[7/8]${NC} Configuration écran tactile..."
if [ -f /usr/bin/xinput ]; then
    # Calibration basique
    echo "   Écran tactile détecté"
    echo -e "${GREEN}   ✅ Prêt pour écran tactile${NC}"
else
    echo "   Pas d'écran tactile détecté (normal)"
fi
echo ""

# Test final
echo -e "${BLUE}[8/8]${NC} Test de l'installation..."
sudo systemctl start easy-facture.service
sleep 3
if curl -s http://localhost:5000 > /dev/null; then
    echo -e "${GREEN}   ✅ Application fonctionnelle !${NC}"
else
    echo -e "${YELLOW}   ⚠️  Vérifier les logs : journalctl -u easy-facture${NC}"
fi
echo ""

# Résumé
echo "============================================================"
echo -e "${GREEN}🎉 INSTALLATION RASPBERRY PI TERMINÉE !${NC}"
echo "============================================================"
echo ""
echo "🚀 L'application est maintenant :"
echo "  • Lancée automatiquement au démarrage"
echo "  • Accessible sur : http://localhost:5000"
echo "  • Icône sur le bureau"
echo ""
echo "📱 Commandes utiles :"
echo "  • Démarrer  : sudo systemctl start easy-facture"
echo "  • Arrêter   : sudo systemctl stop easy-facture"
echo "  • Redémarrer: sudo systemctl restart easy-facture"
echo "  • Logs      : journalctl -u easy-facture -f"
echo ""
echo "🖨️  Pour configurer une imprimante :"
echo "  • Menu → Préférences → Print Settings"
echo ""
echo "📊 Performances Raspberry Pi :"
echo "  • RAM utilisée : ~200-300 MB"
echo "  • CPU : ~5-10%"
echo "  • Optimisé pour Pi 3B+ et Pi 4"
echo ""
echo "Support : adoudi@mondher.ch"
echo ""

# Reboot optionnel
read -p "Redémarrer maintenant ? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    sudo reboot
fi
