#!/usr/bin/env python3
"""
Point d'entrée principal de l'application desktop
Lance Flask en arrière-plan et ouvre le navigateur automatiquement
"""

import os
import sys
import webbrowser
import threading
import time
from app import create_app

def open_browser(port=5000):
    """Ouvre le navigateur après le démarrage de Flask"""
    time.sleep(1.5)  # Attendre que Flask soit prêt
    url = f'http://127.0.0.1:{port}'
    print(f"📱 Ouverture du navigateur sur {url}")
    webbrowser.open(url)

def main():
    """Lance l'application desktop"""
    print("=" * 60)
    print("🚀 DÉMARRAGE DE FACTURATION PRO")
    print("=" * 60)
    
    # Créer l'application Flask
    app = create_app('development')
    
    # Déterminer le port
    port = int(os.environ.get('PORT', 5000))
    
    # Ouvrir le navigateur dans un thread séparé
    # (seulement si ce n'est pas le processus de reload de Flask)
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # Afficher les informations
    print(f"\n✅ Application prête !")
    print(f"📊 Interface disponible sur : http://127.0.0.1:{port}")
    print(f"⚠️  Ne fermez pas cette fenêtre\n")
    print("Pour arrêter l'application : Ctrl+C\n")
    print("=" * 60)
    
    # Lancer Flask
    try:
        app.run(
            host='127.0.0.1',
            port=port,
            debug=True,  # Mode debug pour le développement
            use_reloader=True  # Auto-reload en dev
        )
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt de l'application...")
        sys.exit(0)

if __name__ == '__main__':
    main()
