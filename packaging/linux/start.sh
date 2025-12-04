#!/bin/bash
# ===============================================
# Easy Facture - Lanceur Linux
# Par Mondher ADOUDI - Sidr Valley AI
# ===============================================

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

clear
echo "============================================================"
echo "   🚀 EASY FACTURE v1.5.0"
echo "   Par Mondher ADOUDI - Sidr Valley AI"
echo "============================================================"
echo ""

# Aller dans le répertoire
cd "$(dirname "$0")"

# Activer l'environnement
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Environnement non trouvé. Exécutez install.sh d'abord."
    exit 1
fi

# Trouver un port libre
PORT=5000
while netstat -tuln 2>/dev/null | grep -q ":$PORT "; do
    echo "   Port $PORT occupé, essai du suivant..."
    PORT=$((PORT + 1))
done

echo -e "${GREEN}✅ Port trouvé : $PORT${NC}"
echo ""
echo "============================================================"
echo -e "${GREEN}✅ Easy Facture est prêt !${NC}"
echo -e "${BLUE}🌐 URL : http://localhost:$PORT${NC}"
echo ""
echo "💡 Ouvrez cette URL dans votre navigateur"
echo "⚠️  NE PAS FERMER CETTE FENÊTRE"
echo "============================================================"
echo ""

# Lancer Flask
export FLASK_APP=run.py
export FLASK_ENV=production
python3 run.py --host=127.0.0.1 --port=$PORT
