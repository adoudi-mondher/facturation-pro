#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UTILITAIRE : Récupération du Machine ID
À envoyer au client pour activation à distance

Usage:
    python get_machine_id.py

Le client vous envoie le Machine ID affiché, et vous générez sa licence.
"""

import hashlib
import uuid
import platform


def get_machine_id():
    """
    Génère l'identifiant unique de cette machine
    (Identique à la méthode dans license.py)
    """
    try:
        # MAC Address
        mac = uuid.getnode()
        mac_str = f"{mac:012x}"

        # Infos système
        system = platform.system()
        machine = platform.machine()
        node = platform.node()

        # Combinaison unique
        unique_str = f"{mac_str}-{system}-{machine}-{node}"

        # Hash SHA256 (32 caractères)
        return hashlib.sha256(unique_str.encode()).hexdigest()[:32]

    except Exception as e:
        print(f"⚠️  Erreur : {e}")
        # Fallback minimal
        return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:32]


def main():
    print("="*70)
    print("  FACTURATION PRO - IDENTIFICATION MACHINE")
    print("  Machine ID Generator")
    print("="*70)
    print()

    # Infos système
    print("INFORMATIONS SYSTEME:")
    print("-" * 70)
    print(f"Système        : {platform.system()}")
    print(f"Version        : {platform.version()}")
    print(f"Architecture   : {platform.machine()}")
    print(f"Nom machine    : {platform.node()}")
    print(f"Utilisateur    : {platform.node()}")
    print()

    # Machine ID
    machine_id = get_machine_id()

    print("MACHINE ID:")
    print("="*70)
    print(f"  {machine_id}")
    print("="*70)
    print()

    print("INSTRUCTIONS:")
    print("-" * 70)
    print("1. Copiez le Machine ID ci-dessus")
    print("2. Envoyez-le à votre fournisseur par email")
    print("3. Vous recevrez une clé de licence générée pour cette machine")
    print("4. Entrez la clé lors du premier lancement de l'application")
    print()

    # Sauvegarde dans un fichier
    try:
        filename = f"machine_id_{platform.node()}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("FACTURATION PRO - MACHINE ID\n")
            f.write("="*70 + "\n\n")
            f.write(f"Date        : {platform.node()}\n")
            f.write(f"Système     : {platform.system()} {platform.version()}\n")
            f.write(f"Architecture: {platform.machine()}\n")
            f.write(f"Nom PC      : {platform.node()}\n\n")
            f.write("MACHINE ID:\n")
            f.write("-"*70 + "\n")
            f.write(machine_id + "\n")
            f.write("-"*70 + "\n\n")
            f.write("Envoyez ce fichier à votre fournisseur.\n")

        print(f"✓ Machine ID sauvegardé dans: {filename}")
        print()

    except Exception as e:
        print(f"⚠️  Impossible de sauvegarder le fichier: {e}")

    print("="*70)
    input("\nAppuyez sur Entrée pour fermer...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOpération annulée")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour fermer...")
