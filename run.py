#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Point d'entree principal de l'application desktop
Lance Flask en arriere-plan et ouvre le navigateur automatiquement

Version 1.6 : Avec systeme de protection par licence (optionnel)
"""

import os
import sys
import webbrowser
import threading
import time
from pathlib import Path
from app import create_app

# Creer .env depuis .env.example si n'existe pas
def ensure_env_file():
    """Cree le fichier .env depuis .env.example si necessaire"""
    env_file = Path('.env')
    env_example = Path('.env.example')

    if not env_file.exists() and env_example.exists():
        print("Initialisation du fichier de configuration...")
        import shutil
        shutil.copy(env_example, env_file)
        print("OK Fichier .env cree")
    elif not env_file.exists() and not env_example.exists():
        # Creer un .env minimal
        print("Creation fichier de configuration minimal...")
        env_file.write_text(
            "# Configuration de l'application\n"
            "SECRET_KEY=\n"
            "DATABASE_URI=sqlite:///data/facturation.db\n",
            encoding='utf-8'
        )
        print("OK Fichier .env cree")

# Configuration de la protection
ENABLE_LICENSE_CHECK = True  # Mettre a True pour activer

def check_license():
    """
    Verifie la licence avant de demarrer
    Mode gracieux : ne bloque pas si probleme de licence en dev

    Validation en 2 etapes :
    1. Validation locale (toujours)
    2. Validation API (une fois par jour si connexion internet)

    Returns:
        bool: True si OK ou mode dev, False si licence invalide en prod
    """
    if not ENABLE_LICENSE_CHECK:
        print("ATTENTION Verification de licence DESACTIVEE (mode dev)")
        return True

    try:
        from app.utils.license import LicenseManager

        manager = LicenseManager()

        # ========================================
        # ETAPE 1: Validation LOCALE (toujours)
        # ========================================
        valid_local, message = manager.validate_license()

        if not valid_local:
            print(f"\n{'='*60}")
            print("ERREUR LICENCE INVALIDE")
            print("="*60)
            print(f"Raison: {message}\n")

            # En mode developpement, on continue quand meme
            if os.environ.get('FLASK_ENV') == 'development':
                print("ATTENTION Mode developpement : demarrage autorise")
                return True

            # En production, on demande une licence
            print("Veuillez entrer votre cle de licence.")
            print("="*60 + "\n")

            # Tenter activation
            return attempt_activation(manager, message)

        # Licence valide localement
        print(f"OK {message}")

        # ========================================
        # ETAPE 2: Validation API (periodique)
        # ========================================
        try:
            from app.utils.trial_client import trial_client

            # Fichier pour tracker le dernier check
            last_check_file = Path("data/.last_api_check")

            # Verifier si on doit checker l'API (une fois par jour)
            if trial_client.should_check_online(last_check_file):
                print("Verification en ligne de la licence...")

                # Charger la licence
                license_file = Path("data/license.key")
                if license_file.exists():
                    license_key = license_file.read_text(encoding='utf-8').strip()
                    machine_id = manager.get_machine_id()

                    # Appeler l'API
                    is_valid_online, msg_online, data = trial_client.validate_license_online(
                        license_key, machine_id
                    )

                    if is_valid_online is False:
                        # Licence revoquee cote serveur
                        print(f"\nERREUR {msg_online}")
                        print("Votre licence a ete revoquee.")
                        return False

                    elif is_valid_online is True:
                        # Licence valide en ligne aussi
                        print(f"OK Validation en ligne reussie")
                        trial_client.mark_checked(last_check_file)

                    # is_valid_online is None = pas de connexion, on continue

        except ImportError:
            # Module trial_client pas installe, on skip la validation API
            pass
        except Exception as e:
            # Erreur lors de la validation API (pas grave, on continue)
            print(f"ATTENTION Validation en ligne impossible: {e}")

        return True

    except ImportError:
        print("ATTENTION Module de licence non installe")
        print("   pip install cryptography")
        return True  # Continuer sans licence

    except Exception as e:
        print(f"ATTENTION Erreur verification licence: {e}")
        return True  # Continuer quand meme (mode gracieux)


def attempt_activation(manager, error_msg):
    """
    Tente d'activer l'application avec une nouvelle licence

    Args:
        manager: Instance de LicenseManager
        error_msg: Message d'erreur a afficher

    Returns:
        bool: Succes de l'activation
    """
    # Obtenir et afficher le Machine ID
    machine_id = manager.get_machine_id()

    try:
        # Tentative avec tkinter (interface graphique)
        import tkinter as tk
        from tkinter import messagebox, simpledialog

        root = tk.Tk()
        root.withdraw()

        # Afficher le Machine ID dans la popup
        messagebox.showinfo(
            "Machine ID - EasyFacture",
            f"Votre Machine ID (pour obtenir une licence) :\n\n{machine_id}\n\n"
            f"Envoyez ce code a votre fournisseur pour recevoir votre licence."
        )

        # Proposer essai gratuit OU activation manuelle
        choice = messagebox.askyesnocancel(
            "Activation - EasyFacture",
            f"{error_msg}\n\n"
            "Que souhaitez-vous faire ?\n\n"
            "OUI : Essai GRATUIT 30 jours (automatique)\n"
            "NON : J'ai deja une licence a activer\n"
            "ANNULER : Quitter"
        )

        if choice is True:
            # ========================================
            # ESSAI GRATUIT (automatique via API)
            # ========================================
            email = simpledialog.askstring(
                "Essai Gratuit - EasyFacture",
                "Entrez votre email pour obtenir votre essai gratuit de 30 jours :",
                parent=root
            )

            if email and email.strip():
                # Importer le client API
                try:
                    from app.utils.trial_client import trial_client

                    # Afficher un message de chargement
                    print("Demande de licence d'essai en cours...")

                    # Appeler l'API
                    success, message, license_key = trial_client.request_trial_license(
                        email=email.strip(),
                        machine_id=machine_id
                    )

                    if success and license_key:
                        # Sauvegarder la licence obtenue
                        if manager.save_license(license_key):
                            # Valider
                            valid, msg = manager.validate_license()
                            if valid:
                                messagebox.showinfo(
                                    "Succes !",
                                    f"OK {message}\n\n{msg}\n\n"
                                    f"Vous pouvez maintenant utiliser EasyFacture pendant 30 jours !"
                                )
                                root.destroy()
                                return True
                            else:
                                messagebox.showerror(
                                    "Erreur",
                                    f"Licence recue mais invalide:\n{msg}"
                                )
                        else:
                            messagebox.showerror(
                                "Erreur",
                                "Impossible de sauvegarder la licence"
                            )
                    else:
                        messagebox.showerror(
                            "Erreur",
                            f"Impossible d'obtenir la licence d'essai:\n\n{message}\n\n"
                            f"Verifiez votre connexion internet ou contactez le support."
                        )

                except ImportError:
                    messagebox.showerror(
                        "Erreur",
                        "Module 'requests' non installe.\n\n"
                        "Installez-le avec: pip install requests"
                    )

        elif choice is False:
            # ========================================
            # ACTIVATION MANUELLE (comme avant)
            # ========================================
            messagebox.showwarning(
                "Licence Requise - EasyFacture",
                "Veuillez entrer votre cle de licence."
            )

            license_key = simpledialog.askstring(
                "Activation de EasyFacture",
                "Cle de licence:",
                parent=root
            )

            if license_key:
                # Sauvegarder
                if manager.save_license(license_key):
                    # Valider
                    valid, msg = manager.validate_license()
                    if valid:
                        messagebox.showinfo(
                            "Succes",
                            "OK Licence activee avec succes!\n\n" + msg
                        )
                        root.destroy()
                        return True
                    else:
                        messagebox.showerror(
                            "Erreur",
                            f"ERREUR Licence invalide:\n{msg}"
                        )
                else:
                    messagebox.showerror(
                        "Erreur",
                        "Impossible de sauvegarder la licence"
                    )

        root.destroy()
        return False

    except ImportError:
        # Fallback console si pas de tkinter
        print("\n" + "="*60)
        print("VOTRE MACHINE ID")
        print("="*60)
        print(f"\n{machine_id}\n")
        print("Envoyez ce code a votre fournisseur pour recevoir votre licence.")
        print("="*60)
        print()
        print("ACTIVATION CONSOLE")
        print("="*60)
        license_key = input("Entrez votre cle de licence: ").strip()

        if license_key:
            if manager.save_license(license_key):
                valid, msg = manager.validate_license()
                if valid:
                    print(f"OK {msg}\n")
                    return True
                else:
                    print(f"ERREUR {msg}\n")

        return False


def open_browser(port=5000):
    """Ouvre le navigateur apres le demarrage de Flask"""
    time.sleep(1.5)
    url = f'http://127.0.0.1:{port}'
    print(f"Ouverture du navigateur sur {url}")
    webbrowser.open(url)


def main():
    """Lance l'application desktop"""
    try:
        print("=" * 60)
        print("DEMARRAGE DE FACTURATION PRO v1.6")
        print("=" * 60)
        print()

        # Assurer que .env existe
        ensure_env_file()
        print()

        # Verification de la licence
        if ENABLE_LICENSE_CHECK:
            print("Verification de la licence...")
            if not check_license():
                print("\nERREUR Impossible de demarrer sans licence valide.")
                print("\nPour obtenir une licence, contactez votre fournisseur.")
                input("\nAppuyez sur Entree pour quitter...")
                sys.exit(1)
            print()
    except Exception as e:
        print(f"\nERREUR CRITIQUE lors du demarrage: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entree pour quitter...")
        sys.exit(1)
    
    # Creer l'application Flask
    try:
        app = create_app('development')
    except Exception as e:
        print(f"ERREUR lors de la creation de l'application: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entree pour quitter...")
        sys.exit(1)
    
    # Determiner le port
    port = int(os.environ.get('PORT', 5000))
    
    # Ouvrir le navigateur dans un thread separe
    # (seulement si ce n'est pas le processus de reload de Flask)
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # Afficher les informations
    print(f"OK Application prete !")
    print(f"Interface disponible sur : http://127.0.0.1:{port}")
    print(f"ATTENTION Ne fermez pas cette fenetre\n")
    print("Pour arreter l'application : Ctrl+C\n")
    print("=" * 60)
    
    # Lancer Flask
    try:
        app.run(
            host='127.0.0.1',
            port=port,
            debug=True,  # Mode debug pour le developpement
            use_reloader=True  # Auto-reload en dev
        )
    except KeyboardInterrupt:
        print("\n\nArret de l'application...")
        sys.exit(0)
    except Exception as e:
        print(f"\nERREUR lors du demarrage: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entree pour quitter...")
        sys.exit(1)


if __name__ == '__main__':
    main()