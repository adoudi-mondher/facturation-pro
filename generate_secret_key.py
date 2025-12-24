#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de SECRET_KEY sécurisée pour Flask

Usage:
    python generate_secret_key.py

Le script génère une clé forte et met à jour automatiquement .env
"""

import secrets
import os
from pathlib import Path


def generate_secret_key():
    """Génère une clé secrète cryptographiquement sûre (64 caractères)"""
    return secrets.token_hex(32)


def generate_license_key():
    """Génère une clé pour le système de licence (Fernet compatible)"""
    from cryptography.fernet import Fernet
    return Fernet.generate_key().decode()


def update_env_file(secret_key, license_key=None):
    """
    Met à jour le fichier .env avec la nouvelle SECRET_KEY

    Args:
        secret_key: Nouvelle SECRET_KEY Flask
        license_key: Nouvelle clé de licence (optionnel)
    """
    env_file = Path('.env')
    env_example = Path('.env.example')

    # Si .env n'existe pas, copier depuis .env.example
    if not env_file.exists():
        if env_example.exists():
            print("📝 Création de .env depuis .env.example...")
            env_file.write_text(env_example.read_text(encoding='utf-8'), encoding='utf-8')
        else:
            print("⚠️  .env.example introuvable, création d'un .env minimal...")
            env_file.write_text(
                f"# Configuration de l'application\n"
                f"SECRET_KEY={secret_key}\n\n"
                f"# Email (optionnel)\n"
                f"SMTP_SERVER=smtp.gmail.com\n"
                f"SMTP_PORT=587\n"
                f"SMTP_USER=\n"
                f"SMTP_PASSWORD=\n",
                encoding='utf-8'
            )
            return

    # Lire le contenu actuel
    lines = env_file.read_text(encoding='utf-8').splitlines()
    updated_lines = []
    secret_key_found = False
    license_key_found = False

    for line in lines:
        # Remplacer SECRET_KEY
        if line.startswith('SECRET_KEY='):
            updated_lines.append(f'SECRET_KEY={secret_key}')
            secret_key_found = True
        # Remplacer LICENSE_SECRET_KEY si fourni
        elif license_key and line.startswith('LICENSE_SECRET_KEY='):
            updated_lines.append(f'LICENSE_SECRET_KEY={license_key}')
            license_key_found = True
        else:
            updated_lines.append(line)

    # Ajouter SECRET_KEY si pas trouvée
    if not secret_key_found:
        updated_lines.insert(1, f'SECRET_KEY={secret_key}')

    # Ajouter LICENSE_SECRET_KEY si fournie et pas trouvée
    if license_key and not license_key_found:
        updated_lines.append('')
        updated_lines.append('# License encryption key')
        updated_lines.append(f'LICENSE_SECRET_KEY={license_key}')

    # Écrire le fichier mis à jour
    env_file.write_text('\n'.join(updated_lines) + '\n', encoding='utf-8')


def main():
    """Menu principal"""
    print("="*70)
    print("  GÉNÉRATEUR DE CLÉS SÉCURISÉES")
    print("  Facturation Pro v1.6.0")
    print("="*70)
    print()

    print("Options disponibles:")
    print("  1. Générer seulement SECRET_KEY Flask")
    print("  2. Générer SECRET_KEY + LICENSE_SECRET_KEY")
    print("  3. Afficher les clés sans modifier .env")
    print("  4. Quitter")
    print()

    choice = input("Votre choix (1-4): ").strip()

    if choice == '4':
        print("Au revoir!")
        return

    # Générer les clés
    secret_key = generate_secret_key()
    license_key = None

    if choice in ['2', '3']:
        try:
            license_key = generate_license_key()
        except ImportError:
            print("⚠️  Module 'cryptography' non installé, clé de licence non générée")
            print("   Installation: pip install cryptography")

    # Afficher les clés
    print()
    print("="*70)
    print("  CLÉS GÉNÉRÉES")
    print("="*70)
    print()
    print("SECRET_KEY (Flask - 64 caractères):")
    print("-"*70)
    print(secret_key)
    print("-"*70)
    print()

    if license_key:
        print("LICENSE_SECRET_KEY (Fernet - 44 caractères):")
        print("-"*70)
        print(license_key)
        print("-"*70)
        print()

    # Mode affichage seulement
    if choice == '3':
        print("✓ Clés générées (non sauvegardées)")
        print()
        print("Pour les utiliser manuellement, ajoutez dans .env:")
        print(f"  SECRET_KEY={secret_key}")
        if license_key:
            print(f"  LICENSE_SECRET_KEY={license_key}")
        return

    # Confirmation avant mise à jour
    print("⚠️  Cette action va modifier le fichier .env")
    confirm = input("Continuer? (o/n): ").strip().lower()

    if confirm != 'o':
        print("Opération annulée")
        return

    # Mise à jour du fichier
    try:
        update_env_file(secret_key, license_key)

        print()
        print("✅ SUCCÈS")
        print("="*70)
        print()
        print("✓ Fichier .env mis à jour avec succès")
        print(f"✓ SECRET_KEY: {secret_key[:20]}...")

        if license_key:
            print(f"✓ LICENSE_SECRET_KEY: {license_key[:20]}...")

        print()
        print("⚠️  IMPORTANT:")
        print("  1. Ne JAMAIS commiter le fichier .env")
        print("  2. Conserver une copie de ces clés en lieu sûr")
        print("  3. Ne pas partager ces clés")
        print()
        print("📝 Prochaines étapes:")
        print("  1. Vérifier .env: cat .env")
        print("  2. Redémarrer l'application: python run.py")
        print("  3. Sauvegarder .env dans un endroit sécurisé")
        print()

    except Exception as e:
        print()
        print(f"❌ ERREUR: {e}")
        print()
        print("Clés générées (copiez-les manuellement):")
        print(f"  SECRET_KEY={secret_key}")
        if license_key:
            print(f"  LICENSE_SECRET_KEY={license_key}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOpération annulée")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
