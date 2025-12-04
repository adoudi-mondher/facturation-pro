"""
Easy Facture - Lanceur Windows
Par Mondher ADOUDI - Sidr Valley AI
Version 1.5.0
"""
import sys
import os
import webbrowser
import time
import socket
from threading import Timer

# Ajouter le répertoire courant au path
if getattr(sys, 'frozen', False):
    # Mode PyInstaller
    BASE_DIR = sys._MEIPASS
    os.chdir(os.path.dirname(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_DIR)

def find_free_port(start_port=5000, max_attempts=10):
    """Trouve un port libre"""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

def open_browser(port):
    """Ouvre le navigateur après 2 secondes"""
    time.sleep(2)
    url = f'http://127.0.0.1:{port}'
    print(f"\n🌐 Ouverture du navigateur : {url}")
    webbrowser.open(url)

def main():
    """Lance l'application"""
    print("=" * 60)
    print("   EASY FACTURE v1.5.0")
    print("   Par Mondher ADOUDI - Sidr Valley AI")
    print("=" * 60)
    print()
    
    # Trouver un port libre
    port = find_free_port()
    if not port:
        print("❌ Impossible de trouver un port libre")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    print(f"✅ Port trouvé : {port}")
    print(f"🚀 Démarrage du serveur...")
    print()
    
    # Configurer Flask
    os.environ['FLASK_ENV'] = 'production'
    
    # Ouvrir le navigateur dans 2 secondes
    Timer(2.0, open_browser, args=[port]).start()
    
    # Importer et lancer Flask
    try:
        from app import create_app
        app = create_app('production')
        
        print("=" * 60)
        print(f"✅ Easy Facture est prêt !")
        print(f"🌐 URL : http://127.0.0.1:{port}")
        print()
        print("💡 Le navigateur va s'ouvrir automatiquement...")
        print("⚠️  NE PAS FERMER CETTE FENÊTRE")
        print("=" * 60)
        print()
        
        # Lancer le serveur
        app.run(host='127.0.0.1', port=port, debug=False)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Arrêt du serveur...")
        print("👋 Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == '__main__':
    main()