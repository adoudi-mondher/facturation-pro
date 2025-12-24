#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur de licences pour les clients
A utiliser UNIQUEMENT par l'administrateur/vendeur

Usage:
    python generate_customer_license.py
    
Notes:
    - La licence est liee a la machine du client
    - Le client doit executer ce script sur SA machine
    - Ou vous devez recuperer son Machine ID
"""

import sys
import os
from datetime import datetime, timedelta

# Ajouter le path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    """Affiche la banniere"""
    print("="*70)
    print("  GENERATEUR DE LICENCES - FACTURATION PRO v1.6")
    print("  License Generator Tool")
    print("="*70)
    print()

def get_license_type():
    """Demande le type de licence"""
    print("Types de licence disponibles:")
    print("  1. Trial (30 jours)")
    print("  2. Mensuelle (30 jours)")
    print("  3. Trimestrielle (90 jours)")
    print("  4. Semestrielle (180 jours)")
    print("  5. Annuelle (365 jours)")
    print("  6. Biennale (730 jours)")
    print("  7. A vie (36500 jours ~ 100 ans)")
    print("  8. Personnalisee")
    print()
    
    choice = input("Choisissez le type (1-8): ").strip()
    
    durations = {
        '1': (30, "Trial"),
        '2': (30, "Mensuelle"),
        '3': (90, "Trimestrielle"),
        '4': (180, "Semestrielle"),
        '5': (365, "Annuelle"),
        '6': (730, "Biennale"),
        '7': (36500, "A vie"),
    }
    
    if choice in durations:
        days, name = durations[choice]
        return days, name
    elif choice == '8':
        try:
            days = int(input("Nombre de jours: ").strip())
            return days, f"Personnalisee ({days} jours)"
        except ValueError:
            print("Erreur: nombre invalide")
            return None, None
    else:
        print("Choix invalide")
        return None, None

def generate_for_current_machine():
    """Genere une licence pour la machine actuelle"""
    print_banner()
    
    try:
        from app.utils.license import LicenseManager
    except ImportError:
        print("ERREUR: Module de licence non trouve")
        print("Verifiez que app/utils/license.py existe")
        return
    
    # Informations client
    print("INFORMATIONS CLIENT")
    print("-" * 70)
    customer_email = input("Email du client: ").strip()
    if not customer_email:
        print("Email requis!")
        return
    
    customer_name = input("Nom du client (optionnel): ").strip()
    company = input("Entreprise (optionnel): ").strip()
    print()
    
    # Type de licence
    days, license_type = get_license_type()
    if days is None:
        return
    
    print()
    print("GENERATION DE LA LICENCE")
    print("-" * 70)
    
    # Generer
    manager = LicenseManager()
    machine_id = manager.get_machine_id()
    
    try:
        license_key = manager.generate_license(customer_email, days)
    except Exception as e:
        print(f"ERREUR lors de la generation: {e}")
        return
    
    # Calculer dates
    today = datetime.now()
    expiry = today + timedelta(days=days)
    
    # Affichage
    print()
    print("="*70)
    print("  LICENCE GENEREE AVEC SUCCES!")
    print("="*70)
    print()
    print(f"Client       : {customer_email}")
    if customer_name:
        print(f"Nom          : {customer_name}")
    if company:
        print(f"Entreprise   : {company}")
    print(f"Type         : {license_type}")
    print(f"Duree        : {days} jours")
    print(f"Date emission: {today.strftime('%d/%m/%Y')}")
    print(f"Date expir.  : {expiry.strftime('%d/%m/%Y')}")
    print(f"Machine ID   : {machine_id}")
    print()
    print("CLE DE LICENCE:")
    print("-" * 70)
    print(license_key)
    print("-" * 70)
    print()
    
    # Sauvegarde
    filename = f"license_{customer_email.replace('@', '_at_')}_{today.strftime('%Y%m%d')}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("FACTURATION PRO - LICENCE CLIENT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Client       : {customer_email}\n")
            if customer_name:
                f.write(f"Nom          : {customer_name}\n")
            if company:
                f.write(f"Entreprise   : {company}\n")
            f.write(f"Type         : {license_type}\n")
            f.write(f"Duree        : {days} jours\n")
            f.write(f"Date emission: {today.strftime('%d/%m/%Y')}\n")
            f.write(f"Date expir.  : {expiry.strftime('%d/%m/%Y')}\n")
            f.write(f"Machine ID   : {machine_id}\n\n")
            f.write("CLE DE LICENCE:\n")
            f.write("-"*70 + "\n")
            f.write(license_key + "\n")
            f.write("-"*70 + "\n\n")
            f.write("INSTRUCTIONS:\n")
            f.write("1. Donnez cette cle au client\n")
            f.write("2. Le client doit l'entrer au premier lancement\n")
            f.write("3. La cle est valable uniquement sur cette machine\n")
            f.write("4. Renouvellement requis apres expiration\n")
        
        print(f"Licence sauvegardee dans: {filename}")
        print()
        
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")
    
    # Test activation
    print("VERIFICATION DE LA LICENCE")
    print("-" * 70)
    
    if manager.save_license(license_key):
        valid, message = manager.validate_license()
        if valid:
            print(f"OK {message}")
            print()
            
            # Demander si on garde la licence activee
            keep = input("Garder la licence activee sur cette machine? (o/n): ").strip().lower()
            if keep != 'o':
                manager.delete_license()
                print("Licence desactivee")
        else:
            print(f"ERREUR {message}")
    
    print()
    print("="*70)


def generate_with_machine_id():
    """Genere une licence avec un Machine ID fourni"""
    print_banner()
    print("GENERATION AVEC MACHINE ID DISTANT")
    print("(Pour generer une licence pour une autre machine)")
    print("-" * 70)
    print()

    print("NOTE: Le client doit vous fournir son Machine ID")
    print("      Il peut l'obtenir en executant get_machine_id.py")
    print("      Ou via: python get_machine_id.py")
    print()

    machine_id = input("Machine ID du client (32 caracteres): ").strip()
    if not machine_id or len(machine_id) != 32:
        print("ERREUR: Machine ID invalide (doit faire exactement 32 caracteres)")
        print(f"Recu: {len(machine_id)} caracteres")
        return

    print(f"Machine ID recu: {machine_id}")
    print()

    try:
        from app.utils.license import LicenseManager
    except ImportError:
        print("ERREUR: Module de licence non trouve")
        print("Verifiez que app/utils/license.py existe")
        return

    # Informations client
    print("INFORMATIONS CLIENT")
    print("-" * 70)
    customer_email = input("Email du client: ").strip()
    if not customer_email:
        print("Email requis!")
        return

    customer_name = input("Nom du client (optionnel): ").strip()
    company = input("Entreprise (optionnel): ").strip()
    print()

    # Type de licence
    days, license_type = get_license_type()
    if days is None:
        return

    print()
    print("GENERATION DE LA LICENCE")
    print("-" * 70)

    # Generer la licence avec le Machine ID fourni
    manager = LicenseManager()

    # IMPORTANT: Remplacer temporairement get_machine_id
    # pour utiliser le Machine ID du client
    original_get_machine_id = manager.get_machine_id
    manager.get_machine_id = lambda: machine_id

    try:
        license_key = manager.generate_license(customer_email, days)
    except Exception as e:
        print(f"ERREUR lors de la generation: {e}")
        return
    finally:
        # Restaurer la methode originale
        manager.get_machine_id = original_get_machine_id

    # Calculer dates
    today = datetime.now()
    expiry = today + timedelta(days=days)

    # Affichage
    print()
    print("="*70)
    print("  LICENCE GENEREE AVEC SUCCES (CLIENT DISTANT)!")
    print("="*70)
    print()
    print(f"Client       : {customer_email}")
    if customer_name:
        print(f"Nom          : {customer_name}")
    if company:
        print(f"Entreprise   : {company}")
    print(f"Type         : {license_type}")
    print(f"Duree        : {days} jours")
    print(f"Date emission: {today.strftime('%d/%m/%Y')}")
    print(f"Date expir.  : {expiry.strftime('%d/%m/%Y')}")
    print(f"Machine ID   : {machine_id}")
    print()
    print("CLE DE LICENCE:")
    print("-" * 70)
    print(license_key)
    print("-" * 70)
    print()

    # Sauvegarde
    filename = f"license_{customer_email.replace('@', '_at_')}_{today.strftime('%Y%m%d')}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("FACTURATION PRO - LICENCE CLIENT (GENERATION DISTANTE)\n")
            f.write("="*70 + "\n\n")
            f.write(f"Client       : {customer_email}\n")
            if customer_name:
                f.write(f"Nom          : {customer_name}\n")
            if company:
                f.write(f"Entreprise   : {company}\n")
            f.write(f"Type         : {license_type}\n")
            f.write(f"Duree        : {days} jours\n")
            f.write(f"Date emission: {today.strftime('%d/%m/%Y')}\n")
            f.write(f"Date expir.  : {expiry.strftime('%d/%m/%Y')}\n")
            f.write(f"Machine ID   : {machine_id}\n\n")
            f.write("CLE DE LICENCE:\n")
            f.write("-"*70 + "\n")
            f.write(license_key + "\n")
            f.write("-"*70 + "\n\n")
            f.write("INSTRUCTIONS POUR LE CLIENT:\n")
            f.write("1. Copiez la cle de licence ci-dessus\n")
            f.write("2. Lancez l'application Facturation Pro\n")
            f.write("3. Entrez la cle lors du premier demarrage\n")
            f.write("4. La cle est valable UNIQUEMENT sur la machine avec cet ID\n")
            f.write("5. Contactez-nous pour renouvellement apres expiration\n\n")
            f.write("IMPORTANT:\n")
            f.write("- Cette licence est liee a la machine du client\n")
            f.write("- Ne partagez pas cette cle avec d'autres machines\n")
            f.write("- En cas de changement de materiel, une nouvelle licence sera necessaire\n")

        print(f"✓ Licence sauvegardee dans: {filename}")
        print()
        print("ENVOI AU CLIENT:")
        print("-" * 70)
        print(f"1. Envoyez le fichier '{filename}' au client par email securise")
        print("2. Ou copiez-collez directement la cle de licence")
        print("3. Le client entre la cle au premier lancement de l'application")
        print()

    except Exception as e:
        print(f"Erreur sauvegarde: {e}")

    print()
    print("="*70)


def main():
    """Menu principal"""
    print_banner()
    
    print("Mode de generation:")
    print("  1. Generer pour cette machine (le client est present)")
    print("  2. Generer avec Machine ID (le client est distant)")
    print("  3. Afficher mon Machine ID")
    print("  4. Quitter")
    print()
    
    choice = input("Choix (1-4): ").strip()
    print()
    
    if choice == '1':
        generate_for_current_machine()
    elif choice == '2':
        generate_with_machine_id()
    elif choice == '3':
        try:
            from app.utils.license import LicenseManager
            manager = LicenseManager()
            print("MACHINE ID DE CE PC:")
            print("-" * 70)
            print(manager.get_machine_id())
            print("-" * 70)
        except Exception as e:
            print(f"Erreur: {e}")
    elif choice == '4':
        print("Au revoir!")
        return
    else:
        print("Choix invalide")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation annulee")
    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()